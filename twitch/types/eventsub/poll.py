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
from typing import TypedDict, List, Literal


class Voting(TypedDict):
    is_enabled: bool
    amount_per_vote: int


class Choice(TypedDict):
    id: str
    title: str


class ChoicesCount(Choice):
    bits_votes: int
    channel_points_votes: int
    votes: int


class _BasePoll(SpecificBroadcaster):
    id: str
    title: str
    bits_voting: Voting
    channel_points_voting: Voting
    started_at: str


class Begin(_BasePoll):
    """
    Type: Channel Poll Begin
    Name: `channel.poll.begin`
    Version: 1
    """
    choices: List[Choice]
    ends_at: str


class Progress(_BasePoll):
    """
    Type: Channel Poll Progress
    Name: `channel.poll.progress`
    Version: 1
    """
    choices: List[ChoicesCount]
    ends_at: str


class End(_BasePoll):
    """
    Type: Channel Poll End
    Name: `channel.poll.end`
    Version: 1
    """
    choices: List[ChoicesCount]
    status: Literal['completed', 'archived', 'terminated']
    ended_at: str
