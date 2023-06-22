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

# Libraries
from typing import TypedDict, Dict


class SubscriptionPayload(TypedDict):
    """
    Represents a subscription with a name and a version.
    """
    name: str
    version: str


Subscriptions: Dict[str, SubscriptionPayload] = {
    'channel_update': {'name': 'channel.update', 'version': '1'},
    'follow': {'name': 'channel.follow', 'version': '2'},
    'subscribe': {'name': 'channel.subscribe', 'version': '1'},
    'subscription_end': {'name': 'channel.subscription.end', 'version': '1'},
    'subscription_gift': {'name': 'channel.subscription.gift', 'version': '1'},
    'subscription_message': {'name': 'channel.subscription.message', 'version': '1'},
    'cheer': {'name': 'channel.cheer', 'version': '1'},
    'raid': {'name': 'channel.raid', 'version': '1'},
    'ban': {'name': 'channel.ban', 'version': '1'},
    'unban': {'name': 'channel.unban', 'version': '1'},
    'moderator_add': {'name': 'channel.moderator.add', 'version': '1'},
    'moderator_remove': {'name': 'channel.moderator.remove', 'version': '1'},
    'points_reward_add': {'name': 'channel.channel_points_custom_reward.add', 'version': '1'},
    'points_reward_update': {'name': 'channel.channel_points_custom_reward.update', 'version': '1'},
    'points_reward_remove': {'name': 'channel.channel_points_custom_reward.remove', 'version': '1'},
    'points_reward_redemption': {'name': 'channel.channel_points_custom_reward_redemption.add', 'version': '1'},
    'points_reward_redemption_update': {'name': 'channel.channel_points_custom_reward_redemption.update',
                                        'version': '1'},
    'poll_begin': {'name': 'channel.poll.begin', 'version': '1'},
    'poll_progress': {'name': 'channel.poll.progress', 'version': '1'},
    'poll_end': {'name': 'channel.poll.end', 'version': '1'},
    'prediction_begin': {'name': 'channel.prediction.begin', 'version': '1'},
    'prediction_progress': {'name': 'channel.prediction.progress', 'version': '1'},
    'prediction_lock': {'name': 'channel.prediction.lock', 'version': '1'},
    'prediction_end': {'name': 'channel.prediction.end', 'version': '1'},
    'charity_campaign_donate': {'name': 'channel.charity_campaign.donate', 'version': '1'},
    'charity_campaign_start': {'name': 'channel.charity_campaign.start', 'version': '1'},
    'charity_campaign_progress': {'name': 'channel.charity_campaign.progress', 'version': '1'},
    'charity_campaign_stop': {'name': 'channel.charity_campaign.stop', 'version': '1'},
    'goal_begin': {'name': 'channel.goal.begin', 'version': '1'},
    'goal_progress': {'name': 'channel.goal.progress', 'version': '1'},
    'goal_end': {'name': 'channel.goal.end', 'version': '1'},
    'hype_train_begin': {'name': 'channel.hype_train.begin', 'version': '1'},
    'hype_train_progress': {'name': 'channel.hype_train.progress', 'version': '1'},
    'hype_train_end': {'name': 'channel.hype_train.end', 'version': '1'},
    'shield_mode_begin': {'name': 'channel.shield_mode.begin', 'version': '1'},
    'shield_mode_end': {'name': 'channel.shield_mode.end', 'version': '1'},
    'shoutout_create': {'name': 'channel.shoutout.create', 'version': '1'},
    'shoutout_receive': {'name': 'channel.shoutout.receive', 'version': '1'},
    'stream_online': {'name': 'stream.online', 'version': '1'},
    'stream_offline': {'name': 'stream.offline', 'version': '1'}}
