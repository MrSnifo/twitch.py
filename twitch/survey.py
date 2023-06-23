from __future__ import annotations

from .utils import parse_rfc3339_timestamp
from .user import Predictor

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, List, Union, Literal
    from .types.eventsub import prediction as pd
    from .types.eventsub import poll as pl
    from datetime import datetime


class Voting:
    """
    Represents voting settings for a poll.

    :param vote: The voting settings for the poll.
    """
    __slots__ = ('enabled', 'amount_per_vote')

    def __init__(self, vote: pl.Voting) -> None:
        self.enabled: bool = vote['is_enabled']
        self.amount_per_vote: int = vote['amount_per_vote']

    def __repr__(self):
        return f'<Voting enabled={self.enabled} amount_per_vote={self.amount_per_vote}>'


class Choice:
    """
    Represents a choice in a poll.

    :param choice: The choice data for the poll.
    """
    __slots__ = ('id', 'title', 'bits_votes', 'points_votes')

    def __init__(self, choice: Union[pl.Choice, pl.ChoicesCount]) -> None:
        self.id: str = choice['id']
        self.title: str = choice['title']
        self.bits_votes: int = choice.get('bits_votes') or 0
        self.points_votes: int = choice.get('channel_points_votes') or 0

    def __repr__(self) -> str:
        return f'<Choice id={self.id} title={self.title}>'


class Poll:
    """
    Represents a channel poll.

    :param poll: The poll data.
    """
    __slots__ = ('id', 'title', '_choices', 'bits_voting', 'points_voting', 'started_at',
                 '_ends_at', '_ended_at', '_status')

    def __init__(self, poll: Union[pl.Begin, pl.Progress, pl.End]) -> None:
        self.id: str = poll['id']
        self.title: str = poll['title']
        self._choices: List[Union[pl.Choice, pl.ChoicesCount]] = poll['choices']
        self.bits_voting: Voting = Voting(vote=poll['bits_voting'])
        self.points_voting: Voting = Voting(vote=poll['channel_points_voting'])
        self.started_at: datetime = parse_rfc3339_timestamp(timestamp=poll['started_at'])
        self._ends_at: Optional[str] = poll.get('ends_at')
        self._ended_at: Optional[str] = poll.get('ended_at')
        self._status: Literal['completed', 'archived', 'terminated'] = poll.get('status')

    def __repr__(self) -> str:
        return f'<Poll id={self.id} title={self.title}>'

    @property
    def choices(self) -> List[Choice]:
        """
        Get the list of choices for the poll.

        :return: The list of poll choices.
        """
        return [Choice(choice=c) for c in self._choices]

    @property
    def is_ended(self) -> bool:
        """
        Check if the poll has ended.

        :return: True if the poll has ended, False otherwise.
        """
        return self._ended_at is not None

    @property
    def status(self) -> Literal['active', 'completed', 'archived', 'terminated']:
        """
        Get the status of the poll.

        :return: The status of the poll.
        """
        if self._ended_at:
            return self._status
        return 'active'

    @property
    def end_at(self) -> datetime:
        """
        Get the end timestamp of the poll.

        :return: The end timestamp of the poll.
        """
        if self._ended_at is not None:
            return parse_rfc3339_timestamp(timestamp=self._ended_at)
        return parse_rfc3339_timestamp(timestamp=self._ends_at)


class Outcome:
    """
    Represents an outcome in a prediction.

    :param outcome: The outcome data.
    """
    __slots__ = ('id', 'title', 'color', '_users', '_top_predictors')

    def __init__(self, outcome: Union[pd.BaseOutcome, pd.Outcome]) -> None:
        self.id: str = outcome['id']
        self.title: str = outcome['title']
        self.color: str = outcome['color']
        self._users: int = outcome.get('users') or 0
        self._top_predictors: Optional[List[pd.Predictor]] = outcome.get('top_predictors')

    def __repr__(self) -> str:
        return f'<Outcome user={self.id} title={self.title} color={self.color}>'

    @property
    def users(self) -> int:
        """
        Get the number of users associated with the outcome.

        :return: The number of users associated with the outcome.
        """
        if self._top_predictors is None:
            return self._users
        return len(self._top_predictors)

    @property
    def top_predictors(self) -> List[Predictor]:
        """
        Get the list of top predictors for the outcome.

        :return: The list of top predictors.
        """
        if self._top_predictors:
            return [Predictor(predictor=p) for p in self._top_predictors]
        return []


class Prediction:
    """
    Represents a channel prediction.

    :param prediction: The prediction data.
    """
    __slots__ = ('id', 'title', '_outcomes', 'started_at', '_locks_at', '_locked_at', '_ended_at',
                 '_status')

    def __init__(self, prediction: Union[pd.Begin, pd.Progress, pd.Lock, pd.End]) -> None:
        self.id: str = prediction['id']
        self.title: str = prediction['title']
        self._outcomes: List[Union[pd.BaseOutcome, pd.Outcome]] = prediction['outcomes']
        self.started_at: datetime = parse_rfc3339_timestamp(timestamp=prediction['started_at'])
        self._locks_at: Optional[str] = prediction.get('locks_at')
        self._locked_at: Optional[str] = prediction.get('locked_at')
        self._ended_at: Optional[str] = prediction.get('ended_at')
        self._status: Literal['active', 'completed', 'archived', 'resolved'] = prediction.get('status')

    def __repr__(self) -> str:
        return f'<Prediction id={self.id} title={self.title}>'

    @property
    def outcomes(self) -> List[Outcome]:
        """
        Get the list of outcomes for the prediction.

        :return: The list of prediction outcomes.
        """
        return [Outcome(outcome=o) for o in self._outcomes]

    @property
    def is_ended(self) -> bool:
        """
        Check if the prediction has ended.

        :return: True if the prediction has ended, False otherwise.
        """
        return self._ended_at is not None

    @property
    def status(self) -> Literal['active', 'completed', 'archived', 'resolved']:
        """
        Get the status of the prediction.

        :return: The status of the prediction.
        """
        if self._ended_at:
            return self._status
        return 'active'

    @property
    def locks_at(self) -> datetime:
        """
        Get the locks timestamp of the prediction.

        :return: The locks timestamp of the prediction.
        """
        if self._locked_at is not None:
            return parse_rfc3339_timestamp(timestamp=self._locked_at)
        return parse_rfc3339_timestamp(timestamp=self._locks_at)

    @property
    def ended_at(self) -> Optional[datetime]:
        """
        Get the end time of Prediction.

        :return: The end time as a datetime object.
        """
        if self._ended_at:
            return parse_rfc3339_timestamp(timestamp=self._ended_at)
        return None
