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

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .types import prediction as PredictionTypes
    from typing import Optional, List, Union
    from datetime import datetime

__all__ = ('Prediction', 'Outcome', 'Predictor')


class Predictor(BaseUser):
    """
    Represents a predictor who participates in predictions.

    Attributes
    ----------
    points_won: int
        The channel points won by the predictor.
    points_used: int
        The channel points used by the predictor.

    Methods
    -------
    __str__() -> str
        Returns the name of the Predictor.
    __bool__() -> bool
        Returns True if the predictor has won any channel points.
    """
    __slots__ = ('points_won', 'points_used')

    if TYPE_CHECKING:
        points_won: int
        points_used: int

    def __init__(self, data: PredictionTypes.Predictor) -> None:
        super().__init__(data=data, prefix='user_')
        self._form_data(data=data)

    def __repr__(self) -> str:
        return f'<Predictor name={self.name} points_won={self.points_won} points_used={self.points_used}>'

    def __str__(self) -> str:
        return self.name

    def __bool__(self) -> bool:
        return self.points_won > 0

    def _form_data(self, data: PredictionTypes.Predictor) -> None:
        super()._update_data(data)
        # `points_won` could be null if user didn't win.
        self.points_won: int = data['channel_points_won'] or 0
        self.points_used: int = data['channel_points_used']


class Outcome:
    """
    Represents an outcome of a prediction.

    Attributes
    ----------
    id: str
        The unique ID of the outcome.
    color: str
        The color associated with the outcome.
    title: str
        The title of the outcome.
    total_users: int
        The total number of users who predicted this outcome.
    points_spent: int
        The total channel points spent on this outcome.
    top_predictors: List[Predictor]
        The top predictors who predicted this outcome.

    Methods
    -------
    __str__() -> str
        Returns the title of the Outcome.
    __eq__(other: object) -> bool
        Checks if two Outcome instances are equal based on their IDs.
    __ne__(other: object) -> bool
        Checks if two Outcome instances are not equal.
    """
    __slots__ = ('id', 'color', 'title', 'total_users', 'points_spent', 'top_predictors')

    if TYPE_CHECKING:
        id: str
        color: str
        title: str
        total_users: int
        points_spent: int
        top_predictors: List[Predictor]

    def __init__(self, data: PredictionTypes.Outcome) -> None:
        self._form_data(data=data)

    def __repr__(self) -> str:
        return f'<Outcome id={self.id} total_users={self.total_users} points_spent={self.points_spent}>'

    def __str__(self) -> str:
        return self.title

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Outcome):
            return self.id == other.id
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def _form_data(self, data: PredictionTypes.Outcome) -> None:
        self.id = data['id']
        self.color = data['color']
        self.title = data['title']
        self.total_users = data.get('users', 0)
        self.points_spent = data.get('channel_points', 0)
        self.top_predictors = []
        if data.get('top_predictors'):
            self.top_predictors = [Predictor(data=predictor) for predictor in data['top_predictors']]


class Prediction:
    """
    Represents a prediction on a Twitch channel.

    Attributes
    ----------
    id: str
        The unique ID of the prediction.
    title: str
        The title of the prediction.
    status: str
        The status of the prediction (e.g., "ACTIVE", "LOCKED").
    ended_at: Optional[datetime]
        The date and time when the prediction ended (if ended).
    is_ended: bool
        Indicates if the prediction has ended.
    outcomes: List[Outcome]
        The possible outcomes of the prediction.
    is_active: bool
        Indicates if the prediction is currently active.
    is_locked: bool
        Indicates if the prediction is locked.
    locked_at: Optional[datetime]
        The date and time when the prediction was locked (if locked).
    created_at: datetime
        The date and time when the prediction was created.
    winning_outcome: Optional[Outcome]
        The winning outcome of the prediction (if ended).
    prediction_window: Optional[int]
        The duration of the prediction window in seconds (if available).

    Methods
    -------
    __str__() -> str
        Returns the title of the Prediction.
    __bool__() -> bool
        Returns True if the prediction is currently active.
    __eq__(other: object) -> bool
        Checks if two Prediction instances are equal based on their IDs.
    __ne__(other: object) -> bool
        Checks if two Prediction instances are not equal.
    """
    __slots__ = ('id', 'title', 'status', 'ended_at', 'is_ended', 'outcomes', 'is_active',
                 'is_locked', 'locked_at', 'created_at', 'winning_outcome', 'prediction_window')

    if TYPE_CHECKING:
        id: str
        title: str
        status: str
        ended_at: Optional[datetime]
        is_ended: bool
        outcomes: List[Outcome]
        is_active: bool
        is_locked: bool
        locked_at: Optional[datetime]
        created_at: datetime
        winning_outcome: Optional[Outcome]
        prediction_window: Optional[int]

    def __init__(self, data: Union[PredictionTypes.Prediction,
                                   Union[PredictionTypes.PredictionBeginProgressEvent,
                                         PredictionTypes.PredictionLockEvent,
                                         PredictionTypes.PredictionEndEvent]]) -> None:
        self._form_data(data=data)

    def __repr__(self) -> str:
        return f'<Prediction id={self.id} status={self.status} created_at={self.created_at}>'

    def __str__(self) -> str:
        return self.title

    def __bool__(self) -> bool:
        return self.is_active

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Prediction):
            return self.id == other.id
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def _form_data(self, data: Union[PredictionTypes.Prediction,
                                     Union[PredictionTypes.PredictionBeginProgressEvent,
                                           PredictionTypes.PredictionLockEvent,
                                           PredictionTypes.PredictionEndEvent]]) -> None:
        self.id = data['id']
        self.title = data['title']
        self.outcomes = [Outcome(data=outcome) for outcome in data['outcomes']]
        # Missing on all event's payload.
        self.prediction_window = data.get('prediction_window')
        # `created_at` is missing in the event payload.
        _created_at: str = data.get('created_at') or data.get('started_at')
        self.created_at = convert_rfc3339(_created_at)
        # Prediction Lock.
        self.locked_at = convert_rfc3339(data.get('locked_at'))
        self.is_locked = self.locked_at is not None
        # Prediction End.
        self.ended_at = convert_rfc3339(data.get('ended_at'))
        self.is_ended = self.ended_at is not None
        # `status` is missing on ``Begin`` & ``Progress`` ``Lock`` Event.
        _status: Optional[str] = data.get('status')
        if _status:
            self.status = _status
        else:
            if self.is_locked:
                self.status = 'LOCKED'
            else:
                self.status = 'ACTIVE'
        self.is_active = self.status == 'ACTIVE'
        _winning_outcome_id: Optional[str] = data.get('winning_outcome_id')
        self.winning_outcome = None
        if _winning_outcome_id:
            self.winning_outcome = next(
                (outcome for outcome in self.outcomes if outcome.id == _winning_outcome_id), None)

    def to_json(self) -> PredictionTypes.PredictionToJson:
        # This is useful when you want to recreate the same prediction.
        # If prediction_window is Missing will be set to 900 seconds by default.
        return ({
            'title': self.title,
            'outcomes': [{'title': outcome.title} for outcome in self.outcomes],
            'prediction_window': self.prediction_window if self.prediction_window else 900
        })
