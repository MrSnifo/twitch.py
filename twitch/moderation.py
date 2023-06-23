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

from .utils import parse_rfc3339_timestamp
from .user import User

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .types.eventsub import moderation as md
    from typing import Optional, Union
    from datetime import datetime


class Ban:
    """
    Represents a channel ban.

    :param ban: The ban data.
    """

    def __init__(self, ban: md.Ban) -> None:
        self.user: User = User(user=ban)
        self.moderator: User = User(user=ban, prefix='moderator_user')
        self.reason: str = ban['reason']
        self.banned_at: datetime = parse_rfc3339_timestamp(timestamp=ban['banned_at'])
        self._ends_at: Optional[str] = ban['ends_at']
        self.is_permanent: bool = ban['is_permanent']

    @property
    def ends_at(self) -> Optional[datetime]:
        """
        Get the end time of the ban.

        :return: The end time as a datetime object.
        """
        if self._ends_at:
            return parse_rfc3339_timestamp(timestamp=self._ends_at)
        return None

    def __repr__(self) -> str:
        return f'<Ban user={self.user.__repr__()} moderator={self.moderator.__repr__()}>'


class UnBan:
    """
    Represents a channel unban.

    :param unban: The unban data.
    """

    def __init__(self, unban: md.UnBan) -> None:
        self.user: User = User(user=unban)
        self.moderator: User = User(user=unban, prefix='moderator_user')

    def __repr__(self) -> str:
        return f'<UnBan user={self.user.__repr__()} moderator={self.moderator.__repr__()}>'


class ShieldMode:
    """
    Represents a channel Shield Mode.

    :param mode: The Shield Mode data.
    """

    def __init__(self, mode: Union[md.ShieldModeBegin, md.ShieldModeEnd]) -> None:
        self.moderator: User = User(user=mode, prefix='moderator_user')
        self._started_at: Optional[str] = mode.get('started_at')
        self._ended_at: Optional[str] = mode.get('ended_at')

    def __repr__(self) -> str:
        return f'<ShieldMode moderator={self.moderator} _started_at={self._started_at}' \
               f' _ended_at={self._ended_at}>'

    @property
    def is_enabled(self) -> bool:
        """
        Check if Shield Mode is enabled.

        :return: True if Shield Mode is enabled, False otherwise.
        """
        return self._started_at is not None

    @property
    def started_at(self) -> Optional[datetime]:
        """
        Get the start time of Shield Mode.

        :return: The start time as a datetime object.
        """
        if self._started_at:
            return parse_rfc3339_timestamp(timestamp=self._started_at)
        return None

    @property
    def ended_at(self) -> Optional[datetime]:
        """
        Get the end time of Shield Mode.

        :return: The end time as a datetime object.
        """
        if self._ended_at:
            return parse_rfc3339_timestamp(timestamp=self._ended_at)
        return None
