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

from .users import SpecificBroadcaster, SpecificUser, SpecificModerator, Moderator
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from typing import List, Optional, Literal


# AutoMod
class Emote(TypedDict):
    """
    Represents an emote.

    Attributes
    ----------
    id: str
        The ID of the emote.
    emote_set_id: str
        The ID of the emote set to which the emote belongs.
    """
    id: str
    emote_set_id: str


class Cheermote(TypedDict):
    """
    Represents a cheermote.

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


class Fragment(TypedDict):
    """
    Represents a fragment of a message that can be an emote or cheermote.

    Attributes
    ----------
    text: str
        The text content of the fragment.
    emote: Optional[Emote]
        The emote in the fragment, if any.
    cheermote: Optional[Cheermote]
        The cheermote in the fragment, if any.
    """
    text: str
    emote: Optional[Emote]
    cheermote: Optional[Cheermote]


class Message(TypedDict):
    """
    Represents a message with its content and fragments.

    Attributes
    ----------
    text: str
        The text content of the message.
    fragments: List[Fragment]
        A list of fragments in the message.
    """
    text: str
    fragments: List[Fragment]


class AutomodMessageHoldEvent(SpecificBroadcaster, SpecificUser):
    """
    Represents an event where a message is held by AutoMod.

    Attributes
    ----------
    message_id: str
        The ID of the held message.
    message: Message
        The details of the held message.
    category: str
        The category of the AutoMod action.
    level: int
        The moderation level of the AutoMod action.
    held_at: str
        The timestamp when the message was held, in ISO 8601 format.
    """
    message_id: str
    message: Message
    category: str
    level: int
    held_at: str


class AutomodMessageUpdateEvent(SpecificBroadcaster, SpecificModerator, SpecificUser):
    """
    Represents an event where a held message is updated by AutoMod.

    Attributes
    ----------
    message_id: str
        The ID of the updated message.
    message: Message
        The updated message details.
    category: str
        The category of the AutoMod action.
    level: int
        The moderation level of the AutoMod action.
    status: Literal['Approved', 'Denied', 'Expired']
        The current status of the message.
    held_at: str
        The timestamp when the message was held, in ISO 8601 format.
    """
    message_id: str
    message: Message
    category: str
    level: int
    status: Literal['Approved', 'Denied', 'Expired']
    held_at: str


class AutomodSettingsUpdateEvent(SpecificBroadcaster, SpecificModerator):
    """
    Represents an event where AutoMod settings are updated.

    Attributes
    ----------
    bullying: int
        The level of moderation for bullying.
    overall_level: Optional[int]
        The overall moderation level, if applicable.
    disability: int
        The level of moderation for disability-related terms.
    race_ethnicity_or_religion: int
        The level of moderation for race, ethnicity, or religion.
    misogyny: int
        The level of moderation for misogyny.
    sexuality_sex_or_gender: int
        The level of moderation for sexuality, sex, or gender.
    aggression: int
        The level of moderation for aggression.
    sex_based_terms: int
        The level of moderation for sex-based terms.
    swearing: int
        The level of moderation for swearing.
    """
    bullying: int
    overall_level: Optional[int]
    disability: int
    race_ethnicity_or_religion: int
    misogyny: int
    sexuality_sex_or_gender: int
    aggression: int
    sex_based_terms: int
    swearing: int


class AutomodTermsUpdateEvent(SpecificBroadcaster, SpecificModerator):
    """
    Represents an event where AutoMod terms are updated.

    Attributes
    ----------
    action: Literal['add_permitted', 'remove_permitted', 'add_blocked', 'remove_blocked']
        The action taken on the terms.
    from_automod: bool
        Whether the terms update is from AutoMod.
    terms: List[str]
        A list of terms involved in the update.
    """
    action: Literal['add_permitted', 'remove_permitted', 'add_blocked', 'remove_blocked']
    from_automod: bool
    terms: List[str]


class BanEvent(SpecificBroadcaster, SpecificModerator, SpecificUser):
    """
    Represents an event where a user is banned.

    Attributes
    ----------
    reason: str
        The reason for the ban.
    banned_at: str
        The timestamp when the ban was applied, in ISO 8601 format.
    ends_at: Optional[str]
        The timestamp when the ban will end, if applicable.
    is_permanent: bool
        Whether the ban is permanent.
    """
    reason: str
    banned_at: str
    ends_at: Optional[str]
    is_permanent: bool


class UnbanEvent(SpecificBroadcaster, SpecificModerator, SpecificUser):
    """
    Represents an event where a user is unbanned.

    Attributes
    ----------
    (No additional attributes; inherits from SpecificBroadcaster, SpecificModerator, SpecificUser)
    """
    pass


class UnbanRequestCreateEvent(SpecificBroadcaster, SpecificUser):
    """
    Represents an event where an unban request is created.

    Attributes
    ----------
    id: str
        The ID of the unban request.
    text: str
        The text of the unban request.
    created_at: str
        The timestamp when the unban request was created, in ISO 8601 format.
    """
    id: str
    text: str
    created_at: str


class UnbanRequestResolveEvent(SpecificBroadcaster, Moderator, SpecificUser):
    """
    Represents an event where an unban request is resolved.

    Attributes
    ----------
    id: str
        The ID of the unban request.
    resolution_text: Optional[str]
        The resolution text or reason for the decision.
    status: str
        The status of the unban request.
    """
    id: str
    resolution_text: Optional[str]
    status: str


class FollowersMetadata(TypedDict):
    """
    Represents metadata related to followers.

    Attributes
    ----------
    follow_duration_minutes: int
        The duration for which the user has been following, in minutes.
    """
    follow_duration_minutes: int


class SlowMetadata(TypedDict):
    """
    Represents metadata related to slow mode.

    Attributes
    ----------
    wait_time_seconds: int
        The wait time for slow mode, in seconds.
    """
    wait_time_seconds: int


class BanMetadata(SpecificUser):
    """
    Represents metadata related to a ban.

    Attributes
    ----------
    reason: Optional[str]
        The reason for the ban, if provided.
    """
    reason: Optional[str]


class TimeoutMetadata(SpecificUser):
    """
    Represents metadata related to a timeout.

    Attributes
    ----------
    reason: Optional[str]
        The reason for the timeout, if provided.
    expires_at: Optional[str]
        The timestamp when the timeout will end, in ISO 8601 format.
    """
    reason: Optional[str]
    expires_at: Optional[str]


class RaidMetadata(SpecificUser):
    """
    Represents metadata related to a raid.

    Attributes
    ----------
    viewer_count: int
        The number of viewers involved in the raid.
    """
    viewer_count: int


class DeleteMetadata(SpecificUser):
    """
    Represents metadata related to a message deletion.

    Attributes
    ----------
    message_id: str
        The ID of the deleted message.
    message_body: str
        The body of the deleted message.
    """
    message_id: str
    message_body: str


class AutomodTermsMetadata(TypedDict):
    """
    Represents metadata related to AutoMod terms updates.

    Attributes
    ----------
    action: Literal['add', 'remove']
        The action taken on the terms.
    list: Literal['blocked', 'permitted']
        The list to which the terms were added or removed.
    terms: List[str]
        A list of terms involved in the update.
    from_automod: bool
        Whether the terms update is from AutoMod.
    """
    action: Literal['add', 'remove']
    list: Literal['blocked', 'permitted']
    terms: List[str]
    from_automod: bool


class UnbanRequestMetadata(SpecificUser):
    """
    Represents metadata related to an unban request.

    Attributes
    ----------
    is_approved: bool
        Whether the unban request was approved.
    moderator_message: Optional[str]
        The message from the moderator regarding the unban request.
    """
    is_approved: bool
    moderator_message: Optional[str]


class WarnMetadata(SpecificUser):
    """
    Represents metadata related to a warning.

    Attributes
    ----------
    reason: Optional[str]
        The reason for the warning, if provided.
    chat_rules_cited: Optional[List[str]]
        A list of chat rules cited in the warning, if any.
    """
    reason: Optional[str]
    chat_rules_cited: Optional[List[str]]


class ModerateEvent(SpecificBroadcaster, SpecificModerator):
    """
    Represents an event where moderation actions are taken.

    Attributes
    ----------
    action: str
        The type of moderation action.
    followers: Optional[FollowersMetadata]
        Metadata related to followers, if applicable.
    slow: Optional[SlowMetadata]
        Metadata related to slow mode, if applicable.
    vip: Optional[SpecificUser]
        The user who was made a VIP, if applicable.
    unvip: Optional[SpecificUser]
        The user who was removed from VIP status, if applicable.
    mod: Optional[SpecificUser]
        The user who was given moderator status, if applicable.
    unmod: Optional[SpecificUser]
        The user who was removed from moderator status, if applicable.
    ban: Optional[BanMetadata]
        Metadata related to a ban, if applicable.
    unban: Optional[SpecificUser]
        The user who was unbanned, if applicable.
    timeout: Optional[TimeoutMetadata]
        Metadata related to a timeout, if applicable.
    untimeout: Optional[SpecificUser]
        The user who was removed from timeout status, if applicable.
    raid: Optional[RaidMetadata]
        Metadata related to a raid, if applicable.
    unraid: Optional[SpecificUser]
        The user who was removed from raid status, if applicable.
    delete: Optional[DeleteMetadata]
        Metadata related to a message deletion, if applicable.
    automod_terms: Optional[AutomodTermsMetadata]
        Metadata related to AutoMod terms updates, if applicable.
    unban_request: Optional[UnbanRequestMetadata]
        Metadata related to an unban request, if applicable.
    warn: Optional[WarnMetadata]
        Metadata related to a warning, if applicable.
    shared_chat_ban: Optional[BanMetadata]
        Information about the shared_chat_ban event, if applicable.
    shared_chat_unban: Optional[SpecificUser]
        Information about the shared_chat_unban event, if applicable.
    shared_chat_timeout: Optional[TimeoutMetadata]
        Information about the shared_chat_timeout event, if applicable.
    shared_chat_untimeout: Optional[SpecificUser]
        Information about the shared_chat_untimeout event, if applicable.
    shared_chat_delete: Optional[DeleteMetadata]
        Information about the shared_chat_delete event, if applicable.
    """
    action: str
    followers: Optional[FollowersMetadata]
    slow: Optional[SlowMetadata]
    vip: Optional[SpecificUser]
    unvip: Optional[SpecificUser]
    mod: Optional[SpecificUser]
    unmod: Optional[SpecificUser]
    ban: Optional[BanMetadata]
    unban: Optional[SpecificUser]
    timeout: Optional[TimeoutMetadata]
    untimeout: Optional[SpecificUser]
    raid: Optional[RaidMetadata]
    unraid: Optional[SpecificUser]
    delete: Optional[DeleteMetadata]
    automod_terms: Optional[AutomodTermsMetadata]
    unban_request: Optional[UnbanRequestMetadata]
    warn: Optional[WarnMetadata]
    shared_chat_ban: Optional[BanMetadata]
    shared_chat_unban: Optional[SpecificUser]
    shared_chat_timeout: Optional[TimeoutMetadata]
    shared_chat_untimeout: Optional[SpecificUser]
    shared_chat_delete: Optional[DeleteMetadata]


# Moderator Add/Remove
class ModeratorAddEvent(SpecificBroadcaster, SpecificUser):
    """
    Represents an event where a user is added as a moderator.

    Attributes
    ----------
    (No additional attributes; inherits from SpecificBroadcaster, SpecificUser)
    """
    pass


class ModeratorRemoveEvent(SpecificBroadcaster, SpecificUser):
    """
    Represents an event where a user is removed as a moderator.

    Attributes
    ----------
    (No additional attributes; inherits from SpecificBroadcaster, SpecificUser)
    """
    pass


# SuspiciousUser
class ChatFragment(TypedDict):
    """
    Represents a fragment of a chat message.

    Attributes
    ----------
    type: Literal['text', 'cheermote', 'emote']
        The type of fragment.
    text: str
        The text content of the fragment.
    cheermote: Optional[Cheermote]
        The cheermote in the fragment, if any.
    emote: Optional[Emote]
        The emote in the fragment, if any.
    """
    type: Literal['text', 'cheermote', 'emote']
    text: str
    cheermote: Optional[Cheermote]
    emote: Optional[Emote]


class ChatMessage(TypedDict):
    """
    Represents a chat message with its fragments.

    Attributes
    ----------
    message_id: str
        The ID of the chat message.
    text: str
        The text content of the chat message.
    fragments: List[ChatFragment]
        A list of fragments in the chat message.
    """
    message_id: str
    text: str
    fragments: List[ChatFragment]


class SuspiciousUserUpdateEvent(SpecificBroadcaster, SpecificModerator, SpecificUser):
    """
    Represents an update to a suspicious user's status.

    Attributes
    ----------
    low_trust_status: Literal['none', 'active_monitoring', 'restricted']
        The current low trust status of the user.
    """
    low_trust_status: Literal['none', 'active_monitoring', 'restricted']


class SuspiciousUserMessageEvent(SpecificBroadcaster, SpecificUser):
    """
    Represents an event where a suspicious user sends a message.

    Attributes
    ----------
    low_trust_status: Literal['none', 'active_monitoring', 'restricted']
        The current low trust status of the user.
    shared_ban_channel_ids: List[str]
        A list of channel IDs where the user has shared bans.
    types: List[Literal['manual', 'ban_evader_detector', 'shared_channel_ban']]
        A list of types associated with the suspicious behavior.
    ban_evasion_evaluation: Literal['unknown', 'possible', 'likely']
        The evaluation of ban evasion.
    message: ChatMessage
        The message sent by the suspicious user.
    """
    low_trust_status: Literal['none', 'active_monitoring', 'restricted']
    shared_ban_channel_ids: List[str]
    types: List[Literal['manual', 'ban_evader_detector', 'shared_channel_ban']]
    ban_evasion_evaluation: Literal['unknown', 'possible', 'likely']
    message: ChatMessage


# Warning
class WarningAcknowledgeEvent(SpecificBroadcaster, SpecificUser):
    """
    Represents an event where a warning is acknowledged.

    Attributes
    ----------
    (No additional attributes; inherits from SpecificBroadcaster, SpecificUser)
    """
    pass


class WarningSendEvent(SpecificBroadcaster, SpecificModerator, SpecificUser):
    """
    Represents an event where a warning is sent.

    Attributes
    ----------
    reason: Optional[str]
        The reason for the warning, if provided.
    chat_rules_cited: Optional[List[str]]
        A list of chat rules cited in the warning, if any.
    """
    reason: Optional[str]
    chat_rules_cited: Optional[List[str]]


# ShieldMode
class ShieldModeBeginEvent(SpecificBroadcaster, SpecificModerator):
    """
    Represents an event where Shield Mode begins.

    Attributes
    ----------
    started_at: str
        The timestamp when Shield Mode began, in ISO 8601 format.
    """
    started_at: str


class ShieldModeEndEvent(SpecificBroadcaster, SpecificModerator):
    """
    Represents an event where Shield Mode ends.

    Attributes
    ----------
    ended_at: str
        The timestamp when Shield Mode ended, in ISO 8601 format.
    """
    ended_at: str