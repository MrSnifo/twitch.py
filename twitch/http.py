"""
The MIT License (MIT)

Copyright (c) 2023-present Snifo

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
from __future__ import annotations

from .errors import (HTTPException, BadRequest, Conflict, Forbidden, InvalidToken, UserRoleConflict,
                     NotFound, RateLimit, SessionClosed, TwitchServerError, Unauthorized)
from .utils import MISSING, EXCLUSIVE, convert_to_pst_rfc3339, generate_random_text
from . import __version__, __github__
from aiohttp import client_exceptions
from datetime import datetime
from aiohttp import web
import urllib.parse
import aiohttp
import asyncio
import json
import time

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .types import (http as HttpTypes, user as UserTypes, channel as ChannelTypes, chat as ChatTypes,
                        stream as StreamTypes, poll as PollTypes, reward as RewardTypes,
                        prediction as PredictionTypes, alerts as AlertsTypes)
    from typing import Optional, List, Callable, Any, Type, Tuple, Dict, AsyncGenerator, ClassVar, Set
    from aiohttp import ClientWebSocketResponse
    from types import TracebackType

import logging

_logger = logging.getLogger(__name__)

__all__ = ('HTTPClient', 'Server')


class Route:
    """
    Represents an API route for making requests to Twitch endpoints.
    """
    BASE: ClassVar[str] = 'https://api.twitch.tv/helix/'

    __slots__ = ('method', 'endpoint', '_url', '_query_params')

    def __init__(self, method: str, endpoint: Optional[str] = None,
                 query_params: Optional[Dict[str, ...]] = None, url: Optional[str] = None) -> None:
        self.method = method
        self.endpoint = endpoint
        self._url = url
        self._query_params = query_params
        if endpoint is None and url is None:
            raise ValueError("Either 'endpoint' or 'url' must be provided.")

    @property
    def url(self) -> str:
        """
        Get the complete URL for the API request.
        """
        if self._url is not None:
            base_url = self._url
        else:
            base_url = self.BASE + self.endpoint

        if self._query_params:
            query_string = urllib.parse.urlencode(self._query_params, doseq=True)
            url_with_query = f'{base_url}?{query_string}'
            return url_with_query

        return base_url

    def __repr__(self) -> str:
        return f'<Route method={self.method} url={self.url}>'


class HTTPClient:
    """Serves as an HTTP client responsible for sending HTTP requests to the Twitch API."""
    __slots__ = ('_dispatch', '_client_id', '_client_secret', '__session', '_lock',
                 '_user_agent', '_refresh_token', 'cli', '_videos', '_force_close')

    def __init__(self, dispatcher: Callable[..., Any], client_id: str, secret_secret: Optional[str]) -> None:
        self._dispatch: Callable[[str, Any, Any], asyncio.Task] = dispatcher
        self._client_id: str = client_id
        self._client_secret: str = secret_secret
        self.__session: Optional[aiohttp.ClientSession] = None
        self._user_agent: str = f'Twitchify/{__version__} (GitHub: {__github__})'
        self._refresh_token: Optional[str] = None
        # Twitch CLI.
        self.cli: Optional[str] = None
        self._lock: asyncio.Lock = asyncio.Lock()
        # A temporary solution for cashing videos.
        self._videos: Set[str] = set()
        self._force_close: bool = False

    @property
    def is_open(self) -> bool:
        """
        Checks if the HTTP session is open.
        """
        return self.__session is not None and not self.__session.closed

    @property
    def is_force_closed(self) -> bool:
        return self._force_close

    async def _open(self, access_token: Optional[str] = None) -> None:
        """
        Opens an HTTP session.
        """
        async with self._lock:
            if not self.is_open:
                headers = {
                    'Client-ID': self._client_id,
                    'Content-Type': 'application/json'
                }
                if access_token:
                    headers.update({'Authorization': f'Bearer {access_token}'})
                self.__session = aiohttp.ClientSession(headers=headers)
                _logger.debug('New HTTP session has been created.')

    async def close(self) -> bool:
        """
        Closes the HTTP session.
        """
        async with self._lock:
            if self.is_open:
                await self.__session.close()
                self.__session = None
                _logger.debug('HTTP session has been closed.')
        self._force_close = True
        return not self.is_open

    async def open_session(self, token: str, refresh_token: Optional[str] = None) -> HttpTypes.Validate:
        """
        Verifies the access token and opens a new session with it.
        """
        # Opening a session.
        if self.is_open:
            self.__session.headers.update({'Authorization': f'Bearer {token}'})
        else:
            await self._open(access_token=token)
        self._refresh_token = refresh_token
        validation = await self._validate_token(generate=True)
        if validation['expires_in'] == 0:
            _logger.debug('An old has been application detected, exempt from expiration rules.'
                          ' Investigation needed.')
            if self._refresh_token is not None:
                _logger.warning(
                    'The refresh token has been removed due to the access token returning an'
                    ' expire time of 0.')
                self._refresh_token = None
        return validation

    async def ws_connect(self, *, url: str) -> ClientWebSocketResponse:
        """
        Creates a websocket using the existing session.
        """
        if self.is_open:
            websocket: ClientWebSocketResponse = await self.__session.ws_connect(
                url=url,
                headers={'User-Agent': self._user_agent},
                timeout=30,
                autoclose=False
            )
            return websocket
        raise SessionClosed

    async def _request(self, *, route: Route, **kwargs) -> dict:
        """
        HTTP base request.
        """
        method = route.method
        url = route.url
        for retry_count in range(1, 4):
            try:
                async with self.__session.request(method, url, **kwargs) as response:
                    try:
                        data: Dict[str, ...] = await response.json()
                    except (json.JSONDecodeError, client_exceptions.ContentTypeError):
                        data = {}
                    if 200 <= response.status < 300:
                        return data
                    # Handle client-side error.
                    if 400 <= response.status < 500:
                        message = data.get('message', 'Unknown reason.')
                        if response.status == 400:
                            raise BadRequest(message=data.get('message', 'Unknown error.'))
                        if response.status == 401:
                            if any(keyword.lower() in message for keyword in ['access token is not',
                                                                              'invalid access token',
                                                                              'header is required and '
                                                                              'must']):
                                raise InvalidToken(message=message)
                            elif 'not authorized' in message:
                                raise Unauthorized(message='You are not authorized')
                            raise Unauthorized(message=message)
                        elif response.status == 403:
                            raise Forbidden(message=message)
                        elif response.status == 404:
                            raise NotFound(message=data.get('message', 'Unknown error.'))
                        elif response.status == 422:
                            raise UserRoleConflict(message=message)
                        elif response.status == 409:
                            raise Conflict(message=message)
                        elif response.status == 429:
                            raise RateLimit
                        else:
                            raise BadRequest(message=data.get('message', 'Unknown error.'))
                    # Handle server-side error
                    elif 500 <= response.status < 600:
                        raise TwitchServerError
                    else:
                        raise HTTPException
            except (TwitchServerError, OSError):
                if 3 >= retry_count:
                    _logger.info('Request failed: %s. Retrying in %s seconds...',
                                 Route, (5 * retry_count))
                    await asyncio.sleep(5 * retry_count)
                raise

    async def _generate_token(self) -> Optional[HttpTypes.Token]:
        """
        Generate a new access token using client_secret and refresh_token.
        """
        if self._refresh_token and self._client_secret:
            # There is a chance that both the task and the normal
            # request can refresh the token at the same time.
            if not self._lock.locked():
                async with self._lock:
                    # Encoding the client secret.
                    encoded_secret = aiohttp.helpers.quote(self._refresh_token)
                    params = {'grant_type': 'refresh_token',
                              'refresh_token': encoded_secret,
                              'client_id': self._client_id,
                              'client_secret': self._client_secret}
                    _logger.debug('Generating a new access token to refresh the existing one.')
                    route = Route(method='POST', url='https://id.twitch.tv/oauth2/token')
                    refresh = await self.request(route=route, params=params)
                    # Updating the session headers.
                    self.__session.headers.update({'Authorization': f'Bearer {refresh["access_token"]}'})
                    _logger.debug('Session headers have been successfully updated with'
                                  ' the new access token.')
                    self._dispatch('refresh_token', refresh['access_token'])
                    return refresh
        return None

    async def auth_code(self, code: str, redirect_uri: str) -> Tuple[str, str]:
        """
        Authorization using the code to get the access token and refresh token.
        """
        await self._open()
        params = {'client_id': self._client_id,
                  'client_secret': self._client_secret,
                  'code': code,
                  'grant_type': 'authorization_code',
                  'redirect_uri': redirect_uri}
        route = Route(method='POST', url='https://id.twitch.tv/oauth2/token')
        token = await self.request(route=route, params=params)
        return token['access_token'], token['refresh_token']

    async def _validate_token(self, *, generate: bool = False) -> HttpTypes.Validate:
        """
        Validate access token.
        """
        while True:
            try:
                route = Route(method='GET', url='https://id.twitch.tv/oauth2/validate')
                validation = await self._request(route=route)
                _logger.debug('Access token successfully validated.')
                return validation
            except InvalidToken as exc:
                if generate and (self._client_secret and self._refresh_token):
                    try:
                        # Generating a new access token.
                        await self._generate_token()
                        continue
                    except (BadRequest, Forbidden):
                        raise InvalidToken(message='Invalid refresh token or client secret.') from exc
                else:
                    raise

    async def refresher(self, *, expires_in: int) -> None:
        """
        Refresher task to refresh the current access token or generates a new one if needed.
        """
        start_time = time.time()
        # If the refresh_token or client_secret is missing,
        if self._refresh_token and self._client_secret:
            _logger.debug('A new token will be generated in %s seconds.', expires_in - 300)
        else:
            # Set expires_in to a default value of 3540 seconds (59 minutes).
            expires_in = 3540 + 300
            _logger.warning('Access token will expire in %s seconds, and won\'t be generated without '
                            'the refresh token or client secret.', expires_in - 300)
        while True:
            # Create a new access token approximately 5 minutes before the
            # current token's expiration.
            await asyncio.sleep(min((expires_in - 300), 3540))
            current_time = time.time()
            elapsed_time = current_time - start_time
            try:
                if elapsed_time >= expires_in - 300:
                    # Reset the refresh token timer
                    start_time = time.time()
                    await self._generate_token()
                    _logger.debug('A new token will be generated in %s. seconds', expires_in - 300)
                # ==> Validating the access token <==
                validation = await self._validate_token()
                # Update the expiration time of the access token.
                expires_in = validation['expires_in']
            except BadRequest:
                _logger.warning('Invalid Refresh Token.'
                                ' The automatic generation feature has been disabled.')
                self._refresh_token = None

    async def request(self, *, route: Route, **kwargs) -> _request:
        """
        Sends an HTTP request to the specified route.
        """
        while True:
            try:
                _logger.debug('Sending request: %s kwargs: %s.', route, kwargs)
                data: dict = await self._request(route=route, **kwargs)
                _logger.debug('Received response: %s', data)
                return data
            except InvalidToken:
                try:
                    _logger.error('Unable to make the request to URL: %s Unauthorized access.',
                                  route.url)
                    await self._validate_token(generate=True)
                    continue
                except (InvalidToken, BadRequest):
                    raise

    async def subscribe(self, user_id: str, session_id: str,
                        subscriptions: List[HttpTypes.SubscriptionInfo]) -> None:
        """
        Subscribes to multiple events with the specified subscriptions.
        """
        for subscription in subscriptions:
            try:
                data = {
                    'type': subscription['name'],
                    'version': subscription['version'],
                    'condition': {
                        'user_id': user_id,
                        'broadcaster_user_id': user_id,
                        'moderator_user_id': user_id,
                        'to_broadcaster_user_id': user_id
                    },
                    'transport': {
                        'method': 'websocket',
                        'session_id': session_id
                    }
                }
                _logger.debug('Subscribing to `%s` event version %s.',
                              subscription['name'], subscription['version'])
                if self.cli:
                    route = Route(method='POST', url=self.cli)
                else:
                    route = Route(method='POST', endpoint='eventsub/subscriptions')
                await self.request(route=route, json=data)

            except (Forbidden, BadRequest) as error:
                if isinstance(error, Forbidden):
                    _logger.error('Subscription type `%s` version `%s` is missing scope `%s`.',
                                  subscription['name'], subscription['version'], subscription['scope'])
                if isinstance(error, BadRequest):
                    _logger.warning('Subscription type `%s` version `%s` unsupported.',
                                    subscription['name'], subscription['version'])
        self._dispatch('ready')

    async def _pagination_request(self,
                                  route: Route,
                                  query_params: Dict[str, ...],
                                  limit: int,
                                  check_length: bool = False,
                                  length: int = 100) -> AsyncGenerator[List[Any]]:
        """
        Request pagination.
        """
        if limit == 0:
            limit = 1
        if limit < 0:
            limit = 10000
        for _ in range(limit):
            data = await self.request(route=route)
            yield data['data']
            if check_length and length != len(data['data']):
                return
            if data['pagination'].get('cursor'):
                query_params['after'] = data['pagination']['cursor']
            else:
                return

    # --------------------------------
    #            + Stream +
    # --------------------------------
    async def fetch_streams(self, *, limit: int,
                            user_ids: List[str] = MISSING, user_names: List[str] = MISSING,
                            game_ids: List[str] = MISSING, stream_type: str = MISSING,
                            languages: List[str] = MISSING) -> AsyncGenerator[List[StreamTypes.Stream]]:
        # Gets a list of all streams. The list is in descending order by the number of viewers watching
        # the stream.
        params = {
            'user_id': user_ids,
            'user_login': user_names,
            'game_id': game_ids,
            'stream_type': stream_type,
            'language': languages,
        }
        # Remove keys with MISSING values from the dictionary.
        params = {key: value for key, value in params.items() if value is not MISSING}
        # Calculate the total length of values for list-type keys.
        total_list_values = sum(len(value) for key, value in params.items() if isinstance(value, list))
        if total_list_values <= 100:
            route = Route('GET', 'streams', params)
            async for data in self._pagination_request(route=route, query_params=params, limit=limit):
                yield data
        else:
            raise TypeError('Exceeded maximum limit. Please provide no more than 100 items.')

    async def create_stream_marker(self, *, user_id: str,
                                   description: str = MISSING) -> StreamTypes.StreamMarker:
        # Adds a marker to a live stream. A marker is an arbitrary point in a live stream that the
        # broadcaster or editor wants to mark.
        _payload = {'user_id': user_id}
        if description is not MISSING:
            if len(description) > 140:
                raise ValueError('The maximum length of the description is 140 characters.')
            _payload['description'] = description

        route = Route('POST', 'streams/markers')
        data = await self.request(route=route, json=_payload)
        return data['data'][0]

    async def start_commercial(self, *, broadcaster_id: str, length: int) -> StreamTypes.StartCommercial:
        # Starts a commercial on the specified channel.
        _payload = {'broadcaster_id': broadcaster_id, 'length': length}
        route = Route('POST', 'channels/commercial')
        data = await self.request(route=route, json=_payload)
        return data['data'][0]

    async def create_clip(self, *, broadcaster_id: str, has_delay: bool) -> StreamTypes.CreateClip:
        # Creates a clip from the broadcaster’s stream.
        params = {'broadcaster_id': broadcaster_id, 'has_delay': has_delay}
        route = Route('POST', 'clips', params)
        data = await self.request(route=route)
        return data['data'][0]

    async def start_raid(self, *, broadcaster_id: str, user_id: str) -> StreamTypes.StartRaid:
        # Raid another channel by sending the broadcaster’s viewers to the targeted channel.
        params = {'from_broadcaster_id': broadcaster_id, 'to_broadcaster_id': user_id}
        route = Route('POST', 'raids', params)
        data = await self.request(route=route)
        return data['data'][0]

    async def cancel_raid(self, *, broadcaster_id: str) -> None:
        # Cancel a pending raid.
        params = {'broadcaster_id': broadcaster_id}
        route = Route('DELETE ', 'raids', params)
        await self.request(route=route)

    async def get_categories(self, *, category_ids: List[str] = MISSING,
                             category_names: List[str] = MISSING,
                             igdb_ids: List[str] = MISSING) -> List[StreamTypes.GetGame]:
        # Default query parameters.
        params = {
            'id': category_ids,
            'name': category_names,
            'igdb_id': igdb_ids
        }
        # Remove keys with MISSING values from the dictionary.
        params = {key: value for key, value in params.items() if value is not MISSING}
        route = Route('GET', 'games', params)
        data = await self.request(route=route)
        return data['data']

    # -----------------------------------
    #          + Chat Settings +
    # -----------------------------------
    async def get_chat_settings(self, *, broadcaster_id: str, moderator_id: str) -> ChatTypes.ChatSettings:
        # Gets the broadcaster’s chat settings.
        params = {'broadcaster_id': broadcaster_id, 'moderator_id': moderator_id}
        route = Route('GET', 'chat/settings', params)
        data = await self.request(route=route)
        return data['data'][0]

    async def update_chat_settings(self, *, broadcaster_id: str, moderator_id: str,
                                   emote_mode: bool = MISSING,
                                   follower_mode: bool = MISSING,
                                   follower_mode_duration: Optional[int] = MISSING,
                                   non_moderator_chat_delay: bool = MISSING,
                                   non_moderator_chat_delay_duration: Optional[int] = MISSING,
                                   slow_mode: bool = MISSING,
                                   slow_mode_wait_time: Optional[int] = MISSING,
                                   subscriber_mode: bool = MISSING,
                                   unique_chat_mode: bool = MISSING) -> ChatTypes.ChatSettings:
        # Updates the broadcaster’s chat settings.
        params = {'broadcaster_id': broadcaster_id, 'moderator_id': moderator_id}
        _payload = {'emote_mode': emote_mode,
                    'subscriber_mode': subscriber_mode,
                    'unique_chat_mode': unique_chat_mode,
                    'follower_mode': follower_mode,
                    'non_moderator_chat_delay': non_moderator_chat_delay,
                    'slow_mode': slow_mode}
        # Remove keys with MISSING values from the dictionary.
        _payload = {key: value for key, value in _payload.items() if value is not MISSING}
        # Auto enable modes if duration is provided and mode not.
        if isinstance(follower_mode_duration, int):
            _payload['follower_mode_duration'] = follower_mode_duration
            _payload['follower_mode'] = True if (follower_mode is MISSING) else follower_mode
        if isinstance(non_moderator_chat_delay_duration, int):
            _payload['non_moderator_chat_delay_duration'] = non_moderator_chat_delay_duration
            _non_moderator = non_moderator_chat_delay
            _payload['non_moderator_chat_delay'] = True if (_non_moderator is MISSING) else _non_moderator
        if isinstance(slow_mode_wait_time, int):
            _payload['slow_mode_wait_time'] = slow_mode_wait_time
            _payload['slow_mode'] = True if (slow_mode is MISSING) else follower_mode
        route = Route('PATCH', 'chat/settings', params)
        data = await self.request(route=route, json=_payload)
        return data['data'][0]

    # -----------------------------------
    #          + Chat Chatters +
    # -----------------------------------
    async def fetch_chatters(self, *, limit: int, broadcaster_id: str,
                             moderator_id: str) -> AsyncGenerator[List[UserTypes.SpecificUser]]:
        # Gets the list of users that are connected to the broadcaster’s chat session.
        params = {'broadcaster_id': broadcaster_id, 'moderator_id': moderator_id}
        route = Route('GET', 'chat/chatters', params)
        async for data in self._pagination_request(route=route, query_params=params, limit=limit):
            yield data

    async def get_total_chatters(self, *, broadcaster_id: str, moderator_id: str) -> int:
        # Gets the total number of users that are connected to the broadcaster’s chat session.
        params = {'broadcaster_id': broadcaster_id, 'moderator_id': moderator_id}
        route = Route('GET', 'chat/chatters', params)
        data = await self.request(route=route)
        return data['total']

    # -----------------------------------
    #           + Chat Emotes +
    # -----------------------------------
    async def get_global_emotes(self) -> Tuple[str, List[ChatTypes.BaseEmote]]:
        # Gets the list of global emotes.
        route = Route('GET', 'chat/emotes/global')
        data = await self.request(route=route)
        return data['template'], data['data']

    async def get_channel_emotes(self, *, broadcaster_id: str) -> Tuple[str, List[ChatTypes.Emote]]:
        # Gets the broadcaster’s list of custom emotes.
        params = {'broadcaster_id': broadcaster_id}
        route = Route('GET', 'chat/emotes', params)
        data = await self.request(route=route)
        return data['template'], data['data']

    # ----------------------------------
    #           + Chat Badge +
    # ----------------------------------
    async def get_global_chat_badge(self) -> List[ChatTypes.Badge]:
        # Gets the list of global badges.
        route = Route('GET', 'chat/badges/global')
        data = await self.request(route=route)
        return data['data']

    async def get_channel_chat_badges(self, *, broadcaster_id: str) -> List[ChatTypes.Badge]:
        # Gets the broadcaster’s list of custom chat badges.
        params = {'broadcaster_id': broadcaster_id}
        route = Route('GET', 'chat/badges', params)
        data = await self.request(route=route)
        return data['data']

    # ---------------------------------
    #        + Chat Cheermotes +
    # ---------------------------------
    async def get_cheermotes(self, *, broadcaster_id: str) -> List[ChatTypes.Cheermote]:
        # Gets a list of Cheermotes that users can use to cheer Bits in any Bits-enabled channel’s chat room.
        params = {'broadcaster_id': broadcaster_id}
        route = Route('GET', 'bits/cheermotes', params)
        data = await self.request(route=route)
        return data['data']

    # -----------------------------------
    #       + Chat Announcements  +
    # -----------------------------------
    async def send_chat_announcements(self, *, broadcaster_id: str, moderator_id: str, message: str,
                                      color: str = MISSING) -> None:
        # Sends an announcement to the broadcaster’s chat room.
        params = {'broadcaster_id': broadcaster_id, 'moderator_id': moderator_id}
        if len(message) <= 500:
            _payload = {'message': message}
            if color is not MISSING:
                _payload['color'] = color
            route = Route('POST', 'chat/announcements', params)
            await self.request(route=route, json=_payload)
        else:
            raise ValueError('Announcements are limited to a maximum of 500 characters.')

    # -----------------------------------
    #       + Chat Announcements  +
    # -----------------------------------
    async def send_shoutout(self, *, broadcaster_id: str, moderator_id: str, to_broadcaster_id: str) -> None:
        # Sends a Shoutout to the specified broadcaster.
        params = {
            'from_broadcaster_id': broadcaster_id,
            'to_broadcaster_id': to_broadcaster_id,
            'moderator_id': moderator_id,
        }
        if broadcaster_id == to_broadcaster_id:
            raise TypeError('The broadcaster may not give themselves a Shoutout.')
        route = Route('POST', 'chat/shoutouts', params)
        await self.request(route=route)

    # ----------------------------------
    #      + Chat Delete messages +
    # -----------------------------------
    async def delete_chat_messages(self, *, broadcaster_id: str, moderator_id: str,
                                   message_id: str = MISSING) -> None:
        # Removes a single chat message or all chat messages from the broadcaster’s chat room.
        params = {'broadcaster_id': broadcaster_id, 'moderator_id': moderator_id}
        # If `message_id` is Missing will clear the chat.
        if message_id is not MISSING:
            params['message_id'] = message_id
        route = Route('DELETE', 'moderation/chat', params)
        await self.request(route=route)

    # -----------------------------------
    #         + Chat ShieldMode +
    # -----------------------------------
    async def get_shield_mode_status(self, *, broadcaster_id: str,
                                     moderator_id: str = MISSING) -> ChatTypes.ShieldMode:
        # Gets the broadcaster’s Shield Mode activation status.
        params = {'broadcaster_id': broadcaster_id, 'moderator_id': moderator_id}
        route = Route('GET', 'moderation/shield_mode', params)
        data = await self.request(route=route)
        return data['data'][0]

    async def update_shield_mode_status(self, *, broadcaster_id: str, moderator_id: str,
                                        activate: bool) -> ChatTypes.ShieldMode:
        # Activates or deactivates the broadcaster’s Shield Mode.
        params = {
            'broadcaster_id': broadcaster_id, 'moderator_id': moderator_id
        }
        _payload = {'is_active': activate}
        route = Route('PUT', 'moderation/shield_mode', params)
        data = await self.request(route=route, json=_payload)
        return data['data'][0]

    # ------------------------------------
    #           + Chat AutoMod +
    # ------------------------------------
    async def get_automod_settings(self, *, broadcaster_id: str,
                                   moderator_id: str = MISSING) -> ChatTypes.AutoModSettings:
        # Gets the broadcaster’s AutoMod settings.
        params = {'broadcaster_id': broadcaster_id, 'moderator_id': moderator_id}
        route = Route('GET', 'moderation/automod/settings', params)
        data = await self.request(route=route)
        return data['data'][0]

    async def update_automod_settings(self, *, broadcaster_id: str,
                                      moderator_id: str = MISSING,
                                      overall_level: int = MISSING,
                                      aggression: int = MISSING,
                                      bullying: int = MISSING,
                                      disability: int = MISSING,
                                      misogyny: int = MISSING,
                                      race_ethnicity_or_religion: int = MISSING,
                                      sex_based_terms: int = MISSING,
                                      sexuality_sex_or_gender: int = MISSING,
                                      swearing: int = MISSING) -> ChatTypes.AutoModSettings:
        # Updates the broadcaster’s AutoMod settings
        params = {'broadcaster_id': broadcaster_id, 'moderator_id': moderator_id}
        if overall_level is MISSING:
            _payload = {
                'aggression': aggression,
                'bullying': bullying,
                'disability': disability,
                'misogyny': misogyny,
                'race_ethnicity_or_religion': race_ethnicity_or_religion,
                'sex_based_terms': sex_based_terms,
                'sexuality_sex_or_gender': sexuality_sex_or_gender,
                'swearing': swearing}
            # Remove keys with MISSING values from the dictionary.
            _payload = {key: value for key, value in _payload.items() if value is not MISSING}
        else:
            _payload = {'overall_level': overall_level}
        route = Route('PUT', 'moderation/automod/settings', params)
        data = await self.request(route=route, json=_payload)
        return data['data'][0]

    async def check_automod_status(self, *, broadcaster_id: str, messages: List[str]) -> List[bool]:
        # Checks whether AutoMod would flag the specified messages for review.
        params = {'broadcaster_id': broadcaster_id}
        if 1 <= len(messages) <= 100:
            _payload = {'data': [{'msg_id': generate_random_text(), 'msg_text': msg} for msg in messages]}
            route = Route('POST', 'moderation/enforcements/status', params)
            data = await self.request(route=route, json=_payload)
            # Organize the data using message IDs and extract the AutoMod status.
            msg_id_to_permitted = {entry['msg_id']: (not entry['is_permitted']) for entry in data['data']}
            # Create a list of boolean values indicating AutoMod status for each message.
            bool_list = [msg_id_to_permitted[entry['msg_id']] for entry in _payload['data']]
            return bool_list
        raise TypeError('The number of messages must be between 1 and 100.')

    async def manage_held_automod_messages(self, *, user_id: str, msg_id: str, allow: bool) -> None:
        # Allow or deny the message that AutoMod flagged for review.
        _payload = {'user_id': user_id, 'msg_id': msg_id, 'action': ('ALLOW' if allow else 'DENY')}
        route = Route('POST', 'moderation/automod/message')
        await self.request(route=route, json=_payload)

    async def fetch_blocked_terms(self, *, limit: int, broadcaster_id: str,
                                  moderator_id: str) -> AsyncGenerator[List[ChatTypes.BlockedTerm]]:
        # Gets the broadcaster’s list of non-private, blocked words or phrases.
        params = {'broadcaster_id': broadcaster_id, 'moderator_id': moderator_id, 'first': '100'}
        route = Route('GET', 'moderation/blocked_terms', params)
        async for data in self._pagination_request(limit=limit, route=route, query_params=params):
            yield data

    async def add_blocked_term(self, *, broadcaster_id: str, moderator_id: str,
                               text: str) -> ChatTypes.BlockedTerm:
        # Adds a word or phrase to the broadcaster’s list of blocked terms.
        params = {'broadcaster_id': broadcaster_id, 'moderator_id': moderator_id}
        if 2 <= len(text) <= 500:
            route = Route('POST', 'moderation/blocked_terms', params)
            data = await self.request(route=route, json={'text': text})
            return data['data'][0]
        raise ValueError('The term must contain 2 to 500 characters.')

    async def remove_blocked_term(self, *, broadcaster_id: str, moderator_id: str, term_id: str) -> None:
        # Removes the word or phrase from the broadcaster’s list of blocked terms.
        params = {'broadcaster_id': broadcaster_id, 'moderator_id': moderator_id, 'id': term_id}
        route = Route('DELETE', 'moderation/blocked_terms', params)
        await self.request(route=route)

    # ---------------------------------
    #            + Channel +
    # ---------------------------------
    async def get_channels(self, *, broadcaster_ids: List[str]) -> List[ChannelTypes.Channel]:
        params = {'broadcaster_id': broadcaster_ids}
        if len(broadcaster_ids) <= 100:
            route = Route('GET', 'channels', params)
            data = await self.request(route=route)
            return data['data']
        raise TypeError('The maximum number of broadcasters you may specify is 100.')

    async def modify_channel_information(self, *,
                                         broadcaster_id: str,
                                         category_id: Optional[str] = MISSING,
                                         language: str = MISSING,
                                         title: str = MISSING,
                                         delay: int = MISSING,
                                         tags: Optional[List[str]] = MISSING,
                                         branded_content: Optional[bool] = MISSING,
                                         ccls: List[ChannelTypes.CCLs] = MISSING,
                                         ccls_enable: bool = MISSING) -> None:
        # Updates a channel’s properties.
        params = {'broadcaster_id': broadcaster_id}
        _payload = {
            'game_id': '0' if category_id is None else category_id,
            'broadcaster_language': language,
            'title': title,
            'tags': [] if tags is None else tags,
            'is_branded_content': branded_content,
        }
        # Remove keys with MISSING values from the dictionary.
        _payload = {key: value for key, value in _payload.items() if value is not MISSING}
        # The number of seconds you want your broadcast buffered before streaming it live.
        if delay is not MISSING:
            if not (isinstance(delay, int) and delay <= 900):
                raise ValueError('Delay must be integer and maximum of 900 seconds.')
            _payload['delay'] = delay
        # List of labels that should be set as the Channel’s CCLs.
        if ccls is not MISSING and ccls_enable is not MISSING:
            _payload['content_classification_labels'] = []
            for ccl in ccls:
                _payload['content_classification_labels'].append({'id': ccl, 'is_enabled': ccls_enable})
        route = Route('PATCH', 'channels', params)
        await self.request(route=route, json=_payload)

    async def get_goals(self, *, broadcaster_id: str) -> List[AlertsTypes.Goal]:
        # Gets the broadcaster’s list of active goals.
        params = {'broadcaster_id': broadcaster_id}
        route = Route('GET', 'goals', params)
        data = await self.request(route=route)
        return data['data']

    async def fetch_hype_trains(self, *, limit: int, broadcaster_id: str) \
            -> AsyncGenerator[List[AlertsTypes.HypeTrain]]:
        # Gets information about the broadcaster’s current or most recent Hype Train event.
        params = {'broadcaster_id': broadcaster_id, 'first': '100'}
        route = Route('GET', 'hypetrain/events', params)
        async for data in self._pagination_request(limit=limit, route=route, query_params=params):
            yield data

    async def get_channel_stream_key(self, *, broadcaster_id: str) -> str:
        # Gets the channel’s stream key.
        params = {'broadcaster_id': broadcaster_id}
        route = Route('GET', 'streams/key', params)
        data = await self.request(route=route)
        return data['data'][0]['stream_key']

    # ---------------------------------
    #    + Channel Bits Leaderboard +
    # ---------------------------------
    async def get_bits_leaderboard(self, *, count: int, period: str = MISSING, user_id: str = MISSING,
                                   started_at: datetime = MISSING) -> List[ChannelTypes.UserBitsLeaderboard]:
        # Gets the Bits leaderboard for the authenticated broadcaster.
        params = {'count': count, 'period': 'all'}
        if period is not MISSING:
            params['period'] = period
        if started_at is MISSING:
            # When the user only specifies the period, it will auto set the started_at to the current
            # datetime.
            started_at = convert_to_pst_rfc3339(datetime.now())
        else:
            started_at = convert_to_pst_rfc3339(started_at)
        params['started_at'] = started_at
        if user_id is not MISSING:
            params['user_id'] = user_id
        route = Route('GET', 'bits/leaderboard', params)
        data = await self.request(route=route)
        return data['data']

    # --------------------------------
    #      + Channel Moderators +
    # --------------------------------
    async def fetch_moderators(self, *, limit: int, broadcaster_id: str, user_ids: List[str] = MISSING
                               ) -> AsyncGenerator[List[UserTypes.SpecificUser]]:
        # Gets all users allowed to moderate the broadcaster’s chat room.
        params = {'broadcaster_id': broadcaster_id, 'first': '100'}
        if user_ids is not MISSING:
            if len(user_ids) > 100:
                raise TypeError('The maximum number of users you may specify is 100.')
            params['user_id'] = user_ids
        route = Route('GET', 'moderation/moderators', params)
        async for data in self._pagination_request(limit=limit, route=route, query_params=params):
            yield data

    async def add_channel_moderator(self, *, broadcaster_id: str, user_id: str, force: bool = False) -> None:
        # Adds a moderator to the broadcaster’s chat room.
        params = {'broadcaster_id': broadcaster_id, 'user_id': user_id}
        route = Route('POST', 'moderation/moderators', params)
        while True:
            try:
                await self.request(route=route)
                return
            except UserRoleConflict as state:
                # Auto removes VIP from the user.
                if force and 'vip' in str(state).lower():
                    await self.remove_channel_vip(broadcaster_id=broadcaster_id, user_id=user_id)
                    force = False
                    continue
                raise

    async def remove_channel_moderator(self, *, broadcaster_id: str, user_id: str) -> None:
        # Removes a moderator from the broadcaster’s chat room.
        params = {'broadcaster_id': broadcaster_id, 'user_id': user_id}
        route = Route('DELETE', 'moderation/moderators', params)
        await self.request(route=route)

    # ---------------------------
    #     + Channel Editors +
    # ---------------------------
    async def get_channel_editors(self, *, broadcaster_id: str) -> List[ChannelTypes.Editor]:
        # Gets the broadcaster’s list editors.
        params = {'broadcaster_id': broadcaster_id}
        route = Route('GET', 'channels/editors', params)
        data = await self.request(route=route)
        return data['data']

    # --------------------------------
    #         + Channel Vips +
    # --------------------------------
    async def fetch_vips(self, *, limit: int, broadcaster_id: str, user_ids: List[str] = MISSING
                         ) -> AsyncGenerator[List[UserTypes.SpecificUser]]:
        # Gets a list of the broadcaster’s VIPs.
        params = {'broadcaster_id': broadcaster_id, 'first': '100'}
        if user_ids is not MISSING:
            if len(user_ids) > 100:
                raise TypeError('The maximum number of users you may specify is 100.')
            params['user_id'] = user_ids
        route = Route('GET', 'channels/vips', params)
        async for data in self._pagination_request(limit=limit, route=route, query_params=params):
            yield data

    async def add_channel_vip(self, *, broadcaster_id: str, user_id: str, force: bool = False) -> None:
        # Adds the specified user as a VIP in the broadcaster’s channel.
        params = {'broadcaster_id': broadcaster_id, 'user_id': user_id}
        route = Route('POST', 'channels/vips', params)
        while True:
            try:
                await self.request(route=route)
                return
            except UserRoleConflict as state:
                # Auto remove user Moderator.
                if force and 'moderator' in str(state):
                    await self.remove_channel_moderator(broadcaster_id=broadcaster_id, user_id=user_id)
                    force = False
                    continue
                raise

    async def remove_channel_vip(self, *, broadcaster_id: str, user_id: str) -> None:
        # Removes the specified user as a VIP in the broadcaster’s channel.
        params = {'broadcaster_id': broadcaster_id, 'user_id': user_id}
        route = Route('DELETE', 'channels/vips', params)
        await self.request(route=route)

    # ---------------------------------
    #       + Channel Ban/Unban +
    # ---------------------------------
    async def fetch_banned_users(self, *, broadcaster_id: str,
                                 limit: int,
                                 user_ids: List[str] = MISSING
                                 ) -> AsyncGenerator[List[ChannelTypes.BannedUser]]:
        # Gets all users that the broadcaster banned or put in a timeout.
        params = {'broadcaster_id': broadcaster_id, 'first': '100'}
        if user_ids is not MISSING:
            params['user_id'] = user_ids
        route = Route('GET', 'moderation/banned', params)
        async for data in self._pagination_request(limit=limit, route=route, query_params=params,
                                                   check_length=True):
            yield data

    async def ban_user(self, *, broadcaster_id: str, moderator_id: str, user_id: str,
                       duration: int = MISSING, reason: str = MISSING) -> None:
        # Bans a user from participating in the specified broadcaster’s chat room or puts them in a timeout.
        params = {'broadcaster_id': broadcaster_id, 'moderator_id': moderator_id}
        _payload = {'data': {'user_id': user_id}}
        if duration is not MISSING:
            if 1209600 >= duration >= 1:
                _payload['data']['duration'] = duration
            else:
                raise ValueError('Duration must be between 1 second and 1,209,600 seconds (2 weeks).')
        if reason is not MISSING:
            if len(reason) <= 500:
                _payload['data']['reason'] = reason
            else:
                raise ValueError('Reason is limited to a maximum of 500 characters.')
        route = Route('POST', 'moderation/bans', params)
        await self.request(route=route, json=_payload)

    async def unban_user(self, *, broadcaster_id: str, moderator_id: str, user_id: str) -> None:
        # Removes the ban or timeout that was placed on the specified user.
        params = {
            'broadcaster_id': broadcaster_id,
            'moderator_id': moderator_id,
            'user_id': user_id
        }
        route = Route('DELETE', 'moderation/bans', params)
        await self.request(route=route)

    # ---------------------------------
    #       + Channel Extension +
    # ---------------------------------
    async def get_user_extensions(self) -> List[ChannelTypes.Extension]:
        # Gets a list of all extensions (both active and inactive) that the broadcaster has installed.
        route = Route('GET', 'users/extensions/list')
        data = await self.request(route=route)
        return data['data']

    @staticmethod
    def _form_extension(data: Dict[str, Any]) -> ChannelTypes.Extensions:

        reformatted_data = {
            'panel': [],
            'overlay': [],
            'component': []
        }
        for section, items in data:
            for slot_number, item_info in items.items():
                item = {'slot_number': slot_number}
                item.update(item_info)
                reformatted_data[section].append(item)
        return reformatted_data

    async def get_user_active_extensions(self, *, user_id: str) -> ChannelTypes.Extensions:
        # Gets the active extensions that the broadcaster has installed for each configuration.
        params = {'user_id': user_id}
        route = Route('GET', 'users/extensions', params)
        data = await self.request(route=route)
        return self._form_extension(data=data['data'])

    async def update_user_extensions(self, section: str, slot: str, extension_id: str,
                                     extension_version: str, activate: bool,
                                     x: int = MISSING, y: int = MISSING) -> ChannelTypes.Extensions:
        # Updates an installed extension’s information.
        _payload = {
            'data': {section: {slot: {'id': extension_id,
                                      'version': extension_version,
                                      'active': activate}}}
        }
        if x and y:
            _payload[section][slot].update({'x': x, 'y': y})
        route = Route('PUT', 'users/extensions')
        data = await self.request(route=route, json=_payload)
        return self._form_extension(data=data['data'])

    # ---------------------------------
    #       + Channel Schedule +
    # ---------------------------------
    async def fetch_channel_stream_schedule(self, *, limit: int, broadcaster_id: str,
                                            segment_ids: List[str] = MISSING,
                                            start_time: datetime = MISSING
                                            ) -> AsyncGenerator[ChannelTypes.Schedule]:

        # Gets the broadcaster’s streaming schedule.
        params = {'broadcaster_id': broadcaster_id, 'first': '25'}
        if segment_ids is not MISSING:
            params['id'] = segment_ids
        if start_time is not MISSING:
            params['start_time'] = convert_to_pst_rfc3339(start_time)
        route = Route('GET', 'schedule', params)
        try:
            async for data in self._pagination_request(route=route, query_params=params, limit=limit):
                yield data
        except NotFound:
            return

    async def update_channel_schedule_settings(self, *, broadcaster_id: str, vacation: bool,
                                               timezone: str = MISSING,
                                               start_time: datetime = MISSING,
                                               end_time: datetime = MISSING) -> None:
        # Updates the broadcaster’s schedule settings, such as scheduling a vacation.
        params = {'broadcaster_id': broadcaster_id, 'is_vacation_enabled': vacation}
        if vacation:
            params['vacation_start_time'] = convert_to_pst_rfc3339(datetime.now())
            if start_time is not MISSING:
                params['vacation_start_time'] = convert_to_pst_rfc3339(start_time)
            if end_time is not MISSING:
                params['vacation_end_time'] = convert_to_pst_rfc3339(end_time)
            if timezone is not MISSING:
                params['timezone'] = timezone
        route = Route('PATCH', 'schedule/settings', params)
        await self.request(route=route)

    async def create_channel_stream_schedule_segment(self, *,
                                                     broadcaster_id: str,
                                                     timezone: str,
                                                     duration: int,
                                                     start_time: datetime = MISSING,
                                                     is_recurring: bool = MISSING,
                                                     category_id: str = MISSING,
                                                     title: str = MISSING) -> ChannelTypes.Schedule:
        # Adds a single or recurring broadcast to the broadcaster’s streaming schedule.
        params = {'broadcaster_id': broadcaster_id}
        _payload = {
            'timezone': timezone,
            'duration': duration,
            'title': title,
            'start_time': start_time,
            'is_recurring': is_recurring,
            'category_id': category_id
        }
        # Remove keys with MISSING values from the dictionary.
        _payload = {key: value for key, value in _payload.items() if value is not MISSING}
        route = Route('POST', 'schedule/segment', params)
        data = await self.request(route=route, json=_payload)
        return data['data'][0]

    async def update_channel_stream_schedule_segment(self, *, broadcaster_id: str, segment_id: str,
                                                     start_time: datetime = MISSING,
                                                     duration: int = MISSING,
                                                     category_id: str = MISSING,
                                                     title: str = MISSING,
                                                     timezone: str = MISSING,
                                                     is_canceled: bool = MISSING
                                                     ) -> ChannelTypes.ScheduleSegment:
        # Updates a scheduled broadcast segment.
        params = {'broadcaster_id': broadcaster_id, 'id': segment_id}
        _payload = {
            'duration': duration,
            'category_id': category_id,
            'title': title,
            'timezone': timezone,
            'is_canceled': is_canceled
        }
        # Remove keys with MISSING values from the dictionary.
        _payload = {key: value for key, value in _payload.items() if value is not MISSING}
        if start_time is not MISSING:
            _payload['start_time'] = convert_to_pst_rfc3339(start_time)
        route = Route('PATCH', 'schedule/segment', params)
        data = await self.request(route=route, json=_payload)
        return data['data']['segments'][0]

    async def delete_channel_stream_schedule_segment(self, *, broadcaster_id: str, segment_id: str) -> None:
        # Removes a broadcast segment from the broadcaster’s streaming schedule.
        params = {'broadcaster_id': broadcaster_id, 'id': segment_id}
        route = Route('DELETE', 'schedule/segment', params)
        await self.request(route=route)

    # --------------------------------
    #        + Channel Videos +
    # --------------------------------
    async def fetch_videos(self, *, limit: int,
                           video_ids: List[str] = EXCLUSIVE,
                           user_id: str = EXCLUSIVE,
                           category_id: str = EXCLUSIVE,
                           language: str = MISSING,
                           period: str = MISSING,
                           sort: str = MISSING,
                           videos_type: str = MISSING) -> AsyncGenerator[List[ChannelTypes.Video]]:
        # Gets information about one or more published videos.
        if not any(val is not EXCLUSIVE for val in [user_id, video_ids, category_id]):
            raise TypeError('Mutually exclusive options: user_id, video_ids, category_id.')
        params = {
            'id': video_ids,
            'sort': sort,
            'user_id': user_id,
            'game_id': category_id,
            'language': language,
            'period': period,
            'type': videos_type,
            'first': '100'
        }
        # Remove keys with MISSING values from the dictionary.
        params = {key: value for key, value in params.items() if (value is not MISSING or
                                                                  value is not EXCLUSIVE)}
        route = Route('GET', 'videos', params)
        async for data in self._pagination_request(limit=limit, route=route, query_params=params,
                                                   check_length=True):
            yield [item for item in data if item['id'] not in self._videos]

    async def delete_videos(self, *, video_ids: List[str]) -> List[str]:
        # Deletes one or more videos
        videos = [video for video in video_ids if video not in self._videos]
        params = {'id': videos}
        if len(videos) >= 1:
            try:
                route = Route('DELETE', 'videos', params)
                data = await self.request(route=route)
                # Caching deleted videos to prevent occasional appearances during video retrieval.
                self._videos.update(data['data'])
                return data['data']
            except Unauthorized as error:
                raise Unauthorized(message='Unauthorized or Video Not Found.') from error
        return []

    # -------------------------------
    #        + Channel Clips +
    # -------------------------------
    async def fetch_clips(self, *, limit: int,
                          is_featured: bool = MISSING,
                          broadcaster_id: str = EXCLUSIVE,
                          clip_ids: List[str] = EXCLUSIVE,
                          category_id: str = EXCLUSIVE,
                          started_at: datetime = MISSING,
                          ended_at: datetime = MISSING) -> AsyncGenerator[List[ChannelTypes.Clip]]:
        # Gets one or more video clips that were captured from streams
        if not any(val is not EXCLUSIVE for val in [broadcaster_id, clip_ids, category_id]):
            raise TypeError('Mutually exclusive options: broadcaster_id, clip_ids, category_id.')
        params = {'first': '100'}
        if broadcaster_id is not EXCLUSIVE:
            params['broadcaster_id'] = broadcaster_id
        if clip_ids is not EXCLUSIVE:
            if len(clip_ids) <= 100:
                params['id'] = clip_ids
            else:
                raise TypeError('The maximum number of clips you may specify is 100.')
        if category_id is not EXCLUSIVE:
            params['game_id'] = category_id
        if is_featured is not MISSING:
            params['is_featured'] = is_featured
        if started_at is not MISSING:
            params['started_at'] = convert_to_pst_rfc3339(started_at)
        if ended_at is not MISSING:
            params['ended_at'] = convert_to_pst_rfc3339(ended_at)
        route = Route('GET', 'clips', params)
        async for data in self._pagination_request(limit=limit, route=route, query_params=params,
                                                   check_length=True):
            yield data

    # ------------------------------
    #            + User +
    # ------------------------------
    async def get_users(self, *, user_ids: List[str] = MISSING,
                        user_names: List[str] = MISSING) -> List[UserTypes.User]:
        # Gets information about one or more users.
        params = {'id': [], 'login': []}
        if user_ids is not MISSING:
            params['id'] = user_ids
        if user_names is not MISSING:
            params['login'] = user_names
        if len(params['id']) + len(params['login']) > 100:
            raise TypeError('The maximum number of users you may specify is 100.')
        route = Route('GET', 'users', params)
        data = await self.request(route=route)
        return data['data']

    async def update_user(self, *, description: Optional[str]) -> UserTypes.User:
        # Updates the specified user’s information.
        params = {'description': ''}
        if isinstance(description, str):
            if len(description) > 300:
                raise ValueError('The description is limited to a maximum of 300 characters.')
            params['description'] = description
        route = Route('PUT', 'users', params)
        data = await self.request(route=route)
        return data['data'][0]

    async def check_user_subscription(self, *, broadcaster_id: str, user_id: str) \
            -> ChannelTypes.Subscription:
        params = {'broadcaster_id': broadcaster_id, 'user_id': user_id}
        route = Route('GET', 'subscriptions/user', params)
        data = await self.request(route=route)
        return data['data'][0]

    # -----------------------------
    #      + User Chat Color +
    # -----------------------------
    async def get_users_chat_color(self, *, user_ids: List[str]) -> List[str]:
        # Gets the color used for the user’s name in chat.
        colors = {
            '': 'random',  # If the user hasn’t specified a color in their settings, the string is empty.
            '#0000FF': 'blue',
            '#8A2BE2': 'blue_violet',
            '#5F9EA0': 'cadet_blue',
            '#D2691E': 'chocolate',
            '#FF7F50': 'coral',
            '#1E90FF': 'dodger_blue',
            '#B22222': 'firebrick',
            '#DAA520': 'golden_rod',
            '#008000': 'green',
            '#FF69B4': 'hot_pink',
            '#FF4500': 'orange_red',
            '#FF0000': 'red',
            '#2E8B57': 'sea_green',
            '#00FF7F': 'spring_green',
            '#9ACD32': 'yellow_green'}
        params = {'user_id': user_ids}
        if len(user_ids) > 100:
            raise TypeError('The maximum number of users you may specify is 100.')
        route = Route('GET', 'chat/color', params)
        data = await self.request(route=route)
        # Order colors by the ``users_id``.
        colors_organized = [
            next(colors.get(e['color'], e['color']) for e in data['data']
                 if e['user_id'] == u) for u in user_ids
        ]
        return colors_organized

    async def update_user_chat_color(self, *, user_id: str, color: str) -> None:
        # Updates the color used for the user’s name in chat.
        params = {'user_id': user_id, 'color': color}
        route = Route('PUT', 'chat/color', params)
        await self.request(route=route)

    # ----------------------------
    #       + User Whisper +
    # ----------------------------
    async def send_whisper(self, *, from_user_id: str, to_user_id: str, message: str) -> None:
        # Sends a whisper message to the specified user.
        params = {'from_user_id': from_user_id, 'to_user_id': to_user_id}
        _payload = {'message': message}
        route = Route('POST', 'whispers', params)
        await self.request(route=route, json=_payload)

    # ----------------------------
    #    + User Block/Unblock +
    # ----------------------------
    async def fetch_user_block_list(self, *, limit: int, broadcaster_id: str,
                                    ) -> AsyncGenerator[List[UserTypes.SpecificDisplayUser]]:
        # Gets the list of users that the broadcaster has blocked. Read More.
        params = {'broadcaster_id': broadcaster_id, 'first': '100'}
        route = Route('GET', 'users/blocks', params)
        async for data in self._pagination_request(limit=limit, route=route, query_params=params):
            yield data

    async def block_user(self, *, target_user_id: str,
                         source_context: str = MISSING, reason: str = MISSING) -> None:
        # Blocks the specified user from interacting with or having contact with the broadcaster.
        params = {'target_user_id': target_user_id}
        if source_context is not MISSING:
            params['source_context'] = source_context
        if reason is not MISSING:
            params['reason'] = reason
        route = Route('PUT', 'users/blocks', params)
        await self.request(route=route)

    async def unblock_user(self, *, target_user_id: str) -> None:
        # Removes the user from the broadcaster’s list of blocked users.
        params = {'target_user_id': target_user_id}
        route = Route('DELETE', 'users/blocks', params)
        await self.request(route=route)

    # ----------------------------
    #  + User Followed Channels +
    # ----------------------------
    async def fetch_followed_channels(self, *, limit: int, user_id: str, broadcaster_id: str = MISSING,
                                      ) -> AsyncGenerator[List[ChannelTypes.Followed]]:
        # Gets a list of broadcasters that the specified user follows.
        params = {'user_id': user_id, 'first': '100'}
        if broadcaster_id is not MISSING:
            params['broadcaster_id'] = broadcaster_id
        route = Route('GET', 'channels/followed', params)
        async for data in self._pagination_request(route=route, query_params=params, limit=limit):
            yield data

    async def fetch_followed_streams(self, *, limit: int, user_id: str
                                     ) -> AsyncGenerator[List[StreamTypes.Stream]]:
        # Gets the list of broadcasters that the user follows and that are streaming live.
        params = {'user_id': user_id, 'first': '100'}
        route = Route('GET', 'streams/followed', params)
        async for data in self._pagination_request(limit=limit, route=route, query_params=params):
            yield data

    # ----------------------------
    #          + Reward +
    # ----------------------------
    async def get_custom_rewards(self, *, broadcaster_id: str, only_manageable_rewards: bool,
                                 reward_ids: List[str] = MISSING) -> List[RewardTypes.Reward]:
        # Gets a list of custom rewards that the specified broadcaster created.
        params = {'broadcaster_id': broadcaster_id, 'only_manageable_rewards': only_manageable_rewards}
        if reward_ids is not MISSING:
            if len(reward_ids) > 100:
                raise TypeError('The maximum number of rewards you may specify is 100.')
            params['id'] = reward_ids
        route = Route('GET', 'channel_points/custom_rewards', params)
        data = await self.request(route=route)
        return data['data']

    async def create_custom_rewards(self, *, broadcaster_id: str, title: str, cost: int,
                                    is_enabled: bool = MISSING,
                                    background_color: str = MISSING,
                                    prompt: str = MISSING,
                                    is_user_input_required: bool = MISSING,
                                    should_redemptions_skip_request_queue: bool = MISSING,
                                    is_max_per_stream_enabled: bool = MISSING,
                                    max_per_stream: int = MISSING,
                                    is_max_per_user_per_stream_enabled: bool = MISSING,
                                    max_per_user_per_stream: int = MISSING,
                                    is_global_cooldown_enabled: bool = MISSING,
                                    global_cooldown_seconds: int = MISSING) -> RewardTypes.Reward:
        # Creates a Custom Reward in the broadcaster’s channel.
        params = {'broadcaster_id': broadcaster_id}
        if len(title) > 45:
            raise ValueError('The title may contain a maximum of 45 characters.')
        if cost < 1:
            raise ValueError('The cost of the reward, in Channel Points. The minimum is 1 point.')
        if prompt is not MISSING and len(prompt) > 200:
            raise ValueError('The prompt may contain a maximum of 200 characters.')
        _payload = {
            'title': title,
            'cost': cost,
            'is_enabled': is_enabled,
            'background_color': background_color,
            'prompt': prompt,
            'is_user_input_required': is_user_input_required,
            'should_redemptions_skip_request_queue': should_redemptions_skip_request_queue,
            'is_max_per_stream_enabled': is_max_per_stream_enabled,
            'max_per_stream': max_per_stream,
            'is_max_per_user_per_stream_enabled': is_max_per_user_per_stream_enabled,
            'max_per_user_per_stream': max_per_user_per_stream,
            'is_global_cooldown_enabled': is_global_cooldown_enabled,
            'global_cooldown_seconds': global_cooldown_seconds
        }
        # Remove keys with MISSING values from the dictionary.
        _payload = {key: value for key, value in _payload.items() if value is not MISSING}
        # Some keys requires enable fields.
        if is_max_per_stream_enabled is MISSING and isinstance(max_per_stream, int):
            if max_per_stream < 1:
                raise ValueError('The minimum value of max_per_stream is 1.')
            _payload['is_max_per_stream_enabled'] = True
        if is_max_per_user_per_stream_enabled is MISSING and isinstance(max_per_user_per_stream, int):
            if max_per_user_per_stream < 1:
                raise ValueError('The minimum value of max_per_user_per_stream is 1.')
            _payload['is_max_per_user_per_stream_enabled'] = True
        if is_global_cooldown_enabled is MISSING and isinstance(global_cooldown_seconds, int):
            if global_cooldown_seconds < 1 or global_cooldown_seconds > 604800:
                raise ValueError(
                    'The minimum value of global_cooldown_seconds is 1 and the maximum is 604800.'
                )
            _payload['is_global_cooldown_enabled'] = True
        route = Route('POST', 'channel_points/custom_rewards', params)
        data = await self.request(route=route, json=_payload)
        return data['data'][0]

    async def update_custom_rewards(self, *, broadcaster_id: str,
                                    reward_id: str,
                                    title: str = MISSING,
                                    cost: int = MISSING,
                                    is_enabled: bool = MISSING,
                                    is_paused: bool = MISSING,
                                    background_color: str = MISSING,
                                    prompt: str = MISSING,
                                    is_user_input_required: bool = MISSING,
                                    max_per_stream: Optional[int] = MISSING,
                                    max_per_user_per_stream: Optional[int] = MISSING,
                                    should_redemptions_skip_request_queue: bool = MISSING,
                                    global_cooldown_seconds: Optional[int] = MISSING) -> RewardTypes.Reward:
        # Updates a custom reward.
        params = {'broadcaster_id': broadcaster_id, 'id': reward_id}
        if title is not MISSING and len(title) > 45:
            raise ValueError('The title may contain a maximum of 45 characters.')
        if cost is not MISSING and cost < 1:
            raise ValueError('The cost of the reward, in Channel Points. The minimum is 1 point.')
        if prompt is not MISSING and len(prompt) > 200:
            raise ValueError('The prompt may contain a maximum of 200 characters.')
        _payload = {
            'title': title,
            'cost': cost,
            'is_enabled': is_enabled,
            'is_paused': is_paused,
            'background_color': background_color,
            'prompt': prompt,
            'is_user_input_required': is_user_input_required,
            'should_redemptions_skip_request_queue': should_redemptions_skip_request_queue,
            'is_max_per_stream_enabled': isinstance(max_per_stream, int),
            'max_per_stream': max_per_stream or MISSING,
            'is_max_per_user_per_stream_enabled': isinstance(max_per_user_per_stream, int),
            'max_per_user_per_stream': max_per_user_per_stream or MISSING,
            'is_global_cooldown_enabled': isinstance(global_cooldown_seconds, int),
            'global_cooldown_seconds': global_cooldown_seconds or MISSING
        }
        # Remove keys with MISSING values from the dictionary.
        _payload = {key: value for key, value in _payload.items() if value is not MISSING}
        route = Route('PATCH', 'channel_points/custom_rewards', params)
        data = await self.request(route=route, json=_payload)
        return data['data'][0]

    async def delete_custom_rewards(self, *, broadcaster_id: str, reward_id: str) -> None:
        # Deletes a custom reward that the broadcaster created.
        params = {'broadcaster_id': broadcaster_id, 'id': reward_id}
        route = Route('DELETE ', 'channel_points/custom_rewards', params)
        await self.request(route=route)

    # -----------------------------
    #    + Reward  Redemptions +
    # -----------------------------
    async def fetch_custom_reward_redemption(self, *, limit: int, broadcaster_id: str, recent: bool,
                                             reward_id: str,
                                             redemption_ids: List[str] = MISSING,
                                             status: str = MISSING
                                             ) -> AsyncGenerator[List[RewardTypes.Redemption]]:
        # Gets a list of redemptions for the specified custom reward.
        params = {'broadcaster_id': broadcaster_id,
                  'reward_id': reward_id,
                  'sort': ('NEWEST' if recent else 'OLDEST'),
                  'first': '50'}
        if status is MISSING and redemption_ids is MISSING:
            raise TypeError('Mutually exclusive options: status, redemption_ids.')
        if status is not MISSING:
            params['status'] = status
        if redemption_ids is not MISSING:
            if len(redemption_ids) > 50:
                raise TypeError('The maximum number of redemption you may specify is 50.')
            params['id'] = redemption_ids
        route = Route('GET', 'channel_points/custom_rewards/redemption', params)
        async for data in self._pagination_request(limit=limit, route=route, query_params=params):
            yield data

    async def update_redemption_status(self, *, broadcaster_id: str, reward_id: str, fulfill: bool,
                                       redemption_ids: List[str]) -> List[RewardTypes.Redemption]:
        # Updates a redemption’s status. You may update a redemption only if its status is UNFULFILLED.
        params = {'broadcaster_id': broadcaster_id, 'reward_id': reward_id, 'id': redemption_ids}
        _payload = {'status': 'FULFILLED' if fulfill else 'CANCELED'}
        route = Route('PATCH', 'channel_points/custom_rewards/redemptions', params)
        data = await self.request(route=route, json=_payload)
        return data['data']

    # -----------------------------
    #           + Polls +
    # -----------------------------
    async def fetch_polls(self, *, limit: int, broadcaster_id: str, poll_ids: List[str] = MISSING
                          ) -> AsyncGenerator[List[PollTypes.Poll]]:
        # Gets a list of polls that the broadcaster created.
        params = {'broadcaster_id': broadcaster_id, 'first': '20'}
        if poll_ids is not MISSING:
            if len(poll_ids) > 100:
                raise TypeError('The maximum number of poll you may specify is 100.')
            params['id'] = poll_ids
        route = Route('GET', 'polls', params)
        async for data in self._pagination_request(limit=limit, route=route, query_params=params):
            yield data

    async def create_poll(self, *, broadcaster_id: str, title: str, choices: List[str], duration: int,
                          points_per_vote: int = MISSING) -> PollTypes.Poll:
        # Creates a poll that viewers in the broadcaster’s channel can vote on.
        if len(title) > 60:
            raise ValueError('The title may contain a maximum of 60 characters.')
        if len(choices) < 2 or len(choices) > 5:
            raise ValueError('List must contain a minimum of 2 choices and up to a maximum of 5 choices.')
        if duration < 15 or duration > 1800:
            raise ValueError('The minimum is 15 seconds and the maximum is 1800 seconds (30 minutes).')

        _payload = {'broadcaster_id': broadcaster_id, 'title': title,
                    'choices': [{'title': choice} for choice in choices],
                    'duration': duration}
        if points_per_vote is not MISSING:
            if 1000000 >= points_per_vote >= 1:
                _payload['channel_points_voting_enabled'] = True
                _payload['channel_points_per_vote'] = points_per_vote
            else:
                raise ValueError('The minimum of points_per_vote is 1 and the maximum is 1000000.')
        route = Route('POST', 'polls')
        data = await self.request(route=route, json=_payload)
        return data['data'][0]

    async def end_poll(self, *, broadcaster_id: str, poll_id: str, archive: bool) -> PollTypes.Poll:
        # Ends an active poll. You have the option to end it or end it and archive it.
        _payload = {'broadcaster_id': broadcaster_id, 'id': poll_id,
                    'status': 'ARCHIVED' if archive else 'TERMINATED'}
        route = Route('PATCH', 'polls')
        data = await self.request(route=route, json=_payload)
        return data['data'][0]

    # -----------------------------
    #        + Predictions +
    # -----------------------------
    async def fetch_predictions(self, *, limit: int, broadcaster_id: str,
                                prediction_ids: List[str] = MISSING
                                ) -> AsyncGenerator[List[PredictionTypes.Prediction]]:
        # Gets a list of Channel Points Predictions that the broadcaster created.
        params = {'broadcaster_id': broadcaster_id}
        if prediction_ids is not MISSING:
            if len(prediction_ids) > 25:
                raise TypeError('The maximum number of predictions you may specify is 25.')
            params['id'] = prediction_ids
        route = Route('GET', 'predictions', params)
        async for data in self._pagination_request(limit=limit, route=route, query_params=params):
            yield data

    async def create_prediction(self, *, broadcaster_id: str, title: str, prediction_window: int,
                                outcomes: List[PredictionTypes.PredictionOutcomesTitle]
                                ) -> PredictionTypes.Prediction:
        # Creates a Channel Points Prediction.
        if len(title) > 45:
            raise ValueError('The title is limited to a maximum of 45 characters.')
        if len(outcomes) < 2 or len(outcomes) > 10:
            raise ValueError('List must contain a minimum of 2 outcomes and up to a maximum of 10 outcomes.')
        for outcome in outcomes:
            if len(outcome['title']) > 25:
                raise ValueError('The outcome title is limited to a maximum of 25 characters.')
        if prediction_window < 30 or prediction_window > 1800:
            raise ValueError('The minimum of duration is 30 seconds and the maximum is 1800 seconds')
        request_body = {'broadcaster_id': broadcaster_id, 'title': title,
                        'outcomes': outcomes, 'prediction_window': prediction_window}
        route = Route('POST', 'predictions')
        data = await self.request(route=route, json=request_body)
        return data['data']

    async def end_prediction(self, *, broadcaster_id: str, prediction_id: str, status: str,
                             winning_outcome_id: str = MISSING) -> PredictionTypes.Prediction:
        # Locks, resolves, or cancels a Channel Points Prediction.
        params = {'broadcaster_id': broadcaster_id, 'id': prediction_id, 'status': status}
        if winning_outcome_id is not MISSING:
            params['winning_outcome_id'] = winning_outcome_id
        route = Route('PATCH', 'predictions', params)
        data = await self.request(route=route)
        return data['data']

    # -----------------------------
    #          + Charity +
    # -----------------------------
    async def get_charity_campaigns(self, *, broadcaster_id: str) -> ChannelTypes.Charity:
        # Gets information about the charity campaign that a broadcaster is running
        params = {'broadcaster_id': broadcaster_id}
        route = Route('GET', 'charity/campaigns', params)
        data = await self.request(route=route)
        return data['data']

    async def fetch_charity_campaigns_donations(self, *, limit: int, broadcaster_id: str
                                                ) -> AsyncGenerator[List[ChannelTypes.CharityDonation]]:
        # Gets the list of donations that users have made to the broadcaster’s active charity campaign.
        params = {'broadcaster_id': broadcaster_id, 'first': '100'}
        route = Route('GET', 'charity/donations', params)
        async for data in self._pagination_request(limit=limit, route=route, query_params=params):
            yield data

    # ---------------------------
    #    + Channel Followers +
    # ---------------------------
    async def fetch_channel_followers(self, *, limit: int, broadcaster_id: str,
                                      user_id: str = MISSING) -> AsyncGenerator[List[ChannelTypes.Follower]]:
        # Gets a list of users that follow the specified broadcaster.
        params = {'broadcaster_id': broadcaster_id, 'first': '100'}
        if user_id is not MISSING:
            params['user_id'] = user_id
        route = Route('GET', 'channels/followers', params)
        async for data in self._pagination_request(limit=limit, route=route, query_params=params):
            yield data

    async def get_channel_total_followers(self, *, broadcaster_id: str) -> int:
        # Gets the total number of users that follow the broadcaster.
        params = {'broadcaster_id': broadcaster_id, 'first': '1'}
        route = Route('GET', 'channels/followers', params)
        data = await self.request(route=route)
        return data['total']

    # ---------------------------
    #  + Channel Subscriptions +
    # ---------------------------
    async def fetch_broadcaster_subscriptions(self, *, limit: int, broadcaster_id: str,
                                              user_ids: List[str] = MISSING) \
            -> AsyncGenerator[List[ChannelTypes.Subscription]]:
        # Gets a list of users that follow the specified broadcaster.
        params = {'broadcaster_id': broadcaster_id, 'first': '100'}
        if user_ids is not MISSING:
            if len(user_ids) > 100:
                raise TypeError('The maximum number of users you may specify is 100.')
            params['user_id'] = user_ids
        route = Route('GET', 'subscriptions', params)
        async for data in self._pagination_request(limit=limit, route=route, query_params=params,
                                                   check_length=True):
            yield data

    async def get_total_broadcaster_subscriptions(self, *, broadcaster_id: str) -> Tuple[int, int]:
        # Gets the total number of subscriptions with points.
        params = {'broadcaster_id': broadcaster_id, 'first': '1'}
        route = Route('GET', 'subscriptions', params)
        data = await self.request(route=route)
        return data['total'], data['points']


class Server:
    """Serves as an HTTP server responsible for user authorization."""
    __slots__ = ('host', 'port', 'app', 'event', '__state', '__code')

    def __init__(self, port: int):
        self.host: str = 'localhost'
        self.port: int = port
        self.app: web.Application = aiohttp.web.Application()
        self.event: asyncio.Event = asyncio.Event()
        self.app['runner']: Optional[web.AppRunner] = None
        self.app.router.add_get('/', self.handle_request)
        self.__state: Optional[str] = None
        self.__code: Optional[str] = None

    async def __aenter__(self) -> Server:
        """
        Method to be called when entering the async with block.
        """
        self.__state = generate_random_text()
        await self.start_server()
        return self

    async def start_server(self):
        """
        This method sets up the server.
        """
        runner = web.AppRunner(self.app)
        self.app['runner'] = runner
        await runner.setup()
        site = web.TCPSite(runner, self.host, self.port)
        _logger.debug('Starting the authorization server.')
        await site.start()
        _logger.debug('Server is now running on %s', self.uri)

    def url(self, client_id: str, scopes: HttpTypes.Scopes, force_verify: bool) -> str:
        """Get the authorization URL."""
        # Default scope
        if 'user:read:email' not in scopes:
            scopes.append('user:read:email')
        # Removing duplicates.
        scopes = list(dict.fromkeys(scopes))
        encoded_scope = '+'.join(urllib.parse.quote(s) for s in scopes)
        url = f'https://id.twitch.tv/oauth2/authorize?response_type=code&client_id={client_id}' \
              f'&force_verify={force_verify}&redirect_uri={self.uri}&scope={encoded_scope}' \
              f'&state={self.__state}'
        return url

    @property
    def uri(self) -> str:
        """Get the URI of the server."""
        return f'http://{self.host}:{self.port}'

    async def wait_for_code(self) -> str:
        """
        This method waits for the 'event' to be set
        indicating that the authorization code has been received.
        """
        await self.event.wait()
        return self.__code

    async def handle_request(self, request: web.Request) -> web.Response:
        """
        This method handles the incoming request from Twitch during the authorization process.
        """
        _logger.debug('Received request to URL: %s', request.rel_url)
        query_params = request.query
        if (query_params.get('code') or query_params.get('error')) \
                and self.__state == query_params.get('state'):
            if query_params.get('code'):
                self.__code = query_params.get('code')
                self.event.set()
                html = f'''
                    <html>
                        <body>
                            <h1>Redirect Completed</h1>
                            <p><a href="{__github__}">Twitchify</a> Version: {__version__}</p>
                            <p>You can now close this page.</p>
                        </body>
                    </html>
                    '''
                return web.Response(
                    text=html,
                    content_type='text/html'
                )
            if query_params.get('error'):
                error_description = query_params.get('error_description')
                return web.Response(status=403, text=error_description.replace('+', ' '))
        return web.Response(status=403, text='')

    async def __aexit__(self, exc_type: Optional[Type[BaseException]],
                        exc_value: Optional[BaseException],
                        traceback: Optional[TracebackType]) -> None:
        """
        Method to be called when exiting the async with block.

        This method performs the cleanup tasks when exiting the async with block,
        ensuring that the server is closed gracefully.
        """
        if self.app['runner'] is not None:
            _logger.debug('Shutting down the authorization server.')
            await self.app['runner'].cleanup()
