"""
The MIT License (MIT)

Copyright (c) 2024-present Snifo

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT firstED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from __future__ import annotations

from .users import SpecificBroadcaster, SpecificModerator
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from typing import Literal


# Ad
class AdBreakBeginEvent(SpecificBroadcaster):
    """
    Represents an event where an ad break begins.

    Attributes
    ----------
    duration_seconds: int
        The duration of the ad break in seconds.
    started_at: str
        The timestamp when the ad break started, in ISO 8601 format.
    is_automatic: bool
        Whether the ad break was triggered automatically.
    requester_user_id: str
        The user ID of the requester who initiated the ad break.
    requester_user_login: str
        The login name of the requester.
    requester_user_name: str
        The display name of the requester.
    """
    duration_seconds: int
    started_at: str
    is_automatic: bool
    requester_user_id: str
    requester_user_login: str
    requester_user_name: str


# Raid
class RaidEvent(TypedDict):
    """
    Represents an event where a raid occurs.

    Attributes
    ----------
    from_broadcaster_user_id: str
        The user ID of the broadcaster initiating the raid.
    from_broadcaster_user_login: str
        The login name of the broadcaster initiating the raid.
    from_broadcaster_user_name: str
        The display name of the broadcaster initiating the raid.
    to_broadcaster_user_id: str
        The user ID of the broadcaster receiving the raid.
    to_broadcaster_user_login: str
        The login name of the broadcaster receiving the raid.
    to_broadcaster_user_name: str
        The display name of the broadcaster receiving the raid.
    viewers: int
        The number of viewers participating in the raid.
    """
    from_broadcaster_user_id: str
    from_broadcaster_user_login: str
    from_broadcaster_user_name: str
    to_broadcaster_user_id: str
    to_broadcaster_user_login: str
    to_broadcaster_user_name: str
    viewers: int


# Shoutout
class ShoutoutCreateEvent(SpecificBroadcaster, SpecificModerator):
    """
    Represents an event where a shoutout is created.

    Attributes
    ----------
    to_broadcaster_user_id: str
        The user ID of the broadcaster receiving the shoutout.
    to_broadcaster_user_login: str
        The login name of the broadcaster receiving the shoutout.
    to_broadcaster_user_name: str
        The display name of the broadcaster receiving the shoutout.
    viewer_count: int
        The number of viewers when the shoutout was created.
    started_at: str
        The timestamp when the shoutout started, in ISO 8601 format.
    cooldown_ends_at: str
        The timestamp when the cooldown period for the shoutout ends, in ISO 8601 format.
    target_cooldown_ends_at: str
        The timestamp when the target cooldown period ends, in ISO 8601 format.
    """
    to_broadcaster_user_id: str
    to_broadcaster_user_login: str
    to_broadcaster_user_name: str
    viewer_count: int
    started_at: str
    cooldown_ends_at: str
    target_cooldown_ends_at: str


class ShoutoutReceivedEvent(SpecificBroadcaster):
    """
    Represents an event where a shoutout is received.

    Attributes
    ----------
    from_broadcaster_user_id: str
        The user ID of the broadcaster who sent the shoutout.
    from_broadcaster_user_login: str
        The login name of the broadcaster who sent the shoutout.
    from_broadcaster_user_name: str
        The display name of the broadcaster who sent the shoutout.
    viewer_count: int
        The number of viewers when the shoutout was received.
    started_at: str
        The timestamp when the shoutout was received, in ISO 8601 format.
    """
    from_broadcaster_user_id: str
    from_broadcaster_user_login: str
    from_broadcaster_user_name: str
    viewer_count: int
    started_at: str


# Stream
class StreamOnlineEvent(SpecificBroadcaster):
    """
    Represents an event where a stream goes online.

    Attributes
    ----------
    id: str
        The ID of the stream.
    type: Literal['live', 'playlist', 'watch_party', 'premiere', 'rerun']
        The type of the stream.
    started_at: s²tr
        The timestamp when the stream started, in ISO 8601 format.
    """
    id: str
    type: Literal['live', 'playlist', 'watch_party', 'premiere', 'rerun']
    started_at: str


class StreamOfflineEvent(SpecificBroadcaster):
    """
    Represents an event where a stream goes offline.

    Attributes
    ----------
    (No additional attributes; inherits from SpecificBroadcaster)
    """
    pass
