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

from ..user import SpecificBroadcaster, SpecificModerator, SpecificUser
from typing import Optional


class Ban(SpecificBroadcaster, SpecificModerator, SpecificUser):
    """
    Type: Channel Ban
    Name: `channel.ban`
    Version: 1
    """
    reason: str
    banned_at: str
    ends_at: Optional[str]
    is_permanent: bool


class UnBan(SpecificBroadcaster, SpecificModerator, SpecificUser):
    """
    Type: Channel Unban
    Name: `channel.unban`
    Version: 1
    """
    pass


class Add(SpecificBroadcaster, SpecificUser):
    """
    Type: Channel Moderator Add
    Name: `channel.moderator.add`
    Version: 1
    """
    pass


class Remove(SpecificBroadcaster, SpecificUser):
    """
    Type: Channel Moderator Remove
    Name: `channel.moderator.remove`
    Version: 1
    """
    pass


class ShieldModeBegin(SpecificBroadcaster, SpecificModerator):
    """
    Type: Shield Mode Begin
    Name: `channel.shield_mode.begin`
    Version: 1
    """
    started_at: str


class ShieldModeEnd(SpecificBroadcaster, SpecificModerator):
    """
    Type: Shield Mode End
    Name: `channel.shield_mode.end`
    Version: 1
    """
    ended_at: str
