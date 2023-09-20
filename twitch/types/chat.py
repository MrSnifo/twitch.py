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

from .user import (SpecificBroadcaster, Moderator, SpecificModerator, SpecificDisplayUser)
from typing import TypedDict, List, Literal, Optional, Dict

# Announcement colors.
AnnouncementColors = Literal['blue', 'green', 'orange', 'purple', 'primary']
Images = TypedDict('Images', {'url_1x': str, 'url_2x': str, 'url_4x': str})

# ------------------------------------
#              + User +
# ------------------------------------
UserColors = Literal['blue', 'blue_violet', 'cadet_blue', 'chocolate', 'coral', 'dodger_blue', 'firebrick',
                     'golden_rod', 'green', 'hot_pink', 'orange_red', 'red', 'sea_green', 'spring_green',
                     'yellow_green']


class UserChatColor(SpecificDisplayUser):
    color: str


# --------------------------------------
#              + Message +
# --------------------------------------
class MessageEmote(TypedDict):
    begin: int
    end: int
    id: str


class SubscriptionMessage(TypedDict):
    text: str
    emotes: List[MessageEmote]


class Command(TypedDict):
    command: str
    channel: str
    content: str


class Source(TypedDict):
    nick: str
    host: str


class ChatMessage(TypedDict):
    command: Command
    source: Source
    tags: Optional[Dict[str, str]]
    parameters: str


# ------------------------------------
#              + Emote +
# ------------------------------------
class BaseEmote(TypedDict):
    id: str
    name: str
    images: Images
    format: List[Literal['animated', 'static']]
    scale: List[Literal['1.0', '2.0', '3.0']]
    theme_mode: List[Literal['dark', 'light']]


class Emote(BaseEmote):
    tier: str
    emote_type: Literal['bitstier', 'follower', 'subscriptions']
    emote_set_id: str


# --------------------------------------
#             + Cheermote +
# --------------------------------------
CheermoteImages = TypedDict('CheermoteImages', {'1': str, '1.5': str, '2': str, '3': str, '4': str})
ImagesType = TypedDict('ImagesType', {'animated': CheermoteImages, 'static': CheermoteImages})
TierImages = TypedDict('TierImages', {'dark': ImagesType, 'light': ImagesType})


class Tier(TypedDict):
    id: str
    min_bits: Literal[1, 100, 500, 1000, 5000, 10000, 100000]
    color: str
    images: TierImages
    can_cheer: bool
    show_in_bits_card: bool


class Cheermote(TypedDict):
    prefix: str
    tiers: List[Tier]
    type: Literal['global_first_party', 'global_third_party', 'channel_custom', 'display_only', 'sponsored']
    order: int
    last_updated: str
    is_charitable: bool


# ------------------------------------
#              + Badge +
# ------------------------------------
class BadgeVersion(TypedDict):
    id: str
    image_url_1x: str
    image_url_2x: str
    image_url_4x: str
    title: str
    description: str
    click_action: Optional[str]
    click_url: Optional[str]


class Badge(TypedDict):
    set_id: str
    versions: List[BadgeVersion]


# -------------------------------------
#          + Chat Settings +
# -------------------------------------
class ChatSettings(TypedDict, total=False):
    broadcaster_id: str
    emote_mode: bool
    follower_mode: bool
    follower_mode_duration: Optional[int]
    moderator_id: str
    non_moderator_chat_delay: bool  # May sometimes be unavailable.
    non_moderator_chat_delay_duration: int  # May sometimes be unavailable.
    slow_mode: bool
    slow_mode_wait_time: Optional[bool]
    subscriber_mode: bool
    unique_chat_mode: bool


class ChatSettingsToJson(TypedDict):
    emote_mode: bool
    follower_mode: bool
    follower_mode_duration: int
    non_moderator_chat_delay: bool
    non_moderator_chat_delay_duration: int
    slow_mode: bool
    slow_mode_wait_time: int
    subscriber_mode: bool
    unique_chat_mode: bool


# ------------------------------------
#             + AutoMod +
# ------------------------------------
class AutoModSettings(TypedDict):
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


class AutoModSettingsToJson(TypedDict):
    bullying: int
    misogyny: int
    swearing: int
    aggression: int
    disability: int
    sex_based_terms: int
    sexuality_sex_or_gender: int
    race_ethnicity_or_religion: int


class BlockedTerm(TypedDict):
    broadcaster_id: str
    moderator_id: str
    id: str
    text: str
    created_at: str
    updated_at: str
    expires_at: Optional[str]


# -------------------------------------
#            + ShieldMode +
# -------------------------------------
class ShieldMode(Moderator):
    is_active: bool
    last_activated_at: str


# -------------+ EventSub +-------------
class ShieldModeBeginEvent(SpecificBroadcaster, SpecificModerator):
    started_at: str


class ShieldModeEndEvent(SpecificBroadcaster, SpecificModerator):
    ended_at: str
