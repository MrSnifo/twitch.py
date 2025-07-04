"""
The MIT License (MIT)

Copyright (c) 2025-present Snifo

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

from .user import User, Broadcaster, ClientUser
from typing import TYPE_CHECKING, overload
from .errors import UnregisteredUser
from .utils import datetime_to_str
import datetime
import weakref
import asyncio

if TYPE_CHECKING:
    from .types import Data, TTMData, users, Edata, chat, channels, search, PData, streams, bits, analytics, eventsub
    from typing import List, Tuple, Literal, Callable, Any, Optional, Dict, AsyncGenerator
    from .types.eventsub import MPData
    from .http import HTTPClient

import logging
_logger = logging.getLogger(__name__)

__all__ = ('ConnectionState',)


class ConnectionState:
    """
    Represents the state of the connection.
    """
    __slots__ = ('http', 'user', 'is_live', '__dispatch', '__custom_dispatch', '_return_full_data',
                 '_events', 'ready', 'total_cost', 'max_total_cost', '_users', '_socket_debug', '_broadcasters',
                 '_lock')

    def __init__(self,
                 dispatcher: Callable[..., Any],
                 custom_dispatch: Callable[..., Any],
                 http: HTTPClient,
                 socket_debug: bool,
                 return_full_data: bool) -> None:
        self.http: HTTPClient = http
        # Client User-related attributes
        self.user: Optional[ClientUser] = None
        self.is_live: Optional[bool] = None
        # Callbacks for dispatching events
        self.__dispatch: Callable[..., Any] = dispatcher
        self.__custom_dispatch: Callable[..., Any] = custom_dispatch
        self._return_full_data: bool = return_full_data
        # Event management
        self._events: Dict[str, Any] = {}
        self.ready: Optional[asyncio.Event] = None
        # Cost tracking
        self.total_cost: Optional[int] = None
        self.max_total_cost: Optional[int] = None
        # User management
        self._users: weakref.WeakValueDictionary[str, User] = weakref.WeakValueDictionary()
        self._broadcasters: Dict[str, Broadcaster] = {}
        # Debug and synchronization
        self._socket_debug: bool = socket_debug
        self._lock = asyncio.Lock()

    def clear(self) -> None:
        """Clears the state of the client by resetting attributes."""
        if self.ready is not None:
            self.ready.clear()
        self.user: Optional[ClientUser] = None
        self.is_live: Optional[bool] = None
        self._events: Dict[str, Any] = {}
        self._users: weakref.WeakValueDictionary[str, User] = weakref.WeakValueDictionary()
        self._broadcasters: Dict[str, Broadcaster] = {}

    def get_broadcasters(self) -> List[Broadcaster]:
        """Retrieves all broadcasters"""
        # Insure the broadcaster tokens exists.
        for user_id, broadcaster in self._broadcasters.items():
            if self.http.get_token(user_id):
                continue
            self.remove_user(user_id)

        return list(self._broadcasters.values())

    async def get_broadcaster(self, user_id: str) -> Broadcaster:
        """Retrieve a broadcaster with a given user_id, ensuring the user is authorized."""
        broadcaster = self._broadcasters.get(user_id)
        if self.http.get_token(user_id):
            if broadcaster is not None:
                return broadcaster

        await self.remove_user(user_id)
        raise UnregisteredUser('User %s is not registered. '
                               'Please register the user using `register_user`.' % user_id)

    def is_registered(self, user_id: str) -> bool:
        """checks the user is registered and authorized."""
        return self.http.get_token(user_id) is not None

    async def register_user(self,
                            access_token: Optional[str] = None,
                            refresh_token: Optional[str] = None) -> Broadcaster:
        """Registers a new user by initializing authorization and creating a broadcaster instance."""
        async with self._lock:
            data: users.OAuthToken = await self.http.initialize_authorization(access_token, refresh_token)
            self._broadcasters[data['user_id']] = Broadcaster(data['user_id'], state=self)
            self.user_register(self._broadcasters[data['user_id']])
            _logger.debug('Registered successfully. Broadcaster created for user_id: %s',
                          data['user_id'])

        return self._broadcasters[data['user_id']]

    async def remove_user(self, user_id: str) -> None:
        """Removes a registered user with its token if exists."""
        async with self._lock:
            if self._broadcasters.get(user_id):
                self._broadcasters.pop(user_id)

            if self.is_registered(user_id):
                self.http.remove_token(user_id)
                _logger.debug('Unregistered successfully. Broadcaster removed for user_id: %s', user_id)

    async def initialize_client(self, user_id: str) -> None:
        """Initializes the client with user and channel information and checks if the user is live."""
        user_data: Data[List[users.User]] = await self.http.get_users(user_id, [user_id])
        channel_data: Data[List[channels.ChannelInfo]] = await self.http.get_channel_information(user_id,
                                                                                                 [user_id])

        self.user = ClientUser(state=self, user_data=user_data['data'][0], channel_data=channel_data['data'][0])
        self._broadcasters[user_id] = self.user

        # Checks if User is Streaming.
        data: Optional[streams.StreamInfo] = await self.user.channel.stream.get_live()
        self.is_live = True if data is not None else False

    async def create_subscription(self,
                                  user_id: str,
                                  event: str,
                                  session_id: str,
                                  *,
                                  callbacks: Optional[List[Callable[..., Any]]] = None,
                                  condition_options: Optional[Dict[str, Any]] = None) -> None:
        """Creates a subscription for the given event and user, and manages event callbacks."""
        subscription: Optional[Dict[str, Any]] = self.http.get_subscription_info(event)

        if callbacks is not None and subscription is None:
            raise TypeError(f'Unknown event: `on_{event}` is not a recognized event.')

        if subscription is not None:
            async with self._lock:
                if self._events.setdefault(user_id, {}).get(subscription['name']) is None:
                    if condition_options:
                        subscription.update(subscription['name'])

                    data: TTMData[List[users.EventSubSubscription]] = await self.http.create_subscription(
                        self.user.id,
                        self.user.id,
                        user_id,
                        session_id,
                        subscription_type=subscription['name'],
                        subscription_version=subscription['version'],
                        subscription_condition=subscription['condition']
                    )
                    self._events[user_id][data['data'][0]['type'], subscription['version']] = {
                        'id': data['data'][0]['id'],
                        'name': event,
                        'version': subscription['version'],
                        'condition_options': condition_options,
                        'callbacks': callbacks if callbacks is not None else [],
                        'auth_user_id': self.user.id
                    }
                    self.total_cost = data['total_cost']
                    self.max_total_cost = data['max_total_cost']

                    if data['total_cost'] >= 0.85 * data['max_total_cost']:
                        _logger.warning('Total cost is getting high (%s). '
                                        'Consider unsubscribing from some events.',
                                        data['total_cost'])
                else:
                    self._events[user_id][subscription['name']]['callbacks'] = list(dict.fromkeys(
                        self._events[user_id][subscription['name']]['callbacks'] + callbacks
                    ))

    async def remove_subscription(self, user_id: str, event: str) -> None:
        """Removes a subscription for the given event and user."""
        subscription: Optional[Dict[str, str]] = self.http.get_subscription_info(event)
        if subscription is not None:
            async with self._lock:
                if self._events.setdefault(user_id, {}).get(subscription['name']) is not None:
                    await self.http.delete_subscription(
                        self._events[user_id]['auth_user_id'],
                        self._events[user_id][subscription['name'], subscription['version']]['id']
                    )
                    self._events[user_id].pop(subscription['name'], subscription['version'])
                    if self.user.id == user_id and event in ['channel_update',
                                                             'user_update',
                                                             'stream_online',
                                                             'stream_offline']:
                        _logger.warning('Default client event `%s` removed. Unexpected behavior may occur.',
                                        event)

    def get_user(self, __id: str, /) -> User:
        try:
            return self._users[__id]
        except KeyError:
            user = User(__id, self.user.id, state=self)
            self._users[__id] = user
            return user

    async def get_users(self,
                        user_ids: Optional[List[str]] = None,
                        user_logins: Optional[List[str]] = None) -> List[User]:
        _users = []
        if user_ids is not None:
            _users = [self.get_user(user_id) for user_id in user_ids]

        if user_logins is not None and len(user_logins) >= 1:
            data: Data[List[users.User]] = await self.http.get_users(self.user.id, user_logins=user_logins)
            return [self.get_user(user['id']) for user in data['data']] + _users

        return _users

    async def get_users_chat_color(self, __users: List[User], /) -> List[chat.UserChatColor]:
        data: Data[List[chat.UserChatColor]] = await self.http.get_user_chat_color(self.user.id,
                                                                                   [u.id for u in __users])
        return data['data']

    @overload
    async def get_team_info(self,
                            team_name: Optional[str] = None,
                            team_id: Optional[str] = None) -> channels.Team:
        ...

    @overload
    async def get_team_info(self,
                            team_name: Optional[str] = None,
                            team_id: Optional[str] = None) -> None:
        ...

    async def get_team_info(self,
                            team_name: Optional[str] = None,
                            team_id: Optional[str] = None) -> Optional[channels.Team]:
        data: Data[List[channels.Team]] = await self.http.get_team_info(self.user.id, team_name, team_id)
        return data['data'][0]

    async def get_global_emotes(self) -> Tuple[List[chat.Emote], str]:
        data: Edata[List[chat.Emote]] = await self.http.get_global_emotes(self.user.id)
        return data['data'], data['template']

    async def get_emote_sets(self, emote_set_ids: List[str]) -> Tuple[List[chat.Emote], str]:
        data: Edata[List[chat.Emote]] = await self.http.get_emote_sets(self.user.id, emote_set_ids)
        return data['data'], data['template']

    async def get_global_chat_badges(self) -> List[chat.Badge]:
        data: Data[List[chat.Badge]] = await self.http.get_global_chat_badges(self.user.id)
        return data['data']

    async def get_global_cheermotes(self) -> List[bits.Cheermote]:
        data: Data[List[bits.Cheermote]] = await self.http.get_cheermotes(self.user.id)
        return data['data']

    async def fetch_channels_search(self,
                                    query: str,
                                    live_only: bool = False,
                                    first: int = 20) -> AsyncGenerator[List[search.ChannelSearch], None]:
        kwargs: Dict[str, Any] = {
            'query': query,
            'live_only': live_only,
            'first': first,
            'after': None
        }
        while True:
            data: PData[List[search.ChannelSearch]] = await self.http.search_channels(self.user.id, **kwargs)
            yield data['data']
            kwargs['after'] = data['pagination'].get('cursor')
            if not kwargs['after']:
                break

    async def fetch_streams(self,
                            user_logins: Optional[List[str]] = None,
                            user_ids: Optional[List[str]] = None,
                            game_ids: Optional[List[str]] = None,
                            stream_type: Literal['all', 'live'] = 'all',
                            language: Optional[str] = None,
                            first: int = 20) -> AsyncGenerator[List[streams.StreamInfo], None]:
        kwargs: Dict[str, Any] = {
            'user_ids': user_ids,
            'user_logins': user_logins,
            'game_ids': game_ids,
            'stream_type': stream_type,
            'language': language,
            'first': first,
            'after': None
        }
        while True:
            data: PData[List[streams.StreamInfo]] = await self.http.get_streams(self.user.id, **kwargs)
            yield data['data']
            kwargs['after'] = data['pagination'].get('cursor')
            if not kwargs['after']:
                break

    async def fetch_videos(self,
                           game_id: Optional[str] = None,
                           video_ids: Optional[List[str]] = None,
                           language: Optional[str] = None,
                           period: Optional[Literal['all', 'day', 'month', 'week']] = None,
                           sort: Optional[Literal['time', 'trending', 'views']] = None,
                           video_type: Optional[Literal['all', 'archive', 'highlight', 'upload']] = None,
                           first: Optional[int] = 20) -> AsyncGenerator[List[channels.Video], None]:
        kwargs: Dict[str, Any] = {
            'video_ids': video_ids,
            'game_id': game_id,
            'language': language,
            'period': period,
            'sort': sort,
            'type': video_type,
            'first': first,
            'after': None
        }
        while True:
            data: PData[List[channels.Video]] = await self.http.get_videos(self.user.id, **kwargs)
            yield data['data']
            kwargs['after'] = data['pagination'].get('cursor')
            if not kwargs['after']:
                break

    async def fetch_clips(self,
                          game_id: Optional[str] = None,
                          clip_ids: Optional[List[str]] = None,
                          started_at: Optional[str] = None,
                          ended_at: Optional[str] = None,
                          is_featured: Optional[bool] = None,
                          first: int = 20) -> AsyncGenerator[List[channels.Clip], None]:
        kwargs: Dict[str, Any] = {
            'game_id': game_id,
            'clip_ids': clip_ids,
            'started_at': datetime_to_str(started_at),
            'ended_at': datetime_to_str(ended_at),
            'first': first,
            'is_featured': is_featured,
            'after': None
        }
        while True:
            data: PData[List[channels.Clip]] = await self.http.get_clips(self.user.id, **kwargs)
            yield data['data']
            kwargs['after'] = data['pagination'].get('cursor')
            if not kwargs['after']:
                break

    async def get_content_classification_labels(self, locale: streams.Locale = 'en-US') -> List[streams.CCLInfo]:
        data: Data[List[streams.CCLInfo]] = await self.http.get_content_classification_labels(self.user.id, locale)
        return data['data']

    async def fetch_top_games(self, first: int = 20) -> AsyncGenerator[List[search.Game], None]:
        kwargs: Dict[str, Any] = {
            'first': first,
            'after': None
        }
        while True:
            data: PData[List[search.Game]] = await self.http.get_top_games(self.user.id, **kwargs)
            yield data['data']
            kwargs['after'] = data['pagination'].get('cursor')
            if not kwargs['after']:
                break

    async def fetch_categories_search(self,
                                      query: str,
                                      first: int = 20) -> AsyncGenerator[List[search.CategorySearch], None]:
        kwargs: Dict[str, Any] = {
            'query': query,
            'first': first,
            'after': None
        }
        while True:
            data: PData[List[search.CategorySearch]] = await self.http.search_categories(self.user.id, **kwargs)
            yield data['data']
            kwargs['after'] = data['pagination'].get('cursor')
            if not kwargs['after']:
                break

    async def get_games(self,
                        game_ids: Optional[List[str]] = None,
                        game_names: Optional[List[str]] = None,
                        igdb_ids: Optional[List[str]] = None) -> List[search.Game]:
        data: Data[List[search.Game]] = await self.http.get_games(self.user.id, game_ids, game_names, igdb_ids)
        return data['data']

    async def fetch_extension_analytics(self,
                                        extension_id: Optional[str] = None,
                                        analytics_type: Literal['overview_v2'] = 'overview_v2',
                                        started_at: Optional[datetime.datetime] = None,
                                        ended_at: Optional[datetime.datetime] = None,
                                        first: int = 20) -> AsyncGenerator[List[analytics.Extension], None]:
        kwargs: Dict[str, Any] = {
            'extension_id': extension_id,
            'analytics_type': analytics_type,
            'started_at': datetime_to_str(started_at),
            'ended_at': datetime_to_str(ended_at),
            'first': first,
            'after': None
        }
        while True:
            data: PData[List[analytics.Extension]] = await self.http.get_extension_analytics(self.user.id, **kwargs)
            yield data['data']
            kwargs['after'] = data['pagination'].get('cursor')
            if not kwargs['after']:
                break

    async def fetch_game_analytics(self,
                                   game_id: Optional[str] = None,
                                   analytics_type: Literal['overview_v2'] = 'overview_v2',
                                   started_at: Optional[datetime.datetime] = None,
                                   ended_at: Optional[datetime.datetime] = None,
                                   first: int = 20) -> AsyncGenerator[List[analytics.Game], None]:
        kwargs: Dict[str, Any] = {
            'game_id': game_id,
            'analytics_type': analytics_type,
            'started_at': datetime_to_str(started_at),
            'ended_at': datetime_to_str(ended_at),
            'first': first,
            'after': None
        }
        while True:
            data: PData[List[analytics.Game]] = await self.http.get_game_analytics(self.user.id, **kwargs)
            yield data['data']
            kwargs['after'] = data['pagination'].get('cursor')
            if not kwargs['after']:
                break

    async def initialize_after_disconnect(self, session_id: str) -> None:
        _logger.debug('Initiating re-subscription process after disconnection for session ID: %s',
                      session_id)

        # Keeps the client updated.
        await self.initialize_client(self.user.id)

        events = self._events.copy()
        self._events = {}

        for user_id, events in events.items():
            for event_type, event_details in events.items():
                try:
                    await self.create_subscription(user_id,
                                                   event_details['name'],
                                                   session_id,
                                                   callbacks=event_details['callbacks'],
                                                   condition_options=event_details['condition_options'])
                except Exception as exc:
                    _logger.exception('Error processing event `on_%s`: %s',
                                      event_details['name'],
                                      str(exc))

    def ws_connect(self) -> None:
        self.__dispatch('connect')

    def state_ready(self) -> None:
        self.ready.set()
        self.__dispatch('ready')

    def ws_disconnect(self) -> None:
        self.ready.clear()
        self.__dispatch('disconnect')

    async def socket_raw_receive(self, data: Any):
        if self._socket_debug:
            self.__dispatch('socket_raw_receive', data)

    def user_register(self, broadcaster: Broadcaster) -> None:
        self.__dispatch('user_register', broadcaster)

    def parse(self, data: MPData[Any]) -> None:
        try:
            subscription = data['payload']['subscription']
            conditions = subscription['condition']
            user_id = conditions.get('broadcaster_user_id') or conditions.get('to_broadcaster_user_id')

            version = subscription['version']

            event = self._events.get(user_id, {}).get((subscription['type'], subscription['version']))

            # Incase Using CLI.
            if event is not None:
                for callback in event['callbacks']:
                    self.__custom_dispatch(event['name'], callback,  data['payload']['event'])

                # Dispatch only custom events incase the user is not the client.
                if user_id != self.user.id:
                    return

            event_type = subscription['type'].replace('.', '_')
            key = "%s_v%s" % (event_type, version)

            # Client events
            parse = getattr(self, 'parse_' +  key)
            parse(data)
        except Exception as error:
            _logger.exception('Failed to parse event: %s', error)


    def _dispatcher(self, event: str, data: MPData[Any]) -> None:
        if not self._return_full_data:
            self.__dispatch(event, data['payload']['event'])
        else:
            self.__dispatch(event, data)

    # Chat
    def parse_channel_chat_clear_v1(self, d: MPData[eventsub.chat.ChatClearEvent]) -> None:
        self._dispatcher('chat_clear', d)

    def parse_channel_chat_clear_user_messages_v1(self, d: MPData[eventsub.chat.ClearUserMessagesEvent]) -> None:
        self._dispatcher('chat_clear_user_messages', d)

    def parse_channel_chat_message_v1(self, d: MPData[eventsub.chat.MessageEvent]) -> None:
        self._dispatcher('chat_message', d)

    def parse_channel_chat_message_delete_v1(self, d: MPData[eventsub.chat.MessageDeleteEvent]) -> None:
        self._dispatcher('chat_message_delete', d)

    def parse_channel_chat_notification_v1(self, d: MPData[eventsub.chat.NotificationEvent]) -> None:
        self._dispatcher('chat_notification', d)

    def parse_channel_chat_settings_update_v1(self, d: MPData[eventsub.chat.SettingsUpdateEvent]) -> None:
        self._dispatcher('chat_settings_update', d)

    def parse_channel_shared_chat_begin_v1(self, d: MPData[eventsub.chat.SharedChatBeginEvent]) -> None:
        self._dispatcher('shared_chat_begin', d)

    def parse_channel_shared_chat_update_v1(self, d: MPData[eventsub.chat.SharedChatUpdateEvent]) -> None:
        self._dispatcher('shared_chat_update', d)

    def parse_channel_shared_chat_end_v1(self, d: MPData[eventsub.chat.SharedChatEndEvent]) -> None:
        self._dispatcher('shared_chat_end', d)

    # Bits
    def parse_channel_cheer_v1(self, d: MPData[eventsub.bits.CheerEvent]) -> None:
        self._dispatcher('cheer', d)

    def parse_channel_bits_use_v1(self, d: MPData[eventsub.bits.BitsEvent]) -> None:
        self._dispatcher('bits_use', d)

    # Moderation
    def parse_channel_shield_mode_begin_v1(self, d: MPData[eventsub.moderation.ShieldModeBeginEvent]) -> None:
        self._dispatcher('shield_mode_begin', d)

    def parse_channel_shield_mode_end_v1(self, d: MPData[eventsub.moderation.ShieldModeEndEvent]) -> None:
        self._dispatcher('shield_mode_end', d)

    def parse_channel_suspicious_user_message_v1(self,
                                              d: MPData[eventsub.moderation.SuspiciousUserMessageEvent]) -> None:
        self._dispatcher('suspicious_user_message', d)

    def parse_channel_suspicious_user_update_v1(self, d: MPData[eventsub.moderation.SuspiciousUserUpdateEvent]) -> None:
        self._dispatcher('suspicious_user_update', d)

    def parse_channel_warning_acknowledge_v1(self, d: MPData[eventsub.moderation.WarningAcknowledgeEvent]) -> None:
        self._dispatcher('warning_acknowledge', d)

    def parse_channel_warning_send_v1(self, d: MPData[eventsub.moderation.WarningSendEvent]) -> None:
        self._dispatcher('warning_send', d)

    def parse_automod_message_hold_v2(self, d: MPData[eventsub.moderation.AutomodMessageHoldEvent]) -> None:
        self._dispatcher('automod_message_hold', d)

    def parse_automod_message_update_v2(self, d: MPData[eventsub.moderation.AutomodMessageUpdateEvent]) -> None:
        self._dispatcher('automod_message_update', d)

    def parse_automod_settings_update_v1(self, d: MPData[eventsub.moderation.AutomodSettingsUpdateEvent]) -> None:
        self._dispatcher('automod_settings_update', d)

    def parse_automod_terms_update_v1(self, d: MPData[eventsub.moderation.AutomodTermsUpdateEvent]) -> None:
        self._dispatcher('automod_terms_update', d)

    def parse_channel_ban_v1(self, d: MPData[eventsub.moderation.BanEvent]) -> None:
        self._dispatcher('ban', d)

    def parse_channel_unban_v1(self, d: MPData[eventsub.moderation.UnbanEvent]) -> None:
        self._dispatcher('unban', d)

    def parse_channel_unban_request_create_v1(self, d: MPData[eventsub.moderation.UnbanRequestCreateEvent]) -> None:
        self._dispatcher('unban_request_create', d)

    def parse_channel_moderate_v2(self, d: MPData[eventsub.moderation.UnbanRequestResolveEvent]) -> None:
        self._dispatcher('channel_moderate', d)

    def parse_channel_unban_request_resolve_v1(self, d: MPData[eventsub.moderation.ModerateEvent]) -> None:
        self._dispatcher('unban_request_resolve', d)

    def parse_channel_moderator_add_v1(self, d: MPData[eventsub.moderation.ModeratorAddEvent]) -> None:
        self._dispatcher('moderator_add', d)

    def parse_channel_moderator_remove_v1(self, d: MPData[eventsub.moderation.ModeratorRemoveEvent]) -> None:
        self._dispatcher('moderator_remove', d)

    # Channels
    def parse_channel_update_v2(self, d: MPData[eventsub.channels.ChannelUpdateEvent]) -> None:
        self.user.channel.title = d['payload']['event']['title']
        self.user.channel.language = d['payload']['event']['language']
        self.user.channel.category_id = d['payload']['event']['category_id']
        self.user.channel.category_name = d['payload']['event']['category_name']
        self.user.channel.ccl = d['payload']['event']['content_classification_labels']
        self._dispatcher('channel_update', d)

    def parse_channel_follow_v2(self, d: MPData[eventsub.channels.FollowEvent]) -> None:
        self._dispatcher('follow', d)

    def parse_channel_subscribe_v1(self, d: MPData[eventsub.channels.SubscribeEvent]) -> None:
        self._dispatcher('subscribe', d)

    def parse_channel_subscription_end_v1(self, d: MPData[eventsub.channels.SubscriptionEndEvent]) -> None:
        self._dispatcher('subscription_end', d)

    def parse_channel_subscription_gift_v1(self, d: MPData[eventsub.channels.SubscriptionGiftEvent]) -> None:
        self._dispatcher('subscription_gift', d)

    def parse_channel_subscription_message_v1(self, d: MPData[eventsub.channels.SubscriptionMessageEvent]) -> None:
        self._dispatcher('subscription_message', d)

    def parse_channel_vip_add_v1(self, d: MPData[eventsub.channels.VIPAddEvent]) -> None:
        self._dispatcher('vip_add', d)

    def parse_channel_vip_remove_v1(self, d: MPData[eventsub.channels.VIPRemoveEvent]) -> None:
        self._dispatcher('vip_remove', d)

    # Interaction
    def parse_channel_channel_points_automatic_reward_redemption_add_v1(
            self, d: MPData[eventsub.interaction.AutomaticRewardRedemptionAddEventV1]) -> None:
        self._dispatcher('points_automatic_reward_redemption_add_v1', d)

    def parse_channel_channel_points_automatic_reward_redemption_add_v2(
            self, d: MPData[eventsub.interaction.AutomaticRewardRedemptionAddEventV2]) -> None:
        self._dispatcher('points_automatic_reward_redemption_add_v2', d)

    def parse_channel_channel_points_custom_reward_add_v1(self,
                                                       d: MPData[eventsub.interaction.PointRewardEvent]) -> None:
        self._dispatcher('points_reward_add', d)

    def parse_channel_channel_points_custom_reward_update_v1(self,
                                                          d: MPData[eventsub.interaction.PointRewardEvent]) -> None:
        self._dispatcher('points_reward_update', d)

    def parse_channel_channel_points_custom_reward_remove_v1(self,
                                                          d: MPData[eventsub.interaction.PointRewardEvent]) -> None:
        self._dispatcher('points_reward_remove', d)

    def parse_channel_channel_points_custom_reward_redemption_add(
            self, d: MPData[eventsub.interaction.RewardRedemptionEvent]) -> None:
        self._dispatcher('points_reward_redemption_add', d)

    def parse_channel_channel_points_custom_reward_redemption_update(
            self, d: MPData[eventsub.interaction.RewardRedemptionEvent]) -> None:
        self._dispatcher('points_reward_redemption_update', d)

    def parse_channel_poll_begin_v1(self, d: MPData[eventsub.interaction.PollBeginEvent]) -> None:
        self._dispatcher('poll_begin', d)

    def parse_channel_poll_progress_v1(self, d: MPData[eventsub.interaction.PollProgressEvent]) -> None:
        self._dispatcher('poll_progress', d)

    def parse_channel_poll_end_v1(self, d: MPData[eventsub.interaction.PollEndEvent]) -> None:
        self._dispatcher('poll_end', d)

    def parse_channel_prediction_begin_v1(self, d: MPData[eventsub.interaction.PredictionBeginEvent]) -> None:
        self._dispatcher('prediction_begin', d)

    def parse_channel_prediction_progress_v1(self, d: MPData[eventsub.interaction.PredictionProgressEvent]) -> None:
        self._dispatcher('prediction_progress', d)

    def parse_channel_prediction_lock_v1(self, d: MPData[eventsub.interaction.PredictionLockEvent]) -> None:
        self._dispatcher('prediction_lock', d)

    def parse_channel_prediction_end_v1(self, d: MPData[eventsub.interaction.PredictionEndEvent]) -> None:
        self._dispatcher('prediction_end', d)

    def parse_channel_hype_train_begin_v1(self, d: MPData[eventsub.interaction.HypeTrainEvent]) -> None:
        self._dispatcher('hype_train_begin', d)

    def parse_channel_hype_train_progress_v1(self, d: MPData[eventsub.interaction.HypeTrainEvent]) -> None:
        self._dispatcher('hype_train_progress', d)

    def parse_channel_hype_train_end_v1(self, d: MPData[eventsub.interaction.HypeTrainEndEvent]) -> None:
        self._dispatcher('hype_train_end', d)

    # Activity
    def parse_channel_charity_campaign_donate_v1(self, d: MPData[eventsub.activity.CharityDonationEvent]) -> None:
        self._dispatcher('charity_campaign_donate', d)

    def parse_channel_charity_campaign_start_v1(self, d: MPData[eventsub.activity.CharityCampaignStartEvent]) -> None:
        self._dispatcher('charity_campaign_start', d)

    def parse_channel_charity_campaign_progress_v1(self,
                                                d: MPData[eventsub.activity.CharityCampaignProgressEvent]) -> None:
        self._dispatcher('charity_campaign_progress', d)

    def parse_channel_charity_campaign_stop_v1(self, d: MPData[eventsub.activity.CharityCampaignStopEvent]) -> None:
        self._dispatcher('charity_campaign_stop', d)

    def parse_channel_goal_begin_v1(self, d: MPData[eventsub.activity.GoalsEvent]) -> None:
        self._dispatcher('goal_begin', d)

    def parse_channel_goal_progress_v1(self, d: MPData[eventsub.activity.GoalsEvent]) -> None:
        self._dispatcher('goal_progress', d)

    def parse_channel_goal_end_v1(self, d: MPData[eventsub.activity.GoalsEvent]) -> None:
        self._dispatcher('goal_end', d)

    # Streams
    def parse_channel_ad_break_begin_v1(self, d: MPData[eventsub.streams.AdBreakBeginEvent]) -> None:
        self._dispatcher('ad_break_begin', d)

    def parse_channel_raid_v1(self, d: MPData[eventsub.streams.RaidEvent]) -> None:
        self._dispatcher('raid', d)

    def parse_channel_shoutout_create_v1(self, d: MPData[eventsub.streams.ShoutoutCreateEvent]) -> None:
        self._dispatcher('shoutout_create', d)

    def parse_channel_shoutout_receive_v1(self, d: MPData[eventsub.streams.ShoutoutReceivedEvent]) -> None:
        self._dispatcher('shoutout_received', d)

    def parse_stream_online_v1(self, d: MPData[eventsub.streams.StreamOnlineEvent]) -> None:
        self.is_live = True
        self._dispatcher('stream_online', d)

    def parse_stream_offline_v1(self, d: MPData[eventsub.streams.StreamOfflineEvent]) -> None:
        self.is_live = False
        self._dispatcher('stream_offline', d)

    # Users
    def parse_user_update_v1(self, d: MPData[eventsub.users.UserUpdateEvent]) -> None:
        self.user.name = d['payload']['event']['user_login']
        self.user.display_name = d['payload']['event']['user_name']
        self.user.description = d['payload']['event']['description']
        self.user.email = d['payload']['event'].get('email') or None
        self._dispatcher('user_update', d)

    def parse_user_whisper_message_v1(self, d: MPData[eventsub.users.WhisperReceivedEvent]) -> None:
        self._dispatcher('whisper_received', d)

    def parse_channel_chat_user_message_hold_v1(self, d: MPData[eventsub.users.MessageHoldEvent]) -> None:
        self._dispatcher('chat_user_message_hold', d)

    def parse_channel_chat_user_message_update_v1(self, d: MPData[eventsub.users.MessageUpdateEvent]) -> None:
        self._dispatcher('chat_user_message_update', d)
