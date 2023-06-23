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

# Core
from ..user import (SpecificBroadcaster, SpecificModerator,
                    ToSpecificBroadcaster, FromSpecificBroadcaster)
from typing import Literal


class BaseShoutout(SpecificBroadcaster):
    viewer_count: int
    started_at: str


class ShoutoutCreate(BaseShoutout, SpecificModerator, ToSpecificBroadcaster):
    """
    Type: Shoutout Create
    Name: `channel.shoutout.create`
    Version: 1
    """
    cooldown_ends_at: str
    target_cooldown_ends_at: str


class ShoutoutReceived(BaseShoutout, FromSpecificBroadcaster):
    """
    Type: Shoutout Received
    Name: `channel.shoutout.receive`
    Version: 1
    """
    pass


class Online(SpecificBroadcaster):
    """
    Type: Stream Online
    Name: `stream.online`
    Version: 1
    """
    id: str
    type: Literal['live', 'playlist', 'watch_party', 'premiere', 'rerun']
    started_at: str


class Offline(SpecificBroadcaster):
    """
    Type: Stream Offline
    Name: `stream.offline`
    Version: 1
    """
    pass
