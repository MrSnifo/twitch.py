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

from ..user import SpecificBroadcaster, SpecificUser
from typing import TypedDict, Optional, Literal


class BaseReward(TypedDict):
    id: str
    title: str
    cost: int
    prompt: str


class OptionalImage(TypedDict):
    url_1x: Optional[str]
    url_2x: Optional[str]
    url_4x: Optional[str]


class Image(TypedDict):
    url_1x: str
    url_2x: str
    url_4x: str


class MaxValue(TypedDict):
    is_enabled: bool
    value: int


class Cooldown(TypedDict):
    is_enabled: bool
    seconds: int


class Reward(SpecificBroadcaster, BaseReward):
    """
    Type: Channel Points Custom Reward Add
    Name: `channel.channel_points_custom_reward.add`
    Version: 1

    Type: Channel Points Custom Reward Update
    Name: `channel.channel_points_custom_reward.update`
    Version: 1

    Type: Channel Points Custom Reward Remove
    Name: `channel.channel_points_custom_reward.remove`
    Version: 1
    """
    is_enabled: bool
    is_paused: bool
    is_in_stock: bool
    is_user_input_required: bool
    should_redemptions_skip_request_queue: bool
    max_per_stream: MaxValue
    max_per_user_per_stream: MaxValue
    background_color: str
    image: OptionalImage
    default_image: Image
    global_cooldown: Cooldown
    cooldown_expires_at: Optional[str]
    redemptions_redeemed_current_stream: Optional[int]


class Redemption(SpecificBroadcaster, SpecificUser):
    """
    Type: Channel Points Custom Reward Redemption Add
    Name: `channel.channel_points_custom_reward_redemption.add`
    Version: 1

    Type: Channel Points Custom Reward Redemption Update
    Name: `channel.channel_points_custom_reward_redemption.update`
    Version: 1
    """
    id: str
    status: Literal['unknown', 'unfulfilled', 'fulfilled', 'canceled']
    reward: BaseReward
    redeemed_at: str
