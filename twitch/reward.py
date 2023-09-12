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

from .utils import Value, Images, convert_rfc3339
from .user import BaseUser

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .types import reward as RewardTypes
    from typing import Optional, Union
    from datetime import datetime

__all__ = ('BaseReward', 'Reward', 'Redemption')


class BaseReward:
    """
    Represents base reward.

    Attributes
    ----------
    id: str
        The unique ID of the reward.
    cost: int
        The cost of redeeming the reward in channel points.
    title: str
        The title of the reward.
    prompt: Optional[str]
        An optional prompt for the reward.

    Methods
    -------
    __str__() -> str
        Returns the title of the BaseReward.
    __eq__(other: object) -> bool
        Checks if two BaseReward instances are equal based on their IDs.
    __ne__(other: object) -> bool
        Checks if two BaseReward instances are not equal.
    """
    __slots__ = ('id', 'cost', 'title', 'prompt')

    if TYPE_CHECKING:
        id: str
        cost: int
        title: str
        prompt: Optional[str]

    def __init__(self, data: RewardTypes.BaseReward) -> None:
        self._form_data(data=data)

    def __repr__(self) -> str:
        return f'<BaseReward id={self.id} cost={self.cost}>'

    def __str__(self) -> str:
        return self.title

    def __eq__(self, other: object) -> bool:
        if isinstance(other, BaseReward):
            return self.id == other.id
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def _form_data(self, data: RewardTypes.BaseReward) -> None:
        self.id = data['id']
        self.cost = data['cost']
        self.title = data['title']
        self.prompt = data['prompt'] or None


class Reward(BaseReward):
    """
    Represents channel points reward.

    Attributes
    ----------
    image: Optional[Images]
        An optional image associated with the reward.
    is_paused: bool
        Indicates if the reward is paused.
    is_enabled: bool
        Indicates if the reward is enabled.
    is_in_stock: bool
        Indicates if the reward is in stock.
    default_image: Images
        The default image associated with the reward.
    max_per_stream: Value
        The maximum number of times the reward can be redeemed per stream.
    global_cooldown: Value
        The global cooldown setting for the reward.
    background_color: str
        The background color of the reward.
    cooldown_expires_at: Optional[str]
        An optional expiration time for the reward's cooldown.
    is_user_input_required: bool
        Indicates if user input is required for redeeming the reward.
    max_per_user_per_stream: Value
        The maximum number of times the reward can be redeemed by a user per stream.
    redemptions_redeemed_current_stream: Optional[int]
        An optional count of redemptions redeemed in the current stream.
    should_redemptions_skip_request_queue: bool
        Indicates if redemptions should skip the request queue when redeemed.

    Methods
    -------
    __bool__() -> bool
        Returns True if the reward is enabled.
    """
    __slots__ = ('image', 'is_paused', 'is_enabled', 'is_in_stock', 'default_image', 'max_per_stream',
                 'global_cooldown', 'background_color', 'cooldown_expires_at', 'is_user_input_required',
                 'max_per_user_per_stream', 'redemptions_redeemed_current_stream',
                 'should_redemptions_skip_request_queue')

    if TYPE_CHECKING:
        image: Optional[Images]
        is_paused: bool
        is_enabled: bool
        is_in_stock: bool
        default_image: Images
        max_per_stream: Value
        global_cooldown: Value
        background_color: str
        cooldown_expires_at: Optional[str]
        is_user_input_required: bool
        max_per_user_per_stream: Value
        redemptions_redeemed_current_stream: Optional[int]
        should_redemptions_skip_request_queue: bool

    def __init__(self, data: Union[RewardTypes.Reward, RewardTypes.RewardEvent]) -> None:
        super().__init__(data=data)
        self._form_data(data=data)

    def __repr__(self) -> str:
        return (
            f'<Reward id={self.id} is_enabled={self.is_enabled} is_paused={self.is_paused} cost={self.cost}>'
        )

    def __bool__(self) -> bool:
        return self.is_enabled

    def _form_data(self, data: Union[RewardTypes.Reward, RewardTypes.RewardEvent]) -> None:
        super()._form_data(data=data)
        self.image = Images(data=data['image']) if data['image'] else None
        self.is_paused = data['is_paused']
        self.is_enabled = data['is_enabled']
        self.is_in_stock = data['is_in_stock']
        self.default_image = Images(data=data['default_image'])
        self.max_per_stream = Value(
            data=data.get('max_per_stream_setting', data.get('max_per_stream')))
        self.global_cooldown = Value(
            data=data.get('global_cooldown_setting', data.get('global_cooldown')))
        self.background_color = data['background_color']
        self.cooldown_expires_at = convert_rfc3339(data['cooldown_expires_at'])
        self.is_user_input_required = data['is_user_input_required']
        self.max_per_user_per_stream = Value(
            data=data.get('max_per_user_per_stream_setting', data.get('max_per_user_per_stream')))
        self.redemptions_redeemed_current_stream = data['redemptions_redeemed_current_stream']
        self.should_redemptions_skip_request_queue = data['should_redemptions_skip_request_queue']

    def to_json(self) -> RewardTypes.RewardToJson:
        # This is useful when you want to recreate the same reward.
        return ({
            'title': self.title,
            'cost': self.cost,
            'prompt': self.prompt or '',
            'is_enabled': self.is_enabled,
            'background_color': self.background_color,
            'is_user_input_required': self.is_user_input_required,
            'is_max_per_stream_enabled': self.max_per_stream.is_enabled,
            'max_per_stream': self.max_per_stream.value,
            'is_max_per_user_per_stream_enabled': self.max_per_user_per_stream.is_enabled,
            'max_per_user_per_stream': self.max_per_user_per_stream.value,
            'is_global_cooldown_enabled': self.global_cooldown.is_enabled,
            'global_cooldown_seconds': self.global_cooldown.value,
            'should_redemptions_skip_request_queue': self.should_redemptions_skip_request_queue
        })


class Redemption:
    """
    Represents a redemption of a reward by a viewer.

    Attributes
    ----------
    id: str
        The unique ID of the redemption.
    user: BaseUser
        The user who redeemed the reward.
    reward: BaseReward
        The reward that was redeemed.
    status: str
        The status of the redemption (e.g., "FULFILLED").
    user_input: str
        The user input associated with the redemption.
    redeemed_at: datetime
        The date and time when the reward was redeemed.

    Methods
    -------
    __bool__() -> bool
        Returns True if the redemption status is "FULFILLED".
    """
    __slots__ = ('id',  'user', 'reward', 'status', 'user_input', 'redeemed_at')

    if TYPE_CHECKING:
        id: str
        user: BaseUser
        reward: BaseReward
        status: str
        user_input: str
        redeemed_at: datetime

    def __init__(self, data: Union[RewardTypes.Redemption, RewardTypes.RedemptionEvent]) -> None:
        self._form_data(data=data)

    def __repr__(self) -> str:
        return f'<Redemption id={self.id} status={self.status} redeemed_at={self.redeemed_at}>'

    def __bool__(self) -> bool:
        return self.status == 'FULFILLED'

    def _form_data(self, data: Union[RewardTypes.Redemption, RewardTypes.RedemptionEvent]) -> None:
        self.id = data['id']
        self.user = BaseUser(data, prefix='user_')
        self.reward = BaseReward(data=data['reward'])
        self.status = data['status']
        self.user_input = data['user_input']
        self.redeemed_at = convert_rfc3339(data['redeemed_at'])
