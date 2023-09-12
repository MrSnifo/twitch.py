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

from .utils import convert_rfc3339
from .user import BaseUser
from .chat import Message

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .types import alerts as AlertsTypes
    from typing import Optional, Union, List
    from datetime import datetime

__all__ = ('Raider', 'Cheerer', 'Subscriber', 'Gifter', 'Goal', 'Contributor', 'HypeTrain')


# -----------------------------
#       + Channel Raid +
# -----------------------------
class Raider(BaseUser):
    """
    Represents a raider who raids a Twitch channel.

    Attributes
    ----------
    viewers: int
        The number of viewers who joined the channel during the raid.

    Methods
    -------
    __int__() -> int
        Returns the number of viewers as an integer.
    """
    __slots__ = ('viewers',)

    if TYPE_CHECKING:
        viewers: int

    def __init__(self, data: AlertsTypes.RaidEvent) -> None:
        super().__init__(data, prefix='from_broadcaster_user_')
        self._update_data(data=data)

    def __repr__(self) -> str:
        return f'<Raider name={self.name} viewers={self.viewers}>'

    def __int__(self) -> int:
        return self.viewers

    def _update_data(self, data: AlertsTypes.RaidEvent) -> None:
        super()._update_data(data=data)
        self.viewers = data['viewers']


# -----------------------------
#       + Channel Cheer +
# -----------------------------
class Cheerer(BaseUser):
    """
    Represents a user who cheers bits in a Twitch channel.

    Attributes
    ----------
    bits: int
        The number of bits cheered by the user.
    is_anonymous: bool
        Indicates whether the cheer was made anonymously.

    Methods
    -------
    __int__() -> int
        Returns the number of bits cheered as an integer.
    """
    __slots__ = ('bits', 'is_anonymous')
    if TYPE_CHECKING:
        bits: int
        is_anonymous: bool

    def __init__(self, data: AlertsTypes.CheerEvent) -> None:
        super().__init__(data, prefix='user_')
        self._update_data(data=data)

    def __repr__(self) -> str:
        return f'<Cheerer bits={self.bits} name={self.name} is_anonymous={self.is_anonymous}>'

    def __int__(self) -> int:
        return self.bits

    def _update_data(self, data: AlertsTypes.CheerEvent) -> None:
        super()._update_data(data=data)
        self.bits = data['bits']
        self.is_anonymous = data['is_anonymous']


class Subscriber(BaseUser):
    """
    Represents a subscriber to a Twitch channel.

    Attributes
    ----------
    tier: str
        The subscription tier (e.g., "1000", "2000", "3000").
    is_gift: bool
        Indicates whether the subscription was a gift.
    duration_months: int
        The duration of the subscription in months.
    is_resubscribe: bool
        Indicates whether this is a resubscription.
    message: Optional[Message]
        The subscriber's message (if available).
    streak_months: Optional[int]
        The number of consecutive months subscribed (if available).
    cumulative_months: int
        The total cumulative months subscribed.
    """
    __slots__ = ('tier', 'is_gift', 'duration_months', 'is_resubscribe', 'message', 'streak_months',
                 'cumulative_months')

    if TYPE_CHECKING:
        tier: str
        is_gift: bool
        message: Optional[Message]
        streak_months: Optional[int]
        is_resubscribe: bool
        duration_months: int
        cumulative_months: int

    def __init__(self, data: AlertsTypes.SubscribeEvent) -> None:
        super().__init__(data=data, prefix='user_')
        self._update_data(data=data)

    def __repr__(self) -> str:
        return (
            f'<Subscriber name={self.name} tier={self.tier} is_gift={self.is_gift} '
            f'is_resubscribe={self.is_resubscribe}>'
        )

    def _update_data(self, data: Union[AlertsTypes.SubscribeEvent, AlertsTypes.ReSubscribeEvent]) -> None:
        super()._update_data(data=data)
        self.tier: str = data['tier']
        self.is_gift: bool = data.get('is_gift', False)
        tiers = {'1000': 1, '2000': 3, '3000': 6}
        _message = data.get('message')
        self.is_resubscribe: bool = _message is not None
        self.message: Message = Message(data=_message) if _message else None
        self.duration_months: int = data.get('duration_months', tiers[self.tier])
        self.cumulative_months: int = data.get('cumulative_months', 0)
        self.streak_months: Optional[int] = data.get('streak_months') if _message else 0


# -----------------------------
#       + Channel Gifts +
# -----------------------------
class Gifter(BaseUser):
    """
    Represents a user who gifted subscriptions in a Twitch channel.

    Attributes
    ----------
    tier: str
        The tier of the gifted subscriptions (e.g., "1000", "2000", "3000").
    total: int
        The total number of subscriptions gifted.
    is_anonymous: bool
        Indicates whether the gifter remained anonymous.
    cumulative_total: Optional[str]
        The cumulative total of gifted subscriptions (if available).
    """
    __slots__ = ('tier', 'user', 'total', 'is_anonymous', 'cumulative_total')

    if TYPE_CHECKING:
        tier: str
        total: int
        is_anonymous: bool
        cumulative_total: Optional[str]

    def __init__(self, data: AlertsTypes.GiftSubsEvent) -> None:
        super().__init__(data, prefix='user_')
        self._update_data(data=data)

    def __repr__(self) -> str:
        return (
            f'<Gifter total={self.total} name={self.name} tier={self.tier} is_anonymous={self.is_anonymous}>'
        )

    def _update_data(self, data: AlertsTypes.GiftSubsEvent) -> None:
        super()._update_data(data=data)
        self.tier = data['tier']
        self.total = data['total']
        self.is_anonymous = data['is_anonymous']
        self.cumulative_total = data['cumulative_total']


# -------------------------
#      + Channel Goal +
# -------------------------
class Goal:
    """
    Represents a goal set in a Twitch channel.

    Attributes
    ----------
    id: int
        The unique identifier of the goal.
    type: str
        The type or category of the goal.
    ended_at: Optional[datetime]
        The date and time when the goal ended (if ended).
    is_ended: bool
        Indicates whether the goal has ended.
    started_at: datetime
        The date and time when the goal started.
    description: str
        The description or title of the goal.
    is_achieved: bool
        Indicates whether the goal has been achieved.
    target_amount: int
        The target amount or goal value.
    current_amount: int
        The current amount or progress toward the goal.

    Methods
    -------
    __bool__() -> bool
        Returns True if the goal has not ended, False otherwise.
    __int__() -> int
        Returns the current amount as an integer.
    """
    __slots__ = ('id', 'type', 'ended_at', 'is_ended', 'started_at', 'description', 'is_achieved',
                 'target_amount', 'current_amount')

    if TYPE_CHECKING:
        id: int
        type: str
        ended_at: Optional[datetime]
        is_ended: bool
        started_at: datetime
        description: str
        is_achieved: bool
        target_amount: int
        current_amount: int

    def __init__(self, data: Union[AlertsTypes.Goal,
                                   Union[AlertsTypes.GoalBeginProgressEvent,
                                         AlertsTypes.GoalEndEvent]]) -> None:
        self._form_data(data=data)

    def __repr__(self) -> str:
        return (
            f'<Goal id={self.id} type={self.type} target_amount={self.target_amount} '
            f'current_amount={self.current_amount}>'
        )

    def __bool__(self) -> bool:
        return not self.is_ended

    def __int__(self) -> int:
        return self.current_amount

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Goal):
            return self.id == other.id
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def _form_data(self, data: Union[AlertsTypes.Goal,
                                     Union[AlertsTypes.GoalBeginProgressEvent,
                                           AlertsTypes.GoalEndEvent]]) -> None:
        self.id = data['id']
        self.type = data['type']
        self.description = data['description']
        self.target_amount = data['target_amount']
        self.current_amount = data['current_amount']
        # Missing in Eventsub.
        _started_at: Optional[str] = data.get('started_at')
        # EventSub part.
        _created_at: Optional[str] = data.get('created_at')
        self.started_at = convert_rfc3339(timestamp=(_created_at or _started_at))
        # Missing on ``Begin & Progress`` Event.
        self.is_achieved: bool = data.get('is_achieved', False)
        self.ended_at = convert_rfc3339(data.get('ended_at'))
        self.is_ended = self.ended_at is not None


# -------------------------
#       + HypeTrain +
# -------------------------
class Contributor:
    """
    Represents a contributor to a Hype Train event.

    Attributes
    ----------
    type: str
        The type of contribution (e.g., "BITS", "SUBS").
    total: int
        The total amount contributed.
    user_id: str
        The unique identifier of the contributing user.

    Methods
    -------
    __int__() -> int
        Returns the total amount contributed as an integer.
    __eq__(other: object) -> bool
        Checks if two Contributors have the same user_id.
    __ne__(other: object) -> bool
        Checks if two Contributors have different user_ids.
    """
    __slots__ = ('type', 'total', 'user_id')

    if TYPE_CHECKING:
        type: str
        total: int
        user_id: str

    def __init__(self, data: Union[AlertsTypes.HypeTrainContributor,
                                   AlertsTypes.HypeTrainContributorEvent]) -> None:
        self._form_data(data=data)

    def __repr__(self) -> str:
        return f'<Contributor user_id={self.user_id} type={self.type} total={self.total}>'

    def __int__(self) -> int:
        return self.total

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Contributor):
            return self.user_id == other.user_id
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def _form_data(self, data: Union[AlertsTypes.HypeTrainContributor,
                                     AlertsTypes.HypeTrainContributorEvent]) -> None:
        self.type = data['type'].upper()
        self.total = data['total']
        self.user_id = data.get('user', data.get('user_id'))


class HypeTrain:
    """
    Represents a Hype Train event in a Twitch channel.

    Attributes
    ----------
    id: str
        The unique identifier of the Hype Train event.
    goal: str
        The goal amount set for the Hype Train.
    level: int
        The current level of the Hype Train.
    total: int
        The total amount contributed to the Hype Train.
    end_time: datetime
        The date and time when the Hype Train ends.
    started_at: datetime
        The date and time when the Hype Train started.
    cooldown_end_time: Optional[str]
        The date and time when the Hype Train cooldown ends (if applicable).
    last_contribution: Optional[Contributor]
        The last contributor to the Hype Train (if available).
    top_contributions: List[Contributor]
        A list of the top contributors to the Hype Train.

    Methods
    -------
    __eq__(other: object) -> bool
        Checks if two HypeTrains have the same id.
    __ne__(other: object) -> bool
        Checks if two HypeTrains have different ids.
    """
    if TYPE_CHECKING:
        id: str
        goal: str
        level: int
        total: int
        end_time: datetime
        started_at: datetime
        cooldown_end_time: Optional[str]
        last_contribution: Optional[Contributor]
        top_contributions: List[Contributor]

    def __init__(self, data):
        self._form_data(data=data)

    def __repr__(self) -> str:
        return (
            f'<HypeTrain id={self.id} level={self.level} total={self.total} started_at={self.started_at}>'
        )

    def __int__(self) -> int:
        return self.total

    def __eq__(self, other: object) -> bool:
        if isinstance(other, HypeTrain):
            return self.id == other.id
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def _form_data(self, data: Union[AlertsTypes.HypeTrain, Union[AlertsTypes.HypeTrainBeginProgressEvent,
                                                                  AlertsTypes.HypeTrainEndEvent]]) -> None:
        self.id = data['id']
        self.total = data['total']
        self.level = data['level']
        self.started_at = convert_rfc3339(data['started_at'])
        self.cooldown_end_time = data.get('cooldown_end_time') or None
        self.goal = data.get('goal', 0)
        self.top_contributions = [Contributor(data=c) for c in data['top_contributions']]
        # Missing in HypeTrain End event.
        _expires_at: Optional[str] = data.get('expires_at')
        self.last_contribution = None
        if data.get('last_contribution'):
            self.last_contribution = Contributor(data=data['last_contribution'])
        _ended_at: Optional[str] = data.get('ended_at')
        self.end_time = convert_rfc3339(_expires_at or _ended_at)
