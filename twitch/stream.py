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

# Core
from .utils import parse_rfc3339_timestamp
from .user import User

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .types.eventsub import stream as sm
    from typing import Optional, Union
    from datetime import datetime


class Shoutout:
    """
    Represents a stream shoutout.
    """
    __slots__ = ('__shoutout', 'viewer_count', 'started_at', '_cooldown_ends_at', '_target_cooldown_ends_at')

    def __init__(self, shoutout: Union[sm.ShoutoutCreate, sm.ShoutoutReceived]) -> None:

        self.__shoutout = shoutout
        self.viewer_count: int = shoutout['viewer_count']
        self.started_at: datetime = parse_rfc3339_timestamp(timestamp=shoutout['started_at'])
        self._cooldown_ends_at: Optional[str] = shoutout.get('cooldown_ends_at')
        self._target_cooldown_ends_at: Optional[str] = shoutout.get('target_cooldown_ends_at')

    def __repr__(self) -> str:
        return f'<Shoutout sender={self.sender.__repr__()} Receiver={self.receiver.__repr__()}>'

    @property
    def sender(self) -> User:
        if self._cooldown_ends_at:
            return User(user=self.__shoutout, prefix='broadcaster_user')
        else:
            return User(user=self.__shoutout, prefix='from_broadcaster_user')

    @property
    def receiver(self):
        if self._cooldown_ends_at is None:
            return User(user=self.__shoutout, prefix='broadcaster_user')
        else:
            return User(user=self.__shoutout, prefix='to_broadcaster_user')

    @property
    def cooldown_ends_at(self) -> Optional[datetime]:
        if self._cooldown_ends_at:
            return parse_rfc3339_timestamp(timestamp=self._cooldown_ends_at)
        return None

    @property
    def target_cooldown_ends_at(self) -> Optional[datetime]:
        if self._target_cooldown_ends_at:
            return parse_rfc3339_timestamp(timestamp=self._target_cooldown_ends_at)
        return None


class Online:
    """
    Represents an online stream.
    """
    __slots__ = ('user', 'id', 'type', 'started_at')

    def __init__(self, stream: sm.Online):
        self.user: User = User(user=stream, prefix='broadcaster_user')
        self.id: str = stream['id']
        self.type: str = stream['type']
        self.started_at: datetime = parse_rfc3339_timestamp(timestamp=stream['started_at'])

    def __repr__(self) -> str:
        return f'<Online user={self.user} id={self.id} type={self.type} started_at={self.started_at}>'


class Offline:
    """
    Represents an offline stream.
    """
    __slots__ = 'user'

    def __init__(self, stream: sm.Offline):
        self.user: User = User(user=stream, prefix='broadcaster_user')

    def __repr__(self) -> str:
        return f'<Offline user={self.user}>'
