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

from .errors import (TwitchServerError, BadRequest, Unauthorized, Forbidden,
                     HTTPException, NotFound, SessionClosed)
from . import __version__, __github__
from .utils import format_seconds, generate_random_state

from aiohttp import ClientSession, helpers, web
from asyncio import Lock, sleep, Task
from json import JSONDecodeError
from time import time
import urllib.parse
import asyncio

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Optional, List, Callable, Any, Type, Tuple
    from .types.eventsub.subscriptions import SubscriptionInfo
    from aiohttp import ClientWebSocketResponse
    from .types.http import Validate, Token, ScopesType
    from .types.channel import Channel
    from .types.stream import Stream
    from .types.user import UserType
    from types import TracebackType
    from typing import Type

import logging
_logger = logging.getLogger(__name__)

__all__ = ('HTTPClient', 'Server')


class Route:
    """
    Initialize a Route object.
    """
    BASE_ROUTE: str = 'https://api.twitch.tv/helix/'

    __slots__ = ('method', 'url')

    def __init__(self, method: str, path: Optional[str] = None, url: Optional[str] = None) -> None:
        self.method: str = method
        if path is None and url is None:
            raise TypeError
        else:
            if url is not None:
                self.url = url
            else:
                self.url = self.BASE_ROUTE + path

    def __repr__(self) -> str:
        return f'<Route method={self.method} url={self.url}>'


class HTTPClient:
    """Serves as an HTTP client responsible for sending HTTP requests to the Twitch API."""
    __slots__ = ('_dispatch', '_client_id', '_client_secret', '__session', '_session_lock',
                 '_user_agent', '_refresh_token', 'cli')

    def __init__(self, dispatcher: Callable[..., Any], client_id: str, secret_secret: Optional[str]) -> None:
        self._dispatch: Callable[[str, Any, Any], Task] = dispatcher
        self._client_id: str = client_id
        self._client_secret: str = secret_secret
        self.__session: Optional[ClientSession] = None
        self._session_lock: Lock = Lock()
        self._user_agent: str = f'Twitchify/{__version__} (GitHub: {__github__})'
        self._refresh_token: Optional[str] = None
        # Twitch CLI.
        self.cli: Optional[str] = None

    @property
    def is_open(self) -> bool:
        """
        Checks if the HTTP session is open.
        """
        return self.__session is not None and not self.__session.closed

    async def _open(self, *, access_token: Optional[str] = None) -> None:
        """
        Opens an HTTP session.
        """
        async with self._session_lock:
            if not self.is_open:
                headers = {
                    'Client-ID': self._client_id,
                    'Content-Type': 'application/json'
                }
                if access_token:
                    headers.update({'Authorization': f'Bearer {access_token}'})
                self.__session = ClientSession(headers=headers)
                _logger.debug('New HTTP session has been created.')

    async def close(self) -> bool:
        """
        Closes the HTTP session.
        """
        async with self._session_lock:
            if self.is_open:
                await self.__session.close()
                self.__session = None
                _logger.debug('HTTP session has been closed.')
        return not self.is_open

    async def open_session(self, token: str, refresh_token: Optional[str] = None) -> Validate:
        """
        Verifies the access token and opens a new session with it.
        """
        # Opening a session.
        if self.is_open:
            self.__session.headers.update({'Authorization': f'Bearer {token}'})
        else:
            await self._open(access_token=token)
        self._refresh_token = refresh_token
        validation: Validate = await self._validate_token(generate=True)
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
        HTTP request base.
        """
        method = route.method
        url = route.url
        for retry_count in range(1, 4):
            try:
                async with self.__session.request(method, url, **kwargs) as response:
                    if response.status in [200, 202]:
                        return await response.json()
                    if response.status == 400:
                        raise BadRequest
                    elif response.status == 401:
                        raise Unauthorized
                    elif response.status == 403:
                        try:
                            error = await response.json()
                            if error.get('message'):
                                raise Forbidden(message=error['message'])
                        except JSONDecodeError:
                            pass
                        raise Forbidden
                    elif response.status == 404:
                        raise NotFound
                    elif 500 <= response.status < 600:
                        raise TwitchServerError
                    raise HTTPException
            except OSError as exc:
                if 3 >= retry_count:
                    _logger.info('Request failed: %s. Retrying in %s seconds...',
                                 Route, (5 * retry_count))
                    await sleep(5 * retry_count)
                raise HTTPException from exc

    async def _generate_token(self) -> Optional[Token]:
        """
        Generate a new access token using client_secret and refresh_token.
        """
        if self._refresh_token and self._client_secret:
            # There is a chance that both the task and the normal
            # request can refresh the token at the same time.
            if not self._session_lock.locked():
                async with self._session_lock:
                    # Encoding the client secret.
                    encoded_secret = helpers.quote(self._refresh_token)
                    params = {'grant_type': 'refresh_token',
                              'refresh_token': encoded_secret,
                              'client_id': self._client_id,
                              'client_secret': self._client_secret}
                    _logger.debug('Generating a new access token to refresh the existing one.')
                    route = Route(method='POST', url='https://id.twitch.tv/oauth2/token')
                    refresh: Token = await self.request(route=route, params=params)
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
        token: Token = await self.request(route=route, params=params)
        return token['access_token'], token['refresh_token']

    async def _validate_token(self, *, generate: bool = False) -> Validate:
        """
        Validate access token.
        """
        while True:
            try:
                route = Route(method='GET', url='https://id.twitch.tv/oauth2/validate')
                validation: Validate = await self._request(route=route)
                _logger.debug('Access token successfully validated.')
                return validation
            except Unauthorized as exc:
                if generate and (self._client_secret and self._refresh_token):
                    try:
                        # Generating a new access token.
                        await self._generate_token()
                        continue
                    except (BadRequest, Forbidden):
                        raise Unauthorized(message='Invalid refresh token or client secret.') from exc
                else:
                    raise

    async def refresher(self, *, expires_in: int) -> None:
        """
        Refresher task to refresh the current access token.
        """
        start_time = time()
        # If the refresh_token or client_secret is missing,
        if self._refresh_token and self._client_secret:
            _logger.debug('A new token will be generated in %s.', format_seconds(expires_in - 300))
        else:
            # Set expires_in to a default value of 3540 seconds (59 minutes).
            expires_in = 3540 + 300
            _logger.warning('Access token will expire in %s,'
                            ' and won\'t be generated without the refresh token or client secret.',
                            format_seconds(expires_in - 300))
        while True:
            # Create a new access token approximately 5 minutes before the
            # current token's expiration.
            await sleep(min((expires_in - 300), 3540))
            current_time = time()
            elapsed_time = current_time - start_time
            try:
                if elapsed_time >= expires_in - 300:
                    # Reset the refresh token timer
                    start_time = time()
                    await self._generate_token()
                    _logger.debug('A new token will be generated in %s.',
                                  format_seconds(expires_in - 300))
                # ==> Validating the access token <==
                validation: Validate = await self._validate_token()
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
            except Unauthorized:
                try:
                    _logger.error('Unable to make the request to URL: %s Unauthorized access.',
                                  route.url)
                    await self._validate_token(generate=True)
                    continue
                except (Unauthorized, BadRequest):
                    raise

    async def subscribe(self, *, user_id: str, session_id: str,
                        subscriptions: List[SubscriptionInfo]) -> None:
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
                    route = Route(method='POST', path='eventsub/subscriptions')
                await self.request(route=route, json=data)
            except (Forbidden, BadRequest) as error:
                if isinstance(error, Forbidden):
                    _logger.error('Subscription type `%s` version `%s` is missing scope `%s`.',
                                  subscription['name'], subscription['version'], subscription['scope'])
                if isinstance(error, BadRequest):
                    _logger.warning('Subscription type `%s` version `%s` unsupported.',
                                    subscription['name'], subscription['version'])
        self._dispatch('ready')

    async def get_client(self) -> UserType:
        """
        Retrieves the broadcaster with the associated access token.
        """
        data = await self.request(route=Route(method='GET', path='users'))
        return data['data'][0]

    async def get_channel(self, broadcaster_id: str) -> Channel:
        """
        Retrieves the channel information.
        """
        _route = Route(method='GET', path=f'channels?broadcaster_id={broadcaster_id}')
        data = await self.request(route=_route)
        return data['data'][0]

    async def get_stream(self, user_id: str) -> Optional[Stream]:
        """
        Retrieves the stream.
        """
        try:
            _route = Route(method='GET', path=f'streams?user_id={user_id}')
            data = await self.request(route=_route)
            if len(data['data']) == 1:
                return data['data'][0]
        except NotFound:
            pass
        return None


class Server:
    """Serves as an HTTP server responsible for user authorization."""
    __slots__ = ('host', 'port', 'app', 'event', '__state', '__code')

    def __init__(self, port: int):
        self.host: str = 'localhost'
        self.port: int = port
        self.app: web.Application = web.Application()
        self.event: asyncio.Event = asyncio.Event()
        self.app['runner']: Optional[web.AppRunner] = None
        self.app.router.add_get('/', self.handle_request)
        self.__state: Optional[str] = None
        self.__code: Optional[str] = None

    async def __aenter__(self) -> 'Server':
        """
        Method to be called when entering the async with block.
        """
        self.__state = generate_random_state()
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

    def url(self, client_id: str, scopes: ScopesType, force_verify: bool = True) -> str:
        """Get the authorization URL."""
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
