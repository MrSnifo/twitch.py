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
from typing import TypedDict, Literal


class Goal(TypedDict):
    type: Literal['follow', 'subscription', 'subscription_count', 'new_subscription',
                  'new_subscription_count']
    current_amount: int


class _GoalBase(SpecificBroadcaster, Goal):
    id: str
    description: str
    started_at: str


class Begin(_GoalBase):
    """
    Type: Goal Begin
    Name: `channel.goal.begin`
    Version: 1
    """
    pass


class Progress(_GoalBase):
    """
    Type: Goal Progress
    Name: `channel.goal.progress`
    Version: 1
    """
    pass


class End(_GoalBase):
    """
    Type: Goal End
    Name: `channel.goal.end`
    Version: 1
    """
    is_achieved: bool
    ended_at: str
