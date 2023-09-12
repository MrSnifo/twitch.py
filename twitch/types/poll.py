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
from .user import Broadcaster, SpecificBroadcaster

# ---------------------------------------
#                + Poll +
# ---------------------------------------
PollStatus = Literal['ACTIVE', 'COMPLETED', 'TERMINATED', 'ARCHIVED', 'MODERATED', 'INVALID']


class PollChoice(TypedDict, total=False):
    id: str
    title: str
    votes: int  # May sometimes be unavailable.
    bits_votes: int  # May sometimes be unavailable.
    channel_points_votes: int  # May sometimes be unavailable.


class BasePoll(TypedDict):
    id: str
    title: str
    choices: List[PollChoice]
    started_at: str


class Poll(Broadcaster, BasePoll):
    status: PollStatus
    duration: int
    ended_at: Optional[str]
    bits_per_vote: int
    bits_voting_enabled: bool
    channel_points_per_vote: int
    channel_points_voting_enabled: bool


PollTitleChoice = TypedDict('PollTitleChoice', {'title': str})


class PollToJson(TypedDict):
    title: str
    choices: List[PollTitleChoice]
    duration: int
    points_voting_enabled: bool
    points_per_vote: int


# -------------+ EventSub +-------------
AmountPerVote = TypedDict('AmountPerVote', {'is_enabled': bool, 'amount_per_vote': int})


class PollBeginAndProgressEvent(SpecificBroadcaster, BasePoll):
    ends_at: str
    bits_voting: AmountPerVote
    channel_points_voting: AmountPerVote


class PollEndEvent(SpecificBroadcaster, BasePoll):
    status: Literal['completed', 'archived', 'terminated']
    ended_at: str
    bits_voting: AmountPerVote
    channel_points_voting: AmountPerVote
