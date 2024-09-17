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

from typing import TYPE_CHECKING, TypedDict
from .users import SpecificUser

if TYPE_CHECKING:
    from typing import List, Optional, Literal, NotRequired, Dict


class EmoteImages(TypedDict):
    """
    Represents the URLs for different sizes of emote images.

    Attributes
    ----------
    url_1x: str
        The URL for the emote image at 1x resolution.
    url_2x: str
        The URL for the emote image at 2x resolution.
    url_4x: str
        The URL for the emote image at 4x resolution.
    """
    url_1x: str
    url_2x: str
    url_4x: str


class Emote(TypedDict):
    """
    Represents an emote.

    Attributes
    ----------
    id: str
        The unique identifier for the emote.
    name: str
        The name of the emote.
    images: EmoteImages
        The URLs for different sizes of the emote images.
    template_url: str
        The URL template for the emote images.
    emote_type: str
        The type of the emote.
    emote_set_id: str
        The set ID to which the emote belongs.
    owner_id: str
        The ID of the emotes owner.
    format: Literal['animated', 'static']
        The format of the emote (animated or static).
    scale: Literal['1.0', '2.0', '3.0']
        The scale of the emote.
    theme_mode: Literal['dark', 'light']
        The theme mode for which the emote is designed (dark or light).
    """
    id: str
    name: str
    images: EmoteImages
    template_url: str
    emote_type: str
    emote_set_id: str
    owner_id: str
    format: Literal['animated', 'static']
    scale: Literal['1.0', '2.0', '3.0']
    theme_mode: Literal['dark', 'light']


class BadgeVersion(TypedDict):
    """
    Represents a specific version of a badge.

    Attributes
    ----------
    id: str
        The unique identifier for the badge version.
    image_url_1x: str
        The URL of the badge image at 1x resolution.
    image_url_2x: str
        The URL of the badge image at 2x resolution.
    image_url_4x: str
        The URL of the badge image at 4x resolution.
    title: str
        The title of the badge version.
    description: str
        A brief description of the badge version.
    click_action: Optional[str]
        The action that occurs when the badge is clicked.
    click_url: Optional[str]
        The URL to which the user is directed when the badge is clicked.
    """
    id: str
    image_url_1x: str
    image_url_2x: str
    image_url_4x: str
    title: str
    description: str
    click_action: Optional[str]
    click_url: Optional[str]


class Badge(TypedDict):
    """
    Represents a badge with multiple versions.

    Attributes
    ----------
    set_id: str
        The unique identifier for the badge set.
    versions: List[BadgeVersion]
        A list of the badge's versions.
    """
    set_id: str
    versions: List[BadgeVersion]


class Settings(TypedDict, total=False):
    """
    Represents various chat settings.

    Attributes
    ----------
    broadcaster_id: str
        The unique identifier for the broadcaster.
    emote_mode: bool
        Whether the emote-only mode is enabled.
    follower_mode: bool
        Whether the follower-only mode is enabled.
    follower_mode_duration: Optional[int]
        The duration in minutes for which a user must follow to chat.
    moderator_id: str
        The unique identifier for the moderator.
    non_moderator_chat_delay: NotRequired[bool]
        Whether there is a chat delay for non-moderators.
    non_moderator_chat_delay_duration: NotRequired[int]
        The duration of the chat delay for non-moderators.
    slow_mode: bool
        Whether the slow mode is enabled.
    slow_mode_wait_time: Optional[bool]
        The wait time in seconds for the slow mode.
    subscriber_mode: bool
        Whether the subscriber-only mode is enabled.
    unique_chat_mode: bool
        Whether the unique chat mode is enabled (prevents repeated messages).
    """
    broadcaster_id: str
    emote_mode: bool
    follower_mode: bool
    follower_mode_duration: Optional[int]
    moderator_id: str
    non_moderator_chat_delay: NotRequired[bool]
    non_moderator_chat_delay_duration: NotRequired[int]
    slow_mode: bool
    slow_mode_wait_time: Optional[bool]
    subscriber_mode: bool
    unique_chat_mode: bool


class MessageDropReason(TypedDict):
    """
    Represents the reason for a message drop.

    Attributes
    ----------
    code: str
        The error code associated with the message drop.
    message: str
        A description of the reason for the message drop.
    """
    code: str
    message: str


class SendMessageStatus(TypedDict, total=False):
    """
    Represents the status of a user sent message.

    Attributes
    ----------
    message_id: str
        The unique identifier for the message.
    is_sent: bool
        Whether the message was successfully sent.
    drop_reason: NotRequired[MessageDropReason]
        The reason for a message drop, if applicable.
    """
    message_id: str
    is_sent: bool
    drop_reason: NotRequired[MessageDropReason]


UserChatColors = Literal['blue', 'blue_violet', 'cadet_blue', 'chocolate', 'coral', 'dodger_blue', 'firebrick',
                         'golden_rod', 'green', 'hot_pink', 'orange_red', 'red', 'sea_green', 'spring_green',
                         'yellow_green']


class UserChatColor(SpecificUser):
    """
    Represents a user's chat color.

    Attributes
    ----------
    color: str
        The hexadecimal color code chosen by the user for their chat messages.
    """
    color: str


class SharedChatSession(TypedDict):
    """
    A TypedDict representing a shared chat session.

    Attributes
    ----------
    session_id: str
        Unique identifier for the chat session.
    host_broadcaster_id: str
        Identifier for the host broadcaster.
    participants: List[Dict[Literal['broadcaster_id'], str]]
        List of participants with broadcaster IDs.
    created_at  str
        Timestamp of when the session was created.
    updated_at: str
        Timestamp of the last update to the session.
    """
    session_id: str
    host_broadcaster_id: str
    participants: List[Dict[Literal['broadcaster_id'], str]]
    created_at: str
    updated_at: str
