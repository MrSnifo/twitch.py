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

from .users import SpecificUser, Broadcaster, Moderator
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from typing import Optional, Literal


# Automod
class AutoModMessageStatus(TypedDict):
    """
    Represents the status of an AutoMod message.

    Attributes
    ----------
    msg_id: str
        The unique identifier for the message.
    is_permitted: bool
        Whether the message was permitted by AutoMod.
    """
    msg_id: str
    is_permitted: bool


class AutoModSettings(TypedDict):
    """
    Represents AutoMod settings.

    Attributes
    ----------
    broadcaster_id: str
        The ID of the broadcaster.
    moderator_id: str
        The ID of the moderator.
    overall_level: Optional[int]
        The overall level of AutoMod moderation.
    disability: int
        The level of moderation for disability-related content.
    aggression: int
        The level of moderation for aggressive content.
    sexuality_sex_or_gender: int
        The level of moderation for content related to sexuality, sex, or gender.
    misogyny: int
        The level of moderation for misogynistic content.
    bullying: int
        The level of moderation for bullying-related content.
    swearing: int
        The level of moderation for swearing.
    race_ethnicity_or_religion: int
        The level of moderation for content related to race, ethnicity, or religion.
    sex_based_terms: int
        The level of moderation for sex-based terms.
    """
    broadcaster_id: str
    moderator_id: str
    overall_level: Optional[int]
    disability: int
    aggression: int
    sexuality_sex_or_gender: int
    misogyny: int
    bullying: int
    swearing: int
    race_ethnicity_or_religion: int
    sex_based_terms: int


# Ban / Unban
class BannedUser(SpecificUser, Moderator):
    """
    Represents a banned user.

    Attributes
    ----------
    reason: str
        The reason the user was banned.
    created_at: str
        The timestamp when the ban was created.
    expires_at: str
        The timestamp when the ban expires.
    """
    reason: str
    created_at: str
    expires_at: str


class BanUser(TypedDict):
    """
    Represents a request to ban a user.

    Attributes
    ----------
    broadcaster_id: str
        The ID of the broadcaster.
    moderator_id: str
        The ID of the moderator issuing the ban.
    user_id: str
        The ID of the user to be banned.
    created_at: str
        The timestamp when the ban was created.
    end_time: str
        The timestamp when the ban will end.
    """
    broadcaster_id: str
    moderator_id: str
    user_id: str
    created_at: str
    end_time: str


class UnBanRequest(Broadcaster, Moderator, SpecificUser):
    """
    Represents a request to unban a user.

    Attributes
    ----------
    id: str
        The unique identifier for the unban request.
    text: str
        The text of the unban request.
    status: Literal['pending', 'approved', 'denied', 'acknowledged', 'canceled']
        The status of the unban request.
    created_at: str
        The timestamp when the request was created.
    resolved_at: Optional[str]
        The timestamp when the request was resolved.
    resolution_text: Optional[str]
        The resolution text of the request, if applicable.
    """
    id: str
    text: str
    status: Literal['pending', 'approved', 'denied', 'acknowledged', 'canceled']
    created_at: str
    resolved_at: Optional[str]
    resolution_text: Optional[str]


# BlockedTerms
class BlockedTerm(TypedDict):
    """
    Represents a blocked term.

    Attributes
    ----------
    broadcaster_id: str
        The ID of the broadcaster.
    moderator_id: str
        The ID of the moderator.
    id: str
        The unique identifier for the blocked term.
    text: str
        The text of the blocked term.
    created_at: str
        The timestamp when the term was blocked.
    updated_at: str
        The timestamp when the term was last updated.
    expires_at: Optional[str]
        The timestamp when the block will expire, if applicable.
    """
    broadcaster_id: str
    moderator_id: str
    id: str
    text: str
    created_at: str
    updated_at: str
    expires_at: Optional[str]


# ShieldMode
class ShieldModeStatus(TypedDict):
    """
    Represents the status of Shield Mode.

    Attributes
    ----------
    is_active: bool
        Indicates if Shield Mode is active.
    moderator_id: str
        The ID of the moderator who activated Shield Mode.
    moderator_login: str
        The login name of the moderator who activated Shield Mode.
    moderator_name: str
        The display name of the moderator who activated Shield Mode.
    last_activated_at: str
        The timestamp when Shield Mode was last activated.
    """
    is_active: bool
    moderator_id: str
    moderator_login: str
    moderator_name: str
    last_activated_at: str


# Warning
class UserWarningResponse(TypedDict):
    """
    Represents a warning issued to a user.

    Attributes
    ----------
    broadcaster_id: str
        The ID of the broadcaster issuing the warning.
    user_id: str
        The ID of the user receiving the warning.
    moderator_id: str
        The ID of the moderator issuing the warning.
    reason: str
        The reason for the warning.
    """
    broadcaster_id: str
    user_id: str
    moderator_id: str
    reason: str
