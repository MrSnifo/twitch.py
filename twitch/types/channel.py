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

from .user import (Broadcaster, SpecificBroadcaster, Moderator, SpecificModerator, SpecificUser)
from typing import TypedDict, Optional, List, Literal
from .stream import Category, SpecificCategory

# ------------------------------------
#            + Channel +
# ------------------------------------
CCLs = Literal['DrugsIntoxication', 'SexualThemes', 'ViolentGraphic', 'Gambling', 'ProfanityVulgarity']


class Channel(Broadcaster):
    tags: List[str]
    delay: int
    title: str
    game_id: str
    game_name: str
    is_branded_content: bool
    broadcaster_language: str
    content_classification_labels: List[CCLs]


# -----------------------------------
#              + User +
# -----------------------------------
class Followed(Broadcaster):
    followed_at: str


class Follower(SpecificUser):
    followed_at: str


class Subscription(Broadcaster, SpecificUser):
    tier: int
    is_gift: bool
    gifter_id: str  # May sometimes be unavailable.
    plan_name: str  # May sometimes be unavailable.
    gifter_name: str  # May sometimes be unavailable.
    gifter_login: str  # May sometimes be unavailable.


class Editor(TypedDict, total=False):
    user_id: str
    user_name: str
    created_at: str
    user_login: str  # Does not include in the API.


class UserBitsLeaderboard(SpecificUser):
    rank: int
    score: int


class BannedUser(SpecificUser, Moderator):
    reason: str
    created_at: str
    expires_at: str


# -------------+ EventSub +-------------
class BannedUserEvent(SpecificBroadcaster, SpecificModerator, SpecificUser):
    reason: str
    ends_at: Optional[str]
    banned_at: str
    is_permanent: bool


class UnBannedUserEvent(SpecificBroadcaster, SpecificModerator, SpecificUser):
    pass


# ----------------------------------
#           + Extension +
# ----------------------------------
ExtensionType = Literal['component', 'mobile', 'overlay', 'panel']


class Extension(TypedDict):
    id: str
    name: str
    type: List[ExtensionType]
    version: str
    can_activate: bool


class ActiveExtension(TypedDict, total=False):
    x: str  # May sometimes be unavailable.
    y: str  # May sometimes be unavailable.
    id: str
    name: str
    active: bool
    version: str
    slot_number: int  # Does not include in the API.


class Extensions(TypedDict):
    panel: List[ActiveExtension]
    overlay: List[ActiveExtension]
    component: List[ActiveExtension]


# -----------------------------------
#            + Schedule +
# -----------------------------------
class ScheduleSegment(TypedDict):
    id: str
    title: str
    category: Category
    end_time: str
    start_time: str
    is_recurring: bool
    canceled_until: Optional[str]


class ScheduleVacation(TypedDict):
    end_time: str
    start_time: str


class Schedule(Broadcaster):
    segments: List[ScheduleSegment]
    vacation: Optional[ScheduleVacation]


# ----------------------------------
#           + Charity +
# ----------------------------------
CharityAmount = TypedDict('CharityAmount', {'value': int, 'decimal_places': int, 'currency': str})


class Charity(Broadcaster):
    id: str
    charity_logo: str
    charity_name: str
    target_amount: Optional[CharityAmount]
    current_amount: CharityAmount
    charity_website: str
    charity_description: str


class CharityDonation(SpecificUser):
    id: str
    amount: CharityAmount
    campaign_id: str


# -------------+ EventSub +-------------
class ChannelUpdateEvent(SpecificBroadcaster, SpecificCategory):
    title: str
    language: str
    content_classification_labels: List[str]


class CharityDonationEvent(SpecificBroadcaster, CharityDonation):
    charity_logo: str
    charity_name: str
    charity_website: str
    charity_description: str


class CharityStartEvent(CharityDonation):
    started_at: str


class CharityStopEvent(CharityDonation):
    stopped_at: str


# ----------------------------------
#             + Video +
# ----------------------------------
VideoMutedSegments = TypedDict('VideoMutedSegments', {'duration': int, 'offset': int})


class Video(SpecificUser):
    id: str
    url: str
    type: Literal['archive', 'highlight', 'upload']
    title: str
    duration: str
    language: str
    viewable: str
    stream_id: Optional[str]
    created_at: str
    view_count: str
    description: str
    published_at: str
    thumbnail_url: str
    muted_segments: Optional[VideoMutedSegments]


# ---------------------------------
#             + Clip +
# ---------------------------------
class Clip(TypedDict, total=False):
    id: str
    url: str
    title: str
    game_id: str
    duration: float
    language: str
    video_id: str
    embed_url: str
    created_at: str
    creator_id: str
    view_count: int
    vod_offset: Optional[int]
    creator_name: str
    creator_login: str  # Does not include in the API.
    thumbnail_url: str
    broadcaster_id: str
    broadcaster_name: str
    broadcaster_login: str  # Does not include in the API.
