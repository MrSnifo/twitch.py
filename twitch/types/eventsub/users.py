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

if TYPE_CHECKING:
    from typing import NotRequired, Optional, List


class Broadcaster(TypedDict):
    """
    Represents a broadcaster with basic information.

    Attributes
    ----------
    broadcaster_id: str
        The ID of the broadcaster.
    broadcaster_name: str
        The display name of the broadcaster.
    broadcaster_login: str
        The login name of the broadcaster.
    """
    broadcaster_id: str
    broadcaster_name: str
    broadcaster_login: str


class SpecificBroadcaster(TypedDict):
    """
    Represents a specific broadcaster with user details.

    Attributes
    ----------
    broadcaster_user_id: str
        The user ID of the broadcaster.
    broadcaster_user_name: str
        The user name of the broadcaster.
    broadcaster_user_login: str
        The login name of the broadcaster.
    """
    broadcaster_user_id: str
    broadcaster_user_name: str
    broadcaster_user_login: str


class Moderator(TypedDict):
    """
    Represents a moderator with basic information.

    Attributes
    ----------
    moderator_id: str
        The ID of the moderator.
    moderator_name: str
        The display name of the moderator.
    moderator_login: str
        The login name of the moderator.
    """
    moderator_id: str
    moderator_name: str
    moderator_login: str


class SpecificModerator(TypedDict):
    """
    Represents a specific moderator with user details.

    Attributes
    ----------
    moderator_user_id: str
        The user ID of the moderator.
    moderator_user_name: str
        The user name of the moderator.
    moderator_user_login: str
        The login name of the moderator.
    """
    moderator_user_id: str
    moderator_user_name: str
    moderator_user_login: str


class SpecificUser(TypedDict):
    """
    Represents a specific user with details.

    Attributes
    ----------
    user_id: str
        The ID of the user.
    user_name: str
        The name of the user.
    user_login: str
        The login name of the user.
    """
    user_id: str
    user_name: str
    user_login: str


# User
class UserUpdateEvent(TypedDict, total=False):
    """
    Represents an update event for a user.

    Attributes
    ----------
    user_id: str
        The ID of the user.
    user_login: str
        The login name of the user.
    user_name: str
        The name of the user.
    email: str, optional
        The email of the user, if provided.
    email_verified: bool, optional
        Whether the email has been verified.
    description: str
        The description or bio of the user.
    """
    user_id: str
    user_login: str
    user_name: str
    email: NotRequired[str]
    email_verified: NotRequired[bool]
    description: str


# Whisper
class WhisperDetails(TypedDict):
    """
    Represents the details of a whisper message.

    Attributes
    ----------
    text: str
        The content of the whisper message.
    """
    text: str


class WhisperReceivedEvent(TypedDict):
    """
    Represents an event where a whisper message is received.

    Attributes
    ----------
    from_user_id: str
        The ID of the user who sent the whisper.
    from_user_name: str
        The name of the user who sent the whisper.
    from_user_login: str
        The login name of the user who sent the whisper.
    to_user_id: str
        The ID of the user who received the whisper.
    to_user_name: str
        The name of the user who received the whisper.
    to_user_login: str
        The login name of the user who received the whisper.
    whisper_id: str
        The ID of the whisper message.
    whisper: WhisperDetails
        The details of the whisper message.
    """
    from_user_id: str
    from_user_name: str
    from_user_login: str
    to_user_id: str
    to_user_name: str
    to_user_login: str
    whisper_id: str
    whisper: WhisperDetails


# Automod
class Cheermote(TypedDict):
    """
    Represents a cheermote with its properties.

    Attributes
    ----------
    prefix: str
        The prefix of the cheermote.
    bits: int
        The number of bits required to use the cheermote.
    tier: int
        The tier level of the cheermote.
    """
    prefix: str
    bits: int
    tier: int


class Emote(TypedDict):
    """
    Represents an emote with its properties.

    Attributes
    ----------
    id: str
        The ID of the emote.
    emote_set_id: str
        The ID of the emote set to which the emote belongs.
    """
    id: str
    emote_set_id: str


class Fragment(TypedDict):
    """
    Represents a fragment of a message that can be a cheermote or emote.

    Attributes
    ----------
    cheermote: Cheermote, optional
        The cheermote fragment, if any.
    emote: Emote, optional
        The emote fragment, if any.
    """
    cheermote: Optional[Cheermote]
    emote: Optional[Emote]


class Message(TypedDict):
    """
    Represents a message with its content and fragments.

    Attributes
    ----------
    text: str
        The content of the message.
    fragments: List[Fragment]
        A list of fragments in the message.
    """
    text: str
    fragments: List[Fragment]


class MessageHoldEvent(SpecificBroadcaster, SpecificUser):
    """
    Represents an event where a message is held for moderation.

    Attributes
    ----------
    message_id: str
        The ID of the held message.
    message: Message
        The details of the held message.
    """
    message_id: str
    message: Message


class MessageUpdateEvent(SpecificBroadcaster, SpecificUser):
    """
    Represents an event where a message is updated.

    Attributes
    ----------
    status: str
        The new status of the message.
    message_id: str
        The ID of the updated message.
    message: Message
        The details of the updated message.
    """
    status: str
    message_id: str
    message: Message


# Auth
class AuthorizationGrantEvent(SpecificUser):
    """
    Represents an event where authorization is granted.

    Attributes
    ----------
    client_id: str
        The ID of the client that received authorization.
    """
    client_id: str


class AuthorizationRevokeEvent(TypedDict):
    """
    Represents an event where authorization is revoked.

    Attributes
    ----------
    client_id: str
        The ID of the client whose authorization was revoked.
    user_id: str
        The ID of the user whose authorization was revoked.
    user_login: str, optional
        The login name of the user, if available.
    user_name: str, optional
        The name of the user, if available.
    """
    client_id: str
    user_id: str
    user_login: Optional[str]
    user_name: Optional[str]
