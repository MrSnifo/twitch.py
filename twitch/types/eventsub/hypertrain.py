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

from ..user import SpecificBroadcaster, SpecificUser
from typing import Literal, List


class Contributor(SpecificUser):
    type: Literal['bits', 'subscription', 'other']
    total: int


class BaseHypeTrain(SpecificBroadcaster):
    id: str
    total: int
    level: int
    top_contributions: List[Contributor]
    started_at: str


class Begin(BaseHypeTrain):
    """
    Type: Hype Train Begin
    Name: `channel.hype_train.begin`
    Version: 1
    """
    progress: int
    goal: int
    last_contribution: List[Contributor]
    expires_at: str


class Progress(Begin):
    """
    Type: Hype Train Progress
    Name: `channel.hype_train.progress`
    Version: 1
    """
    pass


class End(BaseHypeTrain):
    """
    Type: Hype Train End
    Name: `channel.hype_train.end`
    Version: 1
    """
    ended_at: str
    cooldown_ends_at: str
