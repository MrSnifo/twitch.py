"""
The MIT License (MIT)

Copyright (c) 2025-present Snifo

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

from .users import SpecificBroadcaster, SpecificUser
from typing import TypedDict, List, Optional, Literal


class CheerEvent(SpecificBroadcaster):
    """
    Represents a channel cheer event on Twitch.

    Attributes
    ----------
    is_anonymous: bool
        Indicates whether the cheer was made anonymously.
    user_id: Optional[str]
        The ID of the user who made the cheer, if not anonymous.
    user_login: Optional[str]
        The login name of the user who made the cheer, if not anonymous.
    user_name: Optional[str]
        The display name of the user who made the cheer, if not anonymous.
    message: str
        The message accompanying the cheer.
    bits: int
        The number of bits cheered.
    """
    is_anonymous: bool
    user_id: Optional[str]
    user_login: Optional[str]
    user_name: Optional[str]
    message: str
    bits: int

# Bits use
class Emote(TypedDict):
    """
    Represents metadata about an emote.

    Attributes
    ----------
    id: str
        The unique identifier for the emote.
    emote_set_id: str
        The identifier for the emote set the emote belongs to.
    owner_id: str
        The ID of the broadcaster who owns the emote.
    format: list of {'animated', 'static'}
        Available formats for the emote (e.g., static PNG or animated GIF).
    """
    id: str
    emote_set_id: str
    owner_id: str
    format: List[Literal["animated", "static"]]


class Cheermote(TypedDict):
    """
    Represents metadata about a cheermote.

    Attributes
    ----------
    prefix: str
        The prefix of the Cheermote string used in chat.
    bits: int
        The number of Bits cheered.
    tier: int
        The tier level of the cheermote.
    """
    prefix: str
    bits: int
    tier: int


class Fragment(TypedDict):
    """
    Represents a fragment of a chat message.

    Attributes
    ----------
    text: str
        The message text within the fragment.
    type: Literal["text", "cheermote", "emote"]
        The type of fragment (text, cheermote, or emote).
    emote: Optional[Emote]
        Metadata about the emote if the fragment contains one.
    """
    text: str
    type: Literal["text", "cheermote", "emote"]
    emote: Optional[Emote]


class Message(TypedDict):
    """
    Represents a chat message with potential emotes and cheermotes.

    Attributes
    ----------
    text: str
        The complete message in plain text.
    fragments: list of Fragment
        The ordered list of message fragments.
    """
    text: str
    fragments: List[Fragment]


class PowerUp(TypedDict):
    """
    Represents a Power-up event in chat.

    Attributes
    ----------
    type: Literal["message_effect", "celebration", "gigantify_an_emote"]
        The type of Power-up effect.
    emote: Optional[Emote]
        Associated emote with the Power-up.
    message_effect_id: Optional[str]
        The ID of the message effect.
    """
    type: Literal["message_effect", "celebration", "gigantify_an_emote"]
    emote: Optional[Emote]
    message_effect_id: Optional[str]


class BitsEvent(SpecificBroadcaster, SpecificUser):
    """
    Represents a Bits transaction event.

    Attributes
    ----------
    bits: int
        The number of Bits used.
    type: Literal["cheer", "power_up"]
        The type of Bits event.
    message: Optional[Message]
        An object containing the user message and emote information.
    cheermote: Optional[Cheermote]
        Metadata about the cheermote.
    power_up: Optional[PowerUp]
        Data about Power-up effects.
    """
    bits: int
    type: Literal["cheer", "power_up"]
    message: Optional[Message]
    cheermote: Optional[Cheermote]
    power_up: Optional[PowerUp]

