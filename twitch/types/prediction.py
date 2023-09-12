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

from typing import TypedDict, Optional, Literal, List
from .user import SpecificUser, SpecificBroadcaster


# --------------------------------------
#            + Predication +
# --------------------------------------
class Predictor(SpecificUser):
    channel_points_won: Optional[int]
    channel_points_used: int


class Outcome(TypedDict, total=False):
    id: str
    color: str
    title: str
    users: int  # May sometimes be unavailable.
    channel_points: int  # May sometimes be unavailable.
    top_predictors: List[Predictor]  # May sometimes be unavailable.


class BasePrediction(TypedDict):
    id: str
    title: str
    outcomes: List[Outcome]


class Prediction(BasePrediction):
    status: Literal['ACTIVE', 'CANCELED', 'LOCKED', 'RESOLVED']
    ended_at: Optional[str]
    locked_at: Optional[str]
    created_at: str
    prediction_window: int
    winning_outcome_id: Optional[str]


PredictionOutcomesTitle = TypedDict('PredictionOutcomesTitle', {'title': str})


class PredictionToJson(TypedDict):
    title: str
    outcomes: List[PredictionOutcomesTitle]
    prediction_window: int


# -------------+ EventSub +-------------
class PredictionBeginProgressEvent(SpecificBroadcaster, BasePrediction):
    locks_at: str
    started_at: str


class PredictionLockEvent(SpecificBroadcaster, BasePrediction):
    locked_at: str
    started_at: str


class PredictionEndEvent(SpecificBroadcaster, BasePrediction):
    status: Literal['resolved', 'canceled']
    ended_at: str
    started_at: str
    winning_outcome_id: str
