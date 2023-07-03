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
    from .types.eventsub import guest as gt
    from typing import Optional, Union
    from datetime import datetime

__all__ = ('GuestStar', 'GuestStarUpdate', 'GuestStarSlotUpdate', 'GuestStarSettingsUpdate')


class GuestStar:
    """
    Represents GuestStar.

    :param session: The GuestStar session data.
    """
    __slots__ = ('id', 'started_at', '_ended_at')

    def __init__(self, session: Union[gt.Begin, gt.End]) -> None:
        self.id: str = session['session_id']
        self.started_at: datetime = parse_rfc3339_timestamp(timestamp=session['started_at'])
        self._ended_at: Optional[str] = session.get('ended_at')

    def __repr__(self):
        return f'<GuestStar id={self.id} started_at={self.started_at}>'

    @property
    def is_ended(self) -> bool:
        """
        Checks if the GuestStar session has ended.

        :return: True if the GuestStar session has ended, False otherwise.
        """
        return self._ended_at is not None

    @property
    def ended_at(self) -> Optional[datetime]:
        """
        Get the end time of GuestStar session.

        :return: The end time as a datetime object.
        """
        if self.is_ended:
            return parse_rfc3339_timestamp(timestamp=self._ended_at)
        return None


class GuestStarUpdate:
    """
    Represents when GuestStar session has been updated.

    :param session: The GuestStar session data.
    """
    __slots__ = ('id', 'moderator', 'guest', 'slot_id', 'state')

    def __init__(self, session: gt.Update) -> None:
        self.id: str = session['session_id']
        self.moderator: Optional[User] = User(
            user=session,
            prefix='moderator_user') if session['moderator_user_id'] is not None else None
        self.guest: User = User(user=session, prefix='guest_user')
        self.slot_id: Optional[str] = session['slot_id']  # None if the guest is in the INVITED state.
        self.state: str = session['state']

    def __repr__(self) -> str:
        return f'<GuestStarUpdate id={self.id} guest={self.guest.__repr__()} state={self.state}>'

    @property
    def is_moderator(self) -> bool:
        """
        Checks if a moderator has updated the GuestStar session.

        :return: True if the moderator has updated the session, False otherwise.
        """
        return self.moderator is not None


class Host:
    """
    Represents GuestStar Host.

    :param host: The GuestStar host.
    """
    __slots__ = ('is_video_enabled', 'is_audio_enabled', 'volume')

    def __init__(self, host: gt.SlotUpdate) -> None:
        self.is_video_enabled: bool = host['host_video_enabled']
        self.is_audio_enabled: bool = host['host_audio_enabled']
        self.volume: int = host['host_volume']

    def __repr__(self) -> str:
        return f'<Host is_video_enabled={self.is_video_enabled} is_audio_enabled={self.is_audio_enabled}>'


class GuestStarSlotUpdate:
    """
    Represents when GuestStar slot has been updated.

    :param slot: The GuestStar slot data.
    """
    __slots__ = ('id', 'moderator', 'guest', 'slot_id', 'host')

    def __init__(self, slot: gt.SlotUpdate) -> None:
        self.id: str = slot['session_id']
        self.moderator: User = User(user=slot, prefix='moderator_user')
        self.guest: Optional[User] = User(
            user=slot,
            prefix='guest_user') if slot['guest_user_id'] is not None else None
        self.slot_id: str = slot['slot_id']  # None if the guest is in the INVITED state.
        self.host: Host = Host(host=slot)

    @property
    def is_moderator(self) -> bool:
        """
        Checks if a moderator has updated the GuestStar session.

        :return: True if the moderator has updated the session, False otherwise.
        """
        return self.moderator is not None


class GuestStarSettingsUpdate:
    """
    Represents when GuestStar settings has been updated.

    :param settings: The GuestStar settings data.
    """
    __slots__ = ('is_moderator_send_live_enabled', 'is_browser_source_audio_enabled', 'slot_count',
                 'group_layout')

    def __init__(self, settings: gt.SettingsUpdate) -> None:
        self.is_moderator_send_live_enabled: bool = settings['is_moderator_send_live_enabled']
        self.is_browser_source_audio_enabled: bool = settings['is_browser_source_audio_enabled']
        self.slot_count: int = settings['slot_count']
        self.group_layout: str = settings['group_layout']
