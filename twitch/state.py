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

from .channel import Charity, CharityDonation, Follow, BannedUser, UserChannel
from .broadcaster import ClientUser, ClientChannel, ClientChat, ClientStream
from .alerts import Raider, Gifter, Subscriber, Cheerer, Goal, HypeTrain
from .utils import convert_rfc3339, MISSING, EXCLUSIVE
from .chat import ShieldModeSettings, Emote, Badge
from .reward import Reward, Redemption
from .stream import Category, Stream
from .prediction import Prediction
from .channel import Video, Clip
from .user import BaseUser, User
from .errors import NotFound
from .user import UserEmail
from .poll import Poll
import asyncio
import weakref

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .types import (user as UserTypes, channel as ChannelTypes, chat as ChatTypes,
                        stream as StreamTypes, poll as PollTypes, reward as RewardTypes,
                        prediction as PredictionTypes, alerts as AlertsTypes)
    from typing import Optional, Dict, Callable, Any, List, Union, AsyncGenerator
    from datetime import datetime
    from .http import HTTPClient

import logging
_logger = logging.getLogger(__name__)

__all__ = ('ConnectionState',)


class ConnectionState:
    """
    Represents the state of the connection.
    """
    __slots__ = ('http', '__dispatch', 'user', 'chat', 'channel', 'stream', 'is_streaming',
                 '_users', '_channels', '_user_ids', '_category_ids')

    def __init__(self, dispatcher: Callable[..., Any], http: HTTPClient) -> None:
        self.http: HTTPClient = http
        self.__dispatch: Callable[[str, Any, Any], asyncio.Task] = dispatcher
        # Client
        self.user: Optional[ClientUser] = None
        self.chat: Optional[ClientChat] = None
        self.channel: Optional[ClientChannel] = None
        self.stream: Optional[ClientStream] = None
        self.is_streaming: bool = False
        # Caching.
        self._users: weakref.WeakValueDictionary[str, User] = weakref.WeakValueDictionary()
        self._channels: weakref.WeakValueDictionary[str, UserChannel] = weakref.WeakValueDictionary()
        self._user_ids: Dict[str, BaseUser] = {}
        self._category_ids: Dict[str, Category] = {}

    async def setup_client(self):
        data = await self.http.get_users()
        self.user = ClientUser(state=self, data=data[0])
        # Client Channel.
        data = await self.http.get_channels(broadcaster_ids=[self.user.id])
        self.channel = ClientChannel(state=self, data=data[0])
        # Client Chat.
        self.chat = ClientChat(state=self)
        # Client stream.
        self.stream = ClientStream(state=self)
        # Checks if the client is streaming.
        async for streams in self.fetch_streams(limit=1, users=[self.user.name], stream_type='all'):
            if streams:
                self.is_streaming = True

    def clear(self):
        self._users: weakref.WeakValueDictionary[str, User] = weakref.WeakValueDictionary()
        self._channels: weakref.WeakValueDictionary[str, UserChannel] = weakref.WeakValueDictionary()
        self._user_ids: Dict[str, BaseUser] = {}
        self._category_ids: Dict[str, Category] = {}

    # ------------------------------------
    #              + User +
    # ------------------------------------
    async def get_users(self, names: List[str], cache: bool = True) -> List[BaseUser]:
        names: List[str] = [name.lower() for name in names]
        users: List[BaseUser] = []
        try:
            for name in names:
                user = self._user_ids[name]
                users.append(user)
        except KeyError:
            users.clear()
            data = await self.http.get_users(user_names=names)
            for payload in data:
                user = BaseUser(data=payload)
                users.append(user)
                if cache:
                    self._user_ids[user.name.lower()] = user
        return users

    async def get_user(self, user: Union[str, BaseUser]) -> BaseUser:
        if isinstance(user, BaseUser):
            return user
        data = await self.get_users(names=[user])
        if len(data) == 1:
            return data[0]
        raise NotFound('Unable to find the requested user.')

    async def get_user_info(self, name: str = EXCLUSIVE, user_id: str = EXCLUSIVE,
                            cache: bool = True) -> User:
        data = []
        if name is EXCLUSIVE and user_id is EXCLUSIVE:
            raise TypeError('Mutually exclusive options: name, id.')
        else:
            if user_id is not EXCLUSIVE:
                data = await self.http.get_users(user_ids=[user_id])
            if name is not EXCLUSIVE:
                try:
                    return self._users[name.lower()]
                except KeyError:
                    pass
                data = await self.http.get_users(user_names=[name])
            if len(data) == 1:
                user = User(data=data[0])
                if cache:
                    self._users[user.name.lower()] = user
                return user
            raise NotFound('Unable to find the requested user.')

    # ------------------------------------
    #             + Category +
    # ------------------------------------
    async def get_categories(self, names: List[str], cache: bool = True) -> List[Category]:
        names: List[str] = [name.lower() for name in names]
        categories: List[Category] = []
        try:
            for name in names:
                category = self._category_ids[name]
                categories.append(category)
        except KeyError:
            categories.clear()
            data = await self.http.get_categories(category_names=names)
            for payload in data:
                category = Category(data=payload)
                categories.append(category)
                if cache:
                    self._category_ids[category.name.lower()] = category
        return categories

    async def get_category(self, category: Union[str, Category]) -> Category:
        if isinstance(category, Category):
            return category
        data = await self.get_categories(names=[category])
        if len(data) == 1:
            self._category_ids[data[0].name] = data[0]
            return data[0]
        raise NotFound('Unable to find the requested category.')

    # -----------------------------------
    #             + Channel +
    # -----------------------------------
    async def get_channel(self, user: Union[str, BaseUser], cache: bool = True) -> UserChannel:
        user = await self.get_user(user=user)
        try:
            return self._channels[user.id]
        except KeyError:
            pass
        channel = UserChannel(state=self, broadcaster_id=user.id)
        if cache:
            self._channels[user.id] = channel
        return UserChannel(state=self, broadcaster_id=user.id)

    async def get_global_emotes(self) -> List[Emote]:
        data = await self.http.get_global_emotes()
        return [Emote(data=emote, template_url=data[0]) for emote in data[1]]

    async def get_global_badges(self) -> List[Badge]:
        data = await self.http.get_global_chat_badge()
        return [Badge(data=badge) for badge in data]

    # -----------------------------------
    #             + Stream +
    # -----------------------------------
    async def fetch_streams(self, limit: int, stream_type: str,
                            users: List[Union[str, BaseUser]] = MISSING,
                            categories: List[Union[str, Category]] = MISSING,
                            languages: List[str] = MISSING) -> AsyncGenerator[List[Stream]]:
        if users is not MISSING:
            users = [user.name for user in (await self.get_users(users))]
        if categories is not MISSING:
            categories = [category.id for category in (await self.get_categories(categories))]
        async for streams in self.http.fetch_streams(limit=limit, user_names=users, game_ids=categories,
                                                     stream_type=stream_type, languages=languages):
            yield [Stream(data=stream) for stream in streams]

    # -----------------------------------
    #          + Video & Clips +
    # -----------------------------------
    async def fetch_videos(self,
                           videos: List[Union[str, Video, Clip]] = EXCLUSIVE,
                           category: Union[str, Category] = EXCLUSIVE,
                           language: str = MISSING,
                           period: str = MISSING,
                           sort: str = MISSING,
                           videos_type: str = MISSING,
                           limit: int = 4) -> AsyncGenerator[List[Video]]:
        if videos is not EXCLUSIVE:
            videos = [
                (i.id if isinstance(i, Video)
                 else (i if isinstance(i, str)
                       else (i.video_id if isinstance(i, Clip) and i.video_id is not None
                             else i))) for i in videos
            ]
        if category is not EXCLUSIVE:
            category = await self.get_category(category=category)
        async for videos in self.http.fetch_videos(limit=limit, video_ids=videos,
                                                   category_id=category.id, language=language,
                                                   period=period, sort=sort, videos_type=videos_type):
            yield [Video(data=video) for video in videos]

    async def fetch_clips(self,
                          clips: List[Union[str, Clip]] = EXCLUSIVE,
                          category: Union[str, Category] = EXCLUSIVE,
                          started_at: datetime = MISSING,
                          ended_at: datetime = MISSING,
                          featured: bool = MISSING,
                          limit: int = 4) -> AsyncGenerator[List[Clip]]:
        if clips is not EXCLUSIVE:
            clips = [(clip.id if isinstance(clip, Clip) else clip) for clip in clips]
        if category is not EXCLUSIVE:
            category = await self.get_category(category=category)
        async for clips in self.http.fetch_clips(limit=limit, category_id=category.id,
                                                 clip_ids=clips, started_at=started_at,
                                                 ended_at=ended_at, is_featured=featured):
            yield [Clip(data=clip) for clip in clips]

    async def connect(self):
        self.clear()
        self.__dispatch('connect')

    async def reconnect(self):
        self.__dispatch('reconnect')

    async def socket_raw_receive(self, data: str):
        self.__dispatch('socket_raw_receive', data)

    # ----------------------------------
    #            + EventSub +
    # ----------------------------------
    async def parse(self, method: str, data: Optional[Dict[str, Any]] = None) -> None:
        """
        Parse an event and dispatch it to the appropriate handler.
        """
        try:
            parse = getattr(self, 'parse_' + method.replace('.', '_'))
            if data is None:
                await parse()
            else:
                await parse(data)
        except Exception as error:
            _logger.exception('Failed to parse event: %s', error)

    async def parse_user_update(self, data: UserTypes.UserUpdateEvent) -> None:
        """
        Parse a user update event.
        """
        if self.user is not None:
            self.user.name = data['user_login']
            self.user.display_name = data['user_name']
            self.user.description = data['description']
            self.user.email = UserEmail(data=data) or None
            self.__dispatch('user_update', self.user)

    async def parse_channel_update(self, data: ChannelTypes.ChannelUpdateEvent) -> None:
        """
        Parse a channel update event.
        """
        if self.channel is not None:
            self.channel.title = data['title']
            self.channel.language = data['language']
            self.channel.category = Category(data=data) or None
            self.channel.ccls = data['content_classification_labels']
            self.__dispatch('channel_update', self.channel)

    async def parse_stream_online(self, data: StreamTypes.Online) -> None:
        """
        Parse a stream online event.
        """
        _logger.debug('%s is now streaming.', data['broadcaster_user_login'])
        self.__dispatch('stream_online', data['type'], convert_rfc3339(data['started_at']))

    async def parse_stream_offline(self, data: UserTypes.SpecificBroadcaster) -> None:
        """
        Parse a stream offline event.
        """
        _logger.debug('%s is no longer streaming.', data['broadcaster_user_login'])
        self.__dispatch('stream_offline')

    async def parse_channel_charity_campaign_donate(self, data: ChannelTypes.CharityDonationEvent) -> None:
        """
        Parse a channel charity campaign donate event.
        """
        charity = Charity(data=data)
        donor = CharityDonation(data=data)
        self.__dispatch('charity_campaign_donate', charity, donor)

    async def parse_channel_charity_campaign_start(self, data: ChannelTypes.CharityStartEvent) -> None:
        """
        Parse a channel charity campaign start event.
        """
        charity = Charity(data=data)
        started_at = convert_rfc3339(data['started_at'])
        self.__dispatch('charity_campaign_start', charity, started_at)

    async def parse_channel_charity_campaign_progress(self, data: ChannelTypes.Charity) -> None:
        """
        Parse a channel charity campaign progress event.
        """
        charity = Charity(data=data)
        self.__dispatch('charity_campaign_progress', charity)

    async def parse_channel_charity_campaign_stop(self, data: ChannelTypes.CharityStopEvent) -> None:
        """
        Parse a channel charity campaign stop event.
        """
        charity = Charity(data=data)
        stopped_at = convert_rfc3339(data['stopped_at'])
        self.__dispatch('charity_campaign_stop', charity, stopped_at)

    async def parse_channel_follow(self, data: ChannelTypes.Follower) -> None:
        """
        Parse a channel follow event.
        """
        follower = Follow(data=data)
        self.__dispatch('follow', follower)

    async def parse_channel_subscribe(self, data: AlertsTypes.SubscribeEvent) -> None:
        """
        Parse a channel subscribe event.
        """
        subscriber = Subscriber(data=data)
        self.__dispatch('subscribe', subscriber)

    async def parse_channel_subscription_end(self, data: AlertsTypes.SubscribeEvent) -> None:
        """
        Parse a channel subscription end event.
        """
        subscriber = Subscriber(data=data)
        self.__dispatch('subscription_end', subscriber)

    async def parse_channel_subscription_message(self, data: AlertsTypes.SubscribeEvent) -> None:
        """
        Parse a channel re-subscription event.
        """
        re_subscribe = Subscriber(data=data)
        self.__dispatch('subscription_message', re_subscribe)

    async def parse_channel_subscription_gift(self, data: AlertsTypes.GiftSubsEvent) -> None:
        """
        Parse a channel subscription gift event.
        """
        gifts = Gifter(data=data)
        self.__dispatch('subscription_gift', gifts)

    async def parse_channel_cheer(self, data: AlertsTypes.CheerEvent) -> None:
        """
        Parse a channel cheer event.
        """
        cheer = Cheerer(data=data)
        self.__dispatch('cheer', cheer)

    async def parse_channel_raid(self, data: AlertsTypes.RaidEvent) -> None:
        """
        Parse a channel raid event.
        """
        raid = Raider(data=data)
        self.__dispatch('raid', raid)

    async def parse_channel_ban(self, data: ChannelTypes.BannedUserEvent) -> None:
        """
        Parse a channel ban event.
        """
        banned_user = BannedUser(data=data)
        self.__dispatch('ban', banned_user)

    async def parse_channel_unban(self, data: ChannelTypes.UnBannedUserEvent) -> None:
        """
        Parse a channel unban event.
        """
        user = BaseUser(data=data, prefix='user_')
        moderator = BaseUser(data=data, prefix='moderator_user_')
        self.__dispatch('unban', user, moderator)

    async def parse_channel_moderator_add(self, data: AlertsTypes.ModeratorPrivilegesEvent) -> None:
        """
        Parse a channel moderator add event.
        """
        user = BaseUser(data=data, prefix='user_')
        self.__dispatch('moderator_add', user)

    async def parse_channel_moderator_remove(self, data: AlertsTypes.ModeratorPrivilegesEvent) -> None:
        """
        Parse a channel moderator remove event.
        """
        user = BaseUser(data=data, prefix='user_')
        self.__dispatch('moderator_remove', user)

    async def parse_channel_channel_points_custom_reward_add(self, data: RewardTypes.RewardEvent) -> None:
        """
        Parse a channel custom reward add event for channel points.
        """
        reward = Reward(data=data)
        self.__dispatch('points_reward_add', reward)

    async def parse_channel_channel_points_custom_reward_update(self,
                                                                data: RewardTypes.RewardEvent) -> None:
        """
        Parse a channel custom reward update event for channel points.
        """
        reward = Reward(data=data)
        self.__dispatch('points_reward_update', reward)

    async def parse_channel_channel_points_custom_reward_remove(self, data: RewardTypes.RewardEvent):
        """
        Parse a channel custom reward remove event for channel points.
        """
        reward = Reward(data=data)
        self.__dispatch('points_reward_remove', reward)

    async def parse_channel_channel_points_custom_reward_redemption_add(
            self, data: RewardTypes.RedemptionEvent) -> None:
        """
        Parse a channel custom reward redemption add event for channel points.
        """
        redemption = Redemption(data=data)
        self.__dispatch('points_reward_redemption', redemption)

    async def parse_channel_channel_points_custom_reward_redemption_update(
            self, data: RewardTypes.RedemptionEvent) -> None:
        """
        Parse a channel custom reward redemption update event for channel points.
        """
        redemption = Redemption(data=data)
        self.__dispatch('points_reward_redemption_update', redemption)

    async def parse_channel_poll_begin(self, data: PollTypes.PollBeginAndProgressEvent) -> None:
        """
        Parse a channel poll begin event.
        """
        poll = Poll(data=data)
        self.__dispatch('poll_begin', poll)

    async def parse_channel_poll_progress(self, data: PollTypes.PollBeginAndProgressEvent) -> None:
        """
        Parse a channel poll progress event.
        """
        poll = Poll(data=data)
        self.__dispatch('poll_progress', poll)

    async def parse_channel_poll_end(self, data: PollTypes.PollEndEvent) -> None:
        """
        Parse a channel poll end event.
        """
        poll = Poll(data=data)
        self.__dispatch('poll_end', poll)

    async def parse_channel_prediction_begin(self, data: PredictionTypes.PredictionBeginProgressEvent) \
            -> None:
        """
        Parse a channel prediction begin event.
        """
        prediction = Prediction(data=data)
        self.__dispatch('prediction_begin', prediction)

    async def parse_channel_prediction_progress(self, data: PredictionTypes.PredictionBeginProgressEvent) \
            -> None:
        """
        Parse a channel prediction progress event.
        """
        prediction = Prediction(data=data)
        self.__dispatch('prediction_progress', prediction)

    async def parse_channel_prediction_lock(self, data: PredictionTypes.PredictionLockEvent) -> None:
        """
        Parse a channel prediction lock event.
        """
        prediction = Prediction(data=data)
        self.__dispatch('prediction_lock', prediction)

    async def parse_channel_prediction_end(self, data: PredictionTypes.PredictionEndEvent) -> None:
        """
        Parse a channel prediction end event.
        """
        prediction = Prediction(data=data)
        self.__dispatch('prediction_end', prediction)

    async def parse_channel_goal_begin(self, data: AlertsTypes.GoalBeginProgressEvent) -> None:
        """
        Parse a channel goal begin event.
        """
        goal = Goal(data=data)
        self.__dispatch('goal_begin', goal)

    async def parse_channel_goal_progress(self, data: AlertsTypes.GoalBeginProgressEvent) -> None:
        """
        Parse a channel goal progress event.
        """
        goal = Goal(data=data)
        self.__dispatch('goal_progress', goal)

    async def parse_channel_goal_end(self, data: AlertsTypes.GoalEndEvent) -> None:
        """
        Parse a channel goal end event.
        """
        goal = Goal(data=data)
        self.__dispatch('goal_end', goal)

    async def parse_channel_hype_train_begin(self, data: AlertsTypes.HypeTrainBeginProgressEvent) -> None:
        """
        Parse a channel hype train begin event.
        """
        hypertrain = HypeTrain(data=data)
        self.__dispatch('hype_train_begin', hypertrain)

    async def parse_channel_hype_train_progress(self, data: AlertsTypes.HypeTrainBeginProgressEvent) -> None:
        """
        Parse a channel hype train progress event.
        """
        hypertrain = HypeTrain(data=data)
        self.__dispatch('hype_train_progress', hypertrain)

    async def parse_channel_hype_train_end(self, data: AlertsTypes.HypeTrainEndEvent) -> None:
        """
        Parse a channel hype train end event.
        """
        hypertrain = HypeTrain(data=data)
        self.__dispatch('hype_train_end', hypertrain)

    async def parse_channel_shield_mode_begin(self, data: ChatTypes.ShieldModeBeginEvent) -> None:
        """
        Parse a channel shield mode begin event.
        """
        _mode = ShieldModeSettings(data=data)
        self.__dispatch('shield_mode_begin', _mode)

    async def parse_channel_shield_mode_end(self, data: ChatTypes.ShieldModeEndEvent) -> None:
        """
        Parse a channel shield mode end event.
        """
        _mode = ShieldModeSettings(data=data)
        self.__dispatch('shield_mode_end', _mode)

    async def parse_channel_shoutout_create(self, data: AlertsTypes.ShoutoutCreateEvent) -> None:
        """
        Parse a channel shoutout create event.
        """
        to_broadcaster = BaseUser(data, prefix='to_broadcaster_user_')
        by_user = BaseUser(data, prefix='moderator_user_')
        self.__dispatch('shoutout_create', to_broadcaster, by_user, data['viewer_count'])

    async def parse_channel_shoutout_receive(self, data: AlertsTypes.ShoutoutReceiveEvent) -> None:
        """
        Parse a channel shoutout receive event.
        """
        from_broadcaster = BaseUser(data, prefix='from_broadcaster_user_')
        self.__dispatch('shoutout_receive', from_broadcaster, data['viewer_count'])
