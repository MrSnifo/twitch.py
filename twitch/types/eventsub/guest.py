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

from ..user import (SpecificBroadcaster, SpecificOpModerator, SpecificModerator,
                    SpecificGuest, SpecificOpGuest)
from typing import Literal, Optional


class _Session(SpecificBroadcaster):
    session_id: str


class Begin(_Session):
    """
    Type: Channel Guest Star Session Begin
    Name: `channel.guest_star_session.begin`
    Version: beta
    """
    started_at: str


class End(_Session):
    """
    Type: Channel Guest Star Session End
    Name: `channel.guest_star_session.end`
    Version: beta
    """
    started_at: str
    ended_at: str


class Update(_Session, SpecificOpModerator, SpecificGuest):
    """
    Type: Channel Guest Star Guest Update
    Name: `channel.guest_star_guest.update`
    Version: beta
    """
    slot_id: Optional[str]
    state: Literal['invited', 'ready', 'backstage', 'live', 'removed']


class SlotUpdate(_Session, SpecificModerator, SpecificOpGuest):
    """
    Type: Channel Guest Star Slot Update
    Name: `channel.guest_star_guest.update`
    Version: beta
    """
    slot_id: str
    host_video_enabled: bool
    host_audio_enabled: bool
    host_volume: int


class SettingsUpdate(SpecificBroadcaster):
    """
    Type: Channel Guest Star Settings Update
    Name: `channel.guest_star_settings.update`
    Version: beta
    """
    is_moderator_send_live_enabled: bool
    slot_count: int
    is_browser_source_audio_enabled: bool
    group_layout: Literal['tiled', 'screenshare']
