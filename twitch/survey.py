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
    from typing import Optional, List, Union, Literal
    from .types.eventsub import poll as pl
    from .types.eventsub import prediction as pd
    from datetime import datetime


class _Voting:
    """
    Represents voting settings for a poll.
    """

    __slots__ = ('enabled', 'amount_per_vote')

    def __init__(self, *, vote: pl.Voting):
        self.enabled: bool = vote['is_enabled']
        self.amount_per_vote: int = vote['amount_per_vote']

    def __repr__(self):
        return f'<Voting enabled={self.enabled} amount_per_vote={self.amount_per_vote}>'


class _Choice:
    """
    Represents a choice in a poll.
    """
    __slots__ = ('id', 'title', 'bits_votes', 'points_votes')

    def __init__(self, choice: Union[pl.Choice, pl.ChoicesCount]):
        self.id: str = choice['id']
        self.title: str = choice['title']
        self.bits_votes: int = choice.get('bits_votes') or 0
        self.points_votes: int = choice.get('channel_points_votes') or 0

    def __repr__(self):
        return f'<Choice id={self.id} title={self.title}>'


class Poll:
    """
    Represents a channel poll.
    """
    __slots__ = ('id', 'title', '_choices', 'bits_voting', 'points_voting', 'started_at',
                 '_ends_at', '_ended_at', '_status')

    def __init__(self, poll: Union[pl.Begin, pl.Progress, pl.End]):
        self.id: str = poll['id']
        self.title: str = poll['title']
        self._choices: List[Union[pl.Choice, pl.ChoicesCount]] = poll['choices']
        self.bits_voting: _Voting = _Voting(vote=poll['bits_voting'])
        self.points_voting: _Voting = _Voting(vote=poll['channel_points_voting'])
        self.started_at: datetime = parse_rfc3339_timestamp(timestamp=poll['started_at'])
        self._ends_at: Optional[str] = poll.get('ends_at')
        self._ended_at: Optional[str] = poll.get('ended_at')
        self._status: Literal['completed', 'archived', 'terminated'] = poll.get('status')

    def __repr__(self):
        return f'<Poll id={self.id} title={self.title}>'

    @property
    def choices(self) -> List[_Choice]:
        return [_Choice(choice=c) for c in self._choices]

    @property
    def is_ended(self):
        return self._ended_at is not None

    @property
    def status(self) -> Literal['active', 'completed', 'archived', 'terminated']:
        if self._ended_at:
            return self._status
        return 'active'

    @property
    def end_at(self) -> datetime:
        if self._ended_at is not None:
            return parse_rfc3339_timestamp(timestamp=self._ended_at)
        return parse_rfc3339_timestamp(timestamp=self._ends_at)


class _Predictor:
    """
    Represents a predictor in a prediction.
    """

    __slots__ = ('user', 'points_used', 'points_won', '_points_won')

    def __init__(self, predictor: pd.Predictor):
        self.user = User(user=predictor)
        self.points_used: int = predictor['channel_points_used']
        self.points_won: int = predictor['channel_points_won'] or 0
        self._points_won: Optional[int] = predictor['channel_points_won']

    @property
    def is_won(self) -> bool:
        return self._points_won is not None and self.points_won != 0

    def __repr__(self):
        return f'<Predictor user={self.user.__repr__()} points_won={self.points_won}>'


class _Outcome:
    """
    Represents an outcome in a prediction.
    """
    __slots__ = ('id', 'title', 'color', '_users', '_top_predictors')

    def __init__(self, outcome: Union[pd.BaseOutcome, pd.Outcome]):
        self.id: str = outcome['id']
        self.title: str = outcome['title']
        self.color: str = outcome['color']
        self._users: int = outcome.get('users') or 0
        self._top_predictors: Optional[List[pd.Predictor]] = outcome.get('top_predictors')

    def __repr__(self):
        return f'<Outcome user={self.id} title={self.title} color={self.color}>'

    @property
    def users(self) -> int:
        if self._top_predictors is None:
            return self._users
        return len(self._top_predictors)

    @property
    def top_predictors(self) -> List[_Predictor]:
        if self._top_predictors:
            return [_Predictor(predictor=p) for p in self._top_predictors]
        return []


class Prediction:
    """
    Represents a channel prediction.
    """
    __slots__ = ('id', 'title', '_outcomes', 'started_at', '_locks_at', '_locked_at', '_ended_at',
                 '_status')

    def __init__(self, *, prediction: Union[pd.Begin, pd.Progress, pd.Lock, pd.End]):
        self.id: str = prediction['id']
        self.title: str = prediction['title']
        self._outcomes: List[Union[pd.Outcome, pd.BaseOutcome]] = prediction['outcomes']
        self.started_at: datetime = parse_rfc3339_timestamp(timestamp=prediction['started_at'])
        self._locks_at: Optional[str] = prediction.get('locks_at')
        self._locked_at: Optional[str] = prediction.get('locked_at')
        self._ended_at: Optional[str] = prediction.get('ended_at')
        self._status: Optional[Literal['resolved', 'canceled']] = prediction.get('status')

    def __repr__(self):
        return f'<Prediction user={self.id} title={self.title}>'

    @property
    def outcomes(self) -> List[_Outcome]:
        return [_Outcome(outcome=o) for o in self._outcomes]

    @property
    def status(self) -> Literal['open', 'locked', 'resolved', 'canceled']:
        if self._locks_at:
            return 'open'
        if self._locked_at:
            return 'locked'
        return self._status

    @property
    def is_locked(self) -> bool:
        if self._locked_at or self._ended_at:
            return True
        return False

    @property
    def is_ended(self) -> bool:
        if self._ended_at:
            return True
        return False

    @property
    def lock_at(self) -> Optional[datetime]:
        if self._locks_at:
            return parse_rfc3339_timestamp(timestamp=self._locks_at)
        if self._locked_at:
            return parse_rfc3339_timestamp(timestamp=self._locked_at)
        return None

    @property
    def ended_at(self) -> Optional[datetime]:
        if self._ended_at:
            return parse_rfc3339_timestamp(timestamp=self._ended_at)
        return None
