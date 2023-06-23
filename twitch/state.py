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

# Core
from .channel import Update, Subscription, SubscriptionGift, SubscriptionMessage, Cheer, Raid
from .goals import Donation, Charity, Goal, HyperTrain
from .user import Follower, User, UserUpdate
from .broadcaster import Broadcaster
from .moderation import Ban, UnBan, ShieldMode
from .stream import Online, Offline, Shoutout
from .reward import Reward, Redemption
from .survey import Poll, Prediction
from asyncio import Task

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, Dict, Callable, Any, List
    from .http import HTTPClient
    from .types.eventsub.reward import Redemption as Rp
    from .types.eventsub import (
        channel as chl,
        moderation as md,
        reward as rd,
        poll as pl,
        prediction as pd,
        charity as ch,
        goal as gl,
        hypertrain as ht,
        stream as sm,
        user as us)

import logging

_logger = logging.getLogger(__name__)


class ConnectionState:
    """
    Represents the state of the connection.
    """
    __slots__ = ('_http', 'broadcaster', '_dispatch', 'is_streaming', 'events')

    def __init__(self, dispatcher: Callable[..., Any], http: HTTPClient, events: List[str]) -> None:
        self._http: HTTPClient = http
        self._dispatch: Callable[[str, Any, Any], Task] = dispatcher
        self.broadcaster: Optional[Broadcaster] = None
        self.events: List[str] = events

    async def get_client(self) -> None:
        """
        Retrieves the broadcaster's data from the connection's HTTP client and initializes the
        Broadcaster object.
        """
        _data = await self._http.get_client()
        self.broadcaster = Broadcaster(http=self._http, user=_data)

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
            _logger.error('Failed to parse event: %s, %s', method, error)

    async def parse_ready(self) -> None:
        """
        Parse ready event.
        """
        self._dispatch('ready')

    async def parse_channel_update(self, data: chl.Update) -> None:
        """
        Parse a channel update event.
        """
        _channel = Update(channel=data)
        self._dispatch('channel_update', _channel)

    async def parse_channel_follow(self, data: chl.Follow) -> None:
        """
        Parse a channel follow event.
        """
        _user = Follower(channel=data)
        self._dispatch('follow', _user)

    async def parse_channel_subscribe(self, data: chl.Subscribe) -> None:
        """
        Parse a channel subscribe event.
        """
        _subscription = Subscription(channel=data)
        self._dispatch('subscribe', _subscription)

    async def parse_channel_subscription_end(self, data: chl.SubscriptionEnd) -> None:
        """
        Parse a channel subscription end event.
        """
        _subscription = Subscription(channel=data)
        self._dispatch('subscription_end', _subscription)

    async def parse_channel_subscription_gift(self, data: chl.SubscriptionGift) -> None:
        """
        Parse a channel subscription gift event.
        """
        _subscription = SubscriptionGift(channel=data)
        self._dispatch('subscription_gift', _subscription)

    async def parse_channel_subscription_message(self, data: chl.SubscriptionMessage) -> None:
        """
        Parse a channel re-subscription event.
        """
        _subscription = SubscriptionMessage(channel=data)
        self._dispatch('subscription_message', _subscription)

    async def parse_channel_cheer(self, data: chl.Cheer) -> None:
        """
        Parse a channel cheer event.
        """
        _cheer = Cheer(channel=data)
        self._dispatch('cheer', _cheer)

    async def parse_channel_raid(self, data: chl.Raid) -> None:
        """
        Parse a channel raid event.
        """
        _raid = Raid(raid=data)
        self._dispatch('raid', _raid)

    # ========================> Moderation <========================
    async def parse_channel_ban(self, data: md.Ban) -> None:
        """
        Parse a channel ban event.
        """
        _ban = Ban(ban=data)
        self._dispatch('ban', _ban)

    async def parse_channel_unban(self, data: md.UnBan) -> None:
        """
        Parse a channel unban event.
        """
        _unban = UnBan(unban=data)
        self._dispatch('unban', _unban)

    async def parse_channel_moderator_add(self, data: md.Add) -> None:
        """
        Parse a channel moderator add event.
        """
        _user = User(user=data)
        self._dispatch('moderator_add', _user)

    async def parse_channel_moderator_remove(self, data: md.Remove) -> None:
        """
        Parse a channel moderator remove event.
        """
        _user = User(user=data)
        self._dispatch('moderator_remove', _user)

    # ========================> Reward <========================
    async def parse_channel_channel_points_custom_reward_add(self, data: rd.Reward) -> None:
        """
        Parse a channel custom reward add event for channel points.
        """
        _reward = Reward(reward=data)
        self._dispatch('points_reward_add', _reward)

    async def parse_channel_channel_points_custom_reward_update(self, data: rd.Reward) -> None:
        """
        Parse a channel custom reward update event for channel points.
        """
        _reward = Reward(reward=data)
        self._dispatch('points_reward_update', _reward)

    async def parse_channel_channel_points_custom_reward_remove(self, data: rd.Reward):
        """
        Parse a channel custom reward remove event for channel points.
        """
        _reward = Reward(reward=data)
        self._dispatch('points_reward_remove', _reward)

    async def parse_channel_channel_points_custom_reward_redemption_add(self, data: Rp) -> None:
        """
        Parse a channel custom reward redemption add event for channel points.
        """
        _redemption = Redemption(redemption=data)
        self._dispatch('points_reward_redemption', _redemption)

    async def parse_channel_channel_points_custom_reward_redemption_update(self, data: Rp) -> None:
        """
        Parse a channel custom reward redemption update event for channel points.
        """
        _redemption = Redemption(redemption=data)
        self._dispatch('points_reward_redemption_update', _redemption)

    # ========================> Survey <========================
    # Poll
    async def parse_channel_poll_begin(self, data: pl.Begin) -> None:
        """
        Parse a channel poll begin event.
        """
        _poll = Poll(poll=data)
        self._dispatch('poll_begin', _poll)

    async def parse_channel_poll_progress(self, data: pl.Progress) -> None:
        """
        Parse a channel poll progress event.
        """
        _poll = Poll(poll=data)
        self._dispatch('poll_progress', _poll)

    async def parse_channel_poll_end(self, data: pl.End) -> None:
        """
        Parse a channel poll end event.
        """
        _poll = Poll(poll=data)
        self._dispatch('poll_end', _poll)

    # Prediction
    async def parse_channel_prediction_begin(self, data: pd.Begin) -> None:
        """
        Parse a channel prediction begin event.
        """
        _prediction = Prediction(prediction=data)
        self._dispatch('prediction_begin', _prediction)

    async def parse_channel_prediction_progress(self, data: pd.Progress) -> None:
        """
        Parse a channel prediction progress event.
        """
        _prediction = Prediction(prediction=data)
        self._dispatch('prediction_progress', _prediction)

    async def parse_channel_prediction_lock(self, data: pd.Lock) -> None:
        """
        Parse a channel prediction lock event.
        """
        _prediction = Prediction(prediction=data)
        self._dispatch('prediction_lock', _prediction)

    async def parse_channel_prediction_end(self, data: pd.End) -> None:
        """
        Parse a channel prediction end event.
        """
        _prediction = Prediction(prediction=data)
        self._dispatch('prediction_end', _prediction)

    # ========================> Goals <========================
    # Charity
    async def parse_channel_charity_campaign_donate(self, data: ch.Donation) -> None:
        """
        Parse a channel charity campaign donate event.
        """
        _donation = Donation(donation=data)
        self._dispatch('charity_campaign_donate', _donation)

    async def parse_channel_charity_campaign_start(self, data: ch.Start) -> None:
        """
        Parse a channel charity campaign start event.
        """
        _charity = Charity(charity=data)
        self._dispatch('charity_campaign_start', _charity)

    async def parse_channel_charity_campaign_progress(self, data: ch.Progress) -> None:
        """
        Parse a channel charity campaign progress event.
        """
        _charity = Charity(charity=data)
        self._dispatch('charity_campaign_progress', _charity)

    async def parse_channel_charity_campaign_stop(self, data: ch.Stop) -> None:
        """
        Parse a channel charity campaign stop event.
        """
        _charity = Charity(charity=data)
        self._dispatch('charity_campaign_stop', _charity)

    # Goal
    async def parse_channel_goal_begin(self, data: gl.Begin) -> None:
        """
        Parse a channel goal begin event.
        """
        _goal = Goal(goal=data)
        self._dispatch('goal_begin', _goal)

    async def parse_channel_goal_progress(self, data: gl.Progress) -> None:
        """
        Parse a channel goal progress event.
        """
        _goal = Goal(goal=data)
        self._dispatch('goal_progress', _goal)

    async def parse_channel_goal_end(self, data: gl.End) -> None:
        """
        Parse a channel goal end event.
        """
        _goal = Goal(goal=data)
        self._dispatch('goal_end', _goal)

    # Hyper train
    async def parse_channel_hype_train_begin(self, data: ht.Begin) -> None:
        """
        Parse a channel hype train begin event.
        """
        _hypertrain = HyperTrain(hypertrain=data)
        self._dispatch('hype_train_begin', _hypertrain)

    async def parse_channel_hype_train_progress(self, data: ht.Progress) -> None:
        """
        Parse a channel hype train progress event.
        """
        _hypertrain = HyperTrain(hypertrain=data)
        self._dispatch('hype_train_progress', _hypertrain)

    async def parse_channel_hype_train_end(self, data: ht.End) -> None:
        """
        Parse a channel hype train end event.
        """
        _hypertrain = HyperTrain(hypertrain=data)
        self._dispatch('hype_train_end', _hypertrain)

    async def parse_channel_shield_mode_begin(self, data: md.ShieldModeBegin) -> None:
        """
        Parse a channel shield mode begin event.
        """
        _mode = ShieldMode(mode=data)
        self._dispatch('shield_mode_begin', _mode)

    async def parse_channel_shield_mode_end(self, data: md.ShieldModeEnd) -> None:
        """
        Parse a channel shield mode end event.
        """
        _mode = ShieldMode(mode=data)
        self._dispatch('shield_mode_end', _mode)

    async def parse_channel_shoutout_create(self, data: sm.ShoutoutCreate) -> None:
        """
        Parse a channel shoutout create event.
        """
        _shoutout = Shoutout(shoutout=data)
        self._dispatch('shoutout_create', _shoutout)

    async def parse_channel_shoutout_receive(self, data: sm.ShoutoutReceived) -> None:
        """
        Parse a channel shoutout receive event.
        """
        _shoutout = Shoutout(shoutout=data)
        self._dispatch('shoutout_receive', _shoutout)

    async def parse_stream_online(self, data: sm.Online) -> None:
        """
        Parse a stream online event.
        """
        _stream = Online(stream=data)
        self._dispatch('stream_online', _stream)

    async def parse_stream_offline(self, data: sm.Offline) -> None:
        """
        Parse a stream offline event.
        """
        _stream = Offline(stream=data)
        self._dispatch('stream_offline', _stream)

    async def parse_user_update(self, data: us.Update) -> None:
        """
        Parse a user update event.
        """
        _update = UserUpdate(update=data)
        # Updating the broadcaster
        self.broadcaster.name = _update.name
        self.broadcaster.display_name = _update.display_name
        self.broadcaster.description = _update.description
        self.broadcaster.email = _update.email
        if 'user_update' in self.events:
            self._dispatch('user_update', _update)
