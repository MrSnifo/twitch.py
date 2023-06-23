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

from .utils import parse_rfc3339_timestamp
from .user import User

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .types.eventsub import reward as rd
    from datetime import datetime
    from typing import Optional

__all__ = ('Reward', 'Redemption')


class Image:
    """
    Represents a custom image for a reward.

    :param image: The image data.
    """

    def __init__(self, image: rd.Image) -> None:
        self.url_1x: str = image['url_1x']
        self.url_2x: str = image['url_2x']
        self.url_4x: str = image['url_4x']


class OptionalImage:
    """
    Represents an optional custom image for a reward.

    :param image: The image data.
    """

    def __init__(self, image: rd.OptionalImage) -> None:
        self.url_1x: Optional[str] = image['url_1x']
        self.url_2x: Optional[str] = image['url_2x']
        self.url_4x: Optional[str] = image['url_4x']


class MaxValue:
    """
    Represents a maximum value setting for a reward.

    :param data: The maximum value data.
    """

    def __init__(self, data: rd.MaxValue) -> None:
        self.is_enabled: bool = data['is_enabled']
        self.value: int = data['value']


class MaxCooldown:
    """
    Represents a maximum cooldown setting for a reward.

    :param data: The maximum cooldown data.
    """

    def __init__(self, data: rd.Cooldown) -> None:
        self.is_enabled: bool = data['is_enabled']
        self.seconds: int = data['seconds']


class Status:
    """
    Represents the status of a reward.

    :param reward: The reward data.
    """

    def __init__(self, reward: rd.Reward) -> None:
        self.is_enabled: bool = reward['is_enabled']
        self.is_paused: bool = reward['is_paused']
        self.is_in_stock: bool = reward['is_in_stock']


class Appearance:
    """
    Represents the appearance settings for a reward.

    :param reward: The reward data.
    """

    def __init__(self, reward: rd.Reward) -> None:
        self.title: str = reward['title']
        self.description: str = reward['prompt']
        self.background_color: str = reward['background_color']
        self.image: OptionalImage = OptionalImage(image=reward['image'])
        self.default_image: Image = Image(image=reward['default_image'])


class Options:
    """
    Represents the options for a reward.

    :param reward: The reward data.
    """

    def __init__(self, reward: rd.Reward) -> None:
        self.redemptions_skip_request_queue: bool = reward['should_redemptions_skip_request_queue']
        self.max_per_stream: MaxValue = MaxValue(data=reward['max_per_stream'])
        self.max_per_user_per_stream: MaxValue = MaxValue(data=reward['max_per_user_per_stream'])
        self.is_user_input_required: bool = reward['is_user_input_required']


class Cooldown:
    """
    Represents the cooldown settings for a reward.

    :param reward: The reward data.
    """

    def __init__(self, reward: rd.Reward) -> None:
        self.duration: MaxCooldown = MaxCooldown(data=reward['global_cooldown'])
        self._cooldown_expires_at: Optional[str] = reward['cooldown_expires_at']

    @property
    def expires_at(self) -> Optional[datetime]:
        if self._cooldown_expires_at:
            return parse_rfc3339_timestamp(timestamp=self._cooldown_expires_at)
        return None


class Reward:
    """
    Represents a channel reward.

    :param reward: The reward data.
    """

    def __init__(self, reward: rd.Reward) -> None:
        self.id: str = reward['id']
        self.cost: int = reward['cost']
        self.status: Status = Status(reward=reward)
        self.appearance: Appearance = Appearance(reward=reward)
        self.options: Options = Options(reward=reward)
        self.cooldown: Cooldown = Cooldown(reward=reward)
        self.redeemed_current_stream: Optional[int] = reward['redemptions_redeemed_current_stream']

    def __repr__(self) -> str:
        return f'<Reward id={self.id} redeemed_current_stream={self.redeemed_current_stream}>'


class RewardInfo:
    """
    Represents reward information.

    :param reward: The reward data.
    """

    def __init__(self, reward: rd.BaseReward) -> None:
        self.id: str = reward['id']
        self.title: str = reward['title']
        self.cost: int = reward['cost']
        self.description: str = reward['prompt']

    def __repr__(self) -> str:
        return f'<_Reward id={self.id} title={self.title} cost={self.cost}>'


class Redemption:
    """
    Represents a reward redemption.

    :param redemption: The redemption data.
    """

    def __init__(self, redemption: rd.Redemption) -> None:
        self.id: str = redemption['id']
        self.user: User = User(user=redemption)
        self.status: str = redemption['status']
        self.reward: RewardInfo = RewardInfo(reward=redemption['reward'])
        self.redeemed_at: datetime = parse_rfc3339_timestamp(timestamp=redemption['redeemed_at'])

    def __repr__(self) -> str:
        return f'<Redemption id={self.id} user={self.user} reward={self.reward.__repr__()}>'
