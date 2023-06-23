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

from ..user import SpecificBroadcaster
from typing import TypedDict, Optional, Literal, List


class BaseOutcome(TypedDict):
    id: str
    title: str
    color: str


class Predictor(TypedDict):
    user_id: str
    user_login: str
    user_name: str
    channel_points_won: Optional[int]
    channel_points_used: int


class Outcome(BaseOutcome, total=False):
    users: int  # Not present sometimes.
    channel_points: int
    top_predictors: Predictor


class _BasePrediction(SpecificBroadcaster):
    id: str
    title: str
    started_at: str


class Begin(_BasePrediction):
    """
    Type: Channel Prediction Begin
    Name: `channel.prediction.begin`
    Version: 1
    """
    outcomes: List[BaseOutcome]
    locks_at: str


class Progress(_BasePrediction):
    """
    Type: Channel Prediction Progress
    Name: `channel.prediction.progress`
    Version: 1
    """
    outcomes: List[Outcome]
    locks_at: str


class Lock(_BasePrediction):
    """
    Type: Channel Prediction Lock
    Name: `channel.prediction.lock`
    Version: 1
    """
    outcomes: List[Outcome]
    locked_at: str


class End(_BasePrediction):
    """
    Type: Channel Prediction End
    Name: `channel.prediction.end`
    Version: 1
    """
    outcomes: List[Outcome]
    status: Literal['resolved', 'canceled']
    ended_at: str
