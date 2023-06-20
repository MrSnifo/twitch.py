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
from .utils import parse_rfc3339_timestamp
from .user import User

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .types.eventsub import hypertrain as ht
    from .types.eventsub import charity as ch
    from typing import Optional, Union, List
    from .types.eventsub import goal as gl
    from datetime import datetime



class CharityInfo:
    """
    Information about a charity.
    """

    def __init__(self, charity: ch.SpecificCharity):
        self.name: str = charity['charity_name']
        self.description: Optional[str] = charity.get('charity_description')
        self.logo: str = charity['charity_logo']
        self.website: Optional[str] = charity.get('charity_website')


class _CharityAmount:
    """
    Represents an amount with its value and currency.
    """
    __slots__ = ('value', 'currency')

    def __init__(self, *, amount: ch.Amount):
        self.value: float = (amount['value'] / 10 ** amount['decimal_places'])
        self.currency: str = amount['currency']

    def __repr__(self):
        return f'<_Amount value={self.value} currency={self.currency}>'


class Charity:
    """
    Represents a channel charity.
    """
    __slots__ = ('id', 'charity', 'current_amount', 'target_amount', '_started_at', '_stopped_at')

    def __init__(self, charity: Union[ch.Start, ch.Progress, ch.Stop]):
        self.id: str = charity['id']
        self.charity: CharityInfo = CharityInfo(charity=charity)
        self.current_amount: _CharityAmount = _CharityAmount(amount=charity['current_amount'])
        self.target_amount: _CharityAmount = _CharityAmount(amount=charity['target_amount'])
        self._started_at: Optional[str] = charity.get('started_at')
        self._stopped_at: Optional[str] = charity.get('stopped_at')

    def __repr__(self):
        return f'<Charity id={self.id} current_amount={self.current_amount.__repr__()}>'


class Donation:
    """
    Represents a donation made to a charity.
    """
    __slots__ = ('id', 'charity', 'user', 'amount')

    def __init__(self, donation: ch.Donation):
        self.id: str = donation['id']
        self.charity: CharityInfo = CharityInfo(charity=donation)
        self.user: User = User(user=donation)
        self.amount: _CharityAmount = _CharityAmount(amount=donation['amount'])

    def __repr__(self):
        return f'<Donation id={self.id} user={self.user.__repr__()} amount={self.amount.__repr__()}>'


class _GoalAmount:
    """
    Represents the amount and type of goal.
    """

    def __init__(self, goal: gl.Goal):
        self.value: int = goal['current_amount']
        self.type: str = goal['type']

    def __repr__(self):
        return f'<_GoalAmount value={self.value} type={self.type}>'


class Goal:
    """
    Represents a channel goal.
    """
    __slots__ = ('id', 'description', 'amount', 'started_at', 'is_achieved', '_ended_at')

    def __init__(self, goal: Union[gl.Begin, gl.Progress, gl.End]):
        self.id: str = goal['id']
        self.description: str = goal['description']
        self.amount: _GoalAmount = _GoalAmount(goal=goal)
        self.started_at: datetime = parse_rfc3339_timestamp(timestamp=goal['started_at'])
        self.is_achieved: bool = goal.get('is_achieved') or False
        self._ended_at: Optional[str] = goal.get('ended_at')

    def __repr__(self):
        return f'<Goal id={self.id} amount={self.amount.__repr__()} started_at={self.started_at}>'


class _Contributor:
    """
    Hyper train top contributor.
    """
    __slots__ = ('user', 'type', 'total')

    def __init__(self, *, contributor: ht.Contributor):
        self.user: User = User(user=contributor)
        self.type: str = contributor['type']
        self.total: int = contributor['total']

    def __repr__(self):
        return f'<_Contributor user={self.user.__repr__()} total={self.total} type={self.type}>'


class Train:
    """
    Hyper train progress.
    """
    __slots__ = ('progress', 'goal', 'expires_at', '_last_contribution')

    def __init__(self, train: ht.Begin):
        self.goal: int = train['goal']
        self.progress: int = train['progress']
        self.expires_at: datetime = parse_rfc3339_timestamp(timestamp=train['expires_at'])
        self._last_contribution: List[ht.Contributor] = train['last_contribution']

    def __repr__(self):
        return f'<_Train goal={self.goal} progress={self.progress} expires_at={self.expires_at}>'

    @property
    def last_contribution(self) -> List[_Contributor]:
        return [_Contributor(contributor=c) for c in self._last_contribution]


class HyperTrain:
    """
    Represents a channel Hyper Train.
    """
    __slots__ = ('__hypertrain', 'id', 'total', 'level', '_top_contributions', 'started_at', '_ended_at',
                 '_cooldown_ends_at')

    def __init__(self, hypertrain: Union[ht.Begin, ht.Progress, ht.End]):
        self.__hypertrain = hypertrain
        self.id: str = hypertrain['id']
        self.level: int = hypertrain['level']
        self.total: int = hypertrain['total']
        self._top_contributions: List[ht.Contributor] = hypertrain['top_contributions']
        self.started_at: datetime = parse_rfc3339_timestamp(timestamp=hypertrain['started_at'])
        self._ended_at: Optional[str] = hypertrain.get('ended_at')
        self._cooldown_ends_at: Optional[str] = hypertrain.get('cooldown_ends_at')

    def __repr__(self):
        return f'<HyperTrain id={self.id} level={self.level} total={self.total}>'

    @property
    def top_contributions(self) -> List[_Contributor]:
        return [_Contributor(contributor=c) for c in self._top_contributions]

    @property
    def train(self) -> Optional[Train]:
        if not self._ended_at:
            return Train(train=self.__hypertrain)
        return None

    @property
    def ended_at(self) -> Optional[datetime]:
        if self._ended_at:
            return parse_rfc3339_timestamp(timestamp=self._ended_at)
        return None

    @property
    def cooldown_ends_at(self) -> Optional[datetime]:
        if self._cooldown_ends_at:
            return parse_rfc3339_timestamp(timestamp=self._cooldown_ends_at)
        return None
