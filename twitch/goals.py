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
from .user import User, Contributor

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .types.eventsub import hypertrain as ht
    from .types.eventsub import charity as ch
    from typing import Optional, Union, List
    from .types.eventsub import goal as gl
    from datetime import datetime

__all__ = ('Charity', 'Donation', 'Goal', 'Train', 'HyperTrain')


class CharityInfo:
    """
    Information about a charity.

    :param charity: A dictionary containing charity information.
    """
    __slots__ = ('name', 'description', 'logo', 'website')

    def __init__(self, charity: ch.SpecificCharity) -> None:
        self.name: str = charity['charity_name']
        self.description: Optional[str] = charity.get('charity_description')
        self.logo: str = charity['charity_logo']
        self.website: Optional[str] = charity.get('charity_website')

    def __repr__(self) -> str:
        return f'<CharityInfo name={self.name} description={self.description}>'


class CharityAmount:
    """
    Represents an amount with its value and currency.

    :param amount: A dictionary containing amount information.
    """
    __slots__ = ('value', 'currency')

    def __init__(self, amount: ch.Amount) -> None:
        self.value: float = (amount['value'] / 10 ** amount['decimal_places'])
        self.currency: str = amount['currency']

    def __repr__(self) -> str:
        return f'<_Amount value={self.value} currency={self.currency}>'


class Charity:
    """
    Represents a channel charity.

    :param charity: An object representing a charity.
    """
    __slots__ = ('id', 'charity', 'current_amount', 'target_amount', '_started_at', '_stopped_at')

    def __init__(self, charity: Union[ch.Start, ch.Progress, ch.Stop]) -> None:
        self.id: str = charity['id']
        self.charity: CharityInfo = CharityInfo(charity=charity)
        self.current_amount: CharityAmount = CharityAmount(amount=charity['current_amount'])
        self.target_amount: CharityAmount = CharityAmount(amount=charity['target_amount'])
        self._started_at: Optional[str] = charity.get('started_at')
        self._stopped_at: Optional[str] = charity.get('stopped_at')

    @property
    def started_at(self) -> Optional[datetime]:
        """The datetime when the charity started."""
        return parse_rfc3339_timestamp(self._started_at) if self._started_at else None

    @property
    def stopped_at(self) -> Optional[datetime]:
        """The datetime when the charity stopped."""
        return parse_rfc3339_timestamp(self._stopped_at) if self._stopped_at else None


class Donation:
    """
    Represents a donation made to a charity.

    :param donation: An object representing a donation.
    """
    __slots__ = ('id', 'charity', 'user', 'amount')

    def __init__(self, donation: ch.Donation) -> None:
        self.id: str = donation['id']
        self.charity: CharityInfo = CharityInfo(charity=donation)
        self.user: User = User(user=donation)
        self.amount: CharityAmount = CharityAmount(amount=donation['amount'])

    def __repr__(self) -> str:
        return f'<Donation id={self.id} user={self.user.__repr__()}>'


class GoalAmount:
    """
    Represents the amount and type of goal.

    :param goal: A dictionary containing goal information.
    """

    def __init__(self, goal: gl.Goal) -> None:
        self.value: int = goal['current_amount']
        self.type: str = goal['type']

    def __repr__(self) -> str:
        return f'<_GoalAmount value={self.value} type={self.type}>'


class Goal:
    """
    Represents a channel goal.

    :param goal: An object representing a goal.
    """
    __slots__ = ('id', 'description', 'amount', 'started_at', 'is_achieved', '_ended_at')

    def __init__(self, goal: Union[gl.Begin, gl.Progress, gl.End]) -> None:
        self.id: str = goal['id']
        self.description: str = goal['description']
        self.amount: GoalAmount = GoalAmount(goal=goal)
        self.started_at: datetime = parse_rfc3339_timestamp(goal['started_at'])
        self.is_achieved: bool = goal.get('is_achieved') or False
        self._ended_at: Optional[str] = goal.get('ended_at')

    def __repr__(self) -> str:
        return f'<Goal id={self.id} amount={self.amount.__repr__()} started_at={self.started_at}>'

    @property
    def ended_at(self) -> Optional[datetime]:
        """The datetime when the goal ended."""
        return parse_rfc3339_timestamp(self._ended_at) if self._ended_at else None


class Train:
    """
    Hyper train progress.
    """
    __slots__ = ('progress', 'goal', 'expires_at', '_last_contribution')

    def __init__(self, train: ht.Begin) -> None:
        self.goal: int = train['goal']
        self.progress: int = train['progress']
        self.expires_at: datetime = parse_rfc3339_timestamp(train['expires_at'])
        self._last_contribution: List[ht.Contributor] = train['last_contribution']

    def __repr__(self) -> str:
        return f'<_Train goal={self.goal} progress={self.progress} expires_at={self.expires_at}>'

    @property
    def last_contribution(self) -> List[Contributor]:
        """The list of top contributors in the last contribution."""
        return [Contributor(contributor=c) for c in self._last_contribution]


class HyperTrain:
    """
    Represents a channel Hyper Train.

    :param hypertrain: An object representing a Hyper Train.
    """
    __slots__ = (
        '__hypertrain', 'id', 'total', 'level', '_top_contributions', 'started_at', '_ended_at',
        '_cooldown_ends_at')

    def __init__(self, hypertrain: Union[ht.Begin, ht.Progress, ht.End]) -> None:
        self.__hypertrain = hypertrain
        self.id: str = hypertrain['id']
        self.level: int = hypertrain['level']
        self.total: int = hypertrain['total']
        self._top_contributions: List[ht.Contributor] = hypertrain['top_contributions']
        self.started_at: datetime = parse_rfc3339_timestamp(hypertrain['started_at'])
        self._ended_at: Optional[str] = hypertrain.get('ended_at')
        self._cooldown_ends_at: Optional[str] = hypertrain.get('cooldown_ends_at')

    def __repr__(self) -> str:
        return f'<HyperTrain id={self.id} level={self.level} total={self.total}>'

    @property
    def top_contributions(self) -> List[Contributor]:
        """The list of top contributors in the Hyper Train."""
        return [Contributor(contributor=c) for c in self._top_contributions]

    @property
    def train(self) -> Optional[Train]:
        """The Hyper Train progress if it's ongoing, None otherwise."""
        if not self._ended_at:
            return Train(train=self.__hypertrain)
        return None

    @property
    def ended_at(self) -> Optional[datetime]:
        """The datetime when the Hyper Train ended."""
        return parse_rfc3339_timestamp(self._ended_at) if self._ended_at else None

    @property
    def cooldown_ends_at(self) -> Optional[datetime]:
        """The datetime when the Hyper Train cooldown ends."""
        return parse_rfc3339_timestamp(self._cooldown_ends_at) if self._cooldown_ends_at else None
