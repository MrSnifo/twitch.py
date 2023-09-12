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

from .user import (Broadcaster, SpecificBroadcaster,
                   SpecificUser)
from typing import TypedDict, Optional, Literal

Images = TypedDict('Images', {'url_1x': str, 'url_2x': str, 'url_4x': str})


# ---------------------------------------
#               + Reward +
# ---------------------------------------
class BaseReward(TypedDict):
    id: str
    cost: int
    title: str
    prompt: str


MaxPerStreamSetting = TypedDict('MaxPerStreamSetting', {'is_enabled': bool, 'max_per_stream': int})
MaxPerUserPerStreamSetting = TypedDict('MaxPerUserPerStreamSetting',
                                       {'is_enabled': bool, 'max_per_user_per_stream': int})
GlobalCooldownSetting = TypedDict('GlobalCooldownSetting',
                                  {'is_enabled': bool, 'global_cooldown_seconds': int})


class Reward(Broadcaster, BaseReward):
    image: Optional[Images]
    is_paused: bool
    is_enabled: bool
    is_in_stock: bool
    default_image: Images
    background_color: str
    cooldown_expires_at: Optional[str]
    is_user_input_required: bool
    max_per_stream_setting: MaxPerStreamSetting
    global_cooldown_setting: GlobalCooldownSetting
    max_per_user_per_stream_setting: MaxPerUserPerStreamSetting
    redemptions_redeemed_current_stream: Optional[int]
    should_redemptions_skip_request_queue: bool


class RewardToJson(TypedDict):
    cost: int
    title: str
    prompt: str
    is_enabled: bool
    max_per_stream: int
    background_color: str
    is_user_input_required: bool
    global_cooldown_seconds: str
    max_per_user_per_stream: int
    is_max_per_stream_enabled: bool
    is_global_cooldown_enabled: bool
    is_max_per_user_per_stream_enabled: bool
    should_redemptions_skip_request_queue: bool


# -------------+ EventSub +-------------
EnableValue = TypedDict('EnableValue', {'is_enabled': bool, 'value': int})
EnableSeconds = TypedDict('EnableSeconds', {'is_enabled': bool, 'seconds': int})


class RewardEvent(SpecificBroadcaster, BaseReward):
    image: Optional[Images]
    is_paused: bool
    is_enabled: bool
    is_in_stock: bool
    default_image: Images
    max_per_stream: EnableValue
    global_cooldown: EnableSeconds
    background_color: str
    cooldown_expires_at: Optional[str]
    is_user_input_required: bool
    max_per_user_per_stream: EnableValue
    redemptions_redeemed_current_stream: Optional[int]
    should_redemptions_skip_request_queue: bool


# --------------------------------------
#         + Reward Redemption +
# --------------------------------------
RedemptionStatus = Literal['CANCELED', 'FULFILLED', 'UNFULFILLED']


class BaseRedemption(SpecificUser):
    id: str
    status: RedemptionStatus
    reward: BaseReward
    user_input: str
    redeemed_at: str


class Redemption(Broadcaster, BaseRedemption):
    pass


# -------------+ EventSub +-------------
class RedemptionEvent(SpecificBroadcaster, BaseRedemption):
    pass
