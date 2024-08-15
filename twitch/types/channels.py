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

from .users import Broadcaster, SpecificUser
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from typing import List, Literal, Dict, Optional, NotRequired


# Channel
class CCL(TypedDict):
    """
    Represents a Content Classification Label (CCL).

    Attributes
    ----------
    id: Literal['DrugsIntoxication', 'SexualThemes', 'ViolentGraphic', 'Gambling', 'ProfanityVulgarity']
        The type of content classification.
    is_enabled: bool
        Indicates if the classification is enabled.
    """
    id: Literal['DrugsIntoxication', 'SexualThemes', 'ViolentGraphic', 'Gambling', 'ProfanityVulgarity']
    is_enabled: bool


class ChannelInfo(Broadcaster):
    """
    Represents channel information.

    Attributes
    ----------
    broadcaster_language: str
        The language of the broadcaster.
    game_id: str
        The ID of the current game being played on the channel.
    game_name: str
        The name of the current game being played on the channel.
    title: str
        The title of the broadcast.
    delay: int
        The delay of the broadcast in seconds.
    tags: List[str]
        A list of tags associated with the broadcast.
    content_classification_labels: List[CCL]
        A list of content classification labels for the broadcast.
    is_branded_content: bool
        Indicates if the content is branded.
    """
    broadcaster_language: str
    game_id: str
    game_name: str
    title: str
    delay: int
    tags: List[str]
    content_classification_labels: List[CCL]
    is_branded_content: bool


class Editor(TypedDict):
    """
    Represents an editor of the channel.

    Attributes
    ----------
    user_id: str
        The ID of the editor.
    user_name: str
        The name of the editor.
    created_at: str
        The timestamp when the editor was added.
    """
    user_id: str
    user_name: str
    created_at: str


class Follows(Broadcaster):
    """
    Represents a follow relationship.

    Attributes
    ----------
    followed_at: str
        The timestamp when the channel was followed.
    """
    followed_at: str


class Follower(SpecificUser):
    """
    Represents a follower.

    Attributes
    ----------
    followed_at: str
        The timestamp when the user followed the channel.
    """
    followed_at: str


# Subscription
class Subscription(Broadcaster, SpecificUser):
    """
    Represents a subscription.

    Attributes
    ----------
    gifter_id: str
        The ID of the user who gifted the subscription.
    gifter_login: str
        The login name of the user who gifted the subscription.
    gifter_name: str
        The display name of the user who gifted the subscription.
    is_gift: bool
        Indicates if the subscription was a gift.
    plan_name: str
        The name of the subscription plan.
    tier: Literal['1000', '2000', '3000']
        The tier of the subscription.
    """
    gifter_id: str
    gifter_login: str
    gifter_name: str
    is_gift: bool
    plan_name: str
    tier: Literal['1000', '2000', '3000']


class SubscriptionCheck(Broadcaster, total=False):
    """
    Represents check subscription details.

    Attributes
    ----------
    gifter_id: NotRequired[str]
        The ID of the user who gifted the subscription.
    gifter_login: NotRequired[str]
        The login name of the user who gifted the subscription.
    gifter_name: NotRequired[str]
        The display name of the user who gifted the subscription.
    is_gift: bool
        Indicates if the subscription was a gift.
    tier: Literal['1000', '2000', '3000']
        The tier of the subscription.
    """
    gifter_id: NotRequired[str]
    gifter_login: NotRequired[str]
    gifter_name: NotRequired[str]
    is_gift: bool
    tier: Literal['1000', '2000', '3000']


# Clip
class ClipEdit(TypedDict):
    """
    Represents a clip edit.

    Attributes
    ----------
    edit_url: str
        The URL to edit the clip.
    id: str
        The ID of the clip.
    """
    edit_url: str
    id: str


class Clip(TypedDict):
    """
    Represents a clip.

    Attributes
    ----------
    id: str
        The ID of the clip.
    url: str
        The URL of the clip.
    title: str
        The title of the clip.
    game_id: str
        The ID of the game being played in the clip.
    duration: float
        The duration of the clip in seconds.
    language: str
        The language of the clip.
    video_id: str
        The ID of the video from which the clip was created.
    embed_url: str
        The URL to embed the clip.
    created_at: str
        The timestamp when the clip was created.
    creator_id: str
        The ID of the creator of the clip.
    view_count: int
        The number of views the clip has.
    vod_offset: Optional[int]
        The offset in the VOD where the clip starts.
    creator_name: str
        The display name of the creator of the clip.
    thumbnail_url: str
        The URL of the clip's thumbnail.
    broadcaster_id: str
        The ID of the broadcaster of the clip.
    broadcaster_name: str
        The display name of the broadcaster of the clip.
    """
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
    thumbnail_url: str
    broadcaster_id: str
    broadcaster_name: str


# Video
class VideoMutedSegments(TypedDict):
    """
    Represents muted segments in a video.

    Attributes
    ----------
    duration: int
        The duration of the muted segment in seconds.
    offset: int
        The offset in the video where the muted segment starts.
    """
    duration: int
    offset: int


class Video(SpecificUser):
    """
    Represents a video.

    Attributes
    ----------
    id: str
        The ID of the video.
    url: str
        The URL of the video.
    type: Literal['archive', 'highlight', 'upload']
        The type of video.
    title: str
        The title of the video.
    duration: str
        The duration of the video in the format 'HH:MM:SS'.
    language: str
        The language of the video.
    viewable: str
        Indicates if the video is viewable.
    stream_id: Optional[str]
        The ID of the stream from which the video was created.
    created_at: str
        The timestamp when the video was created.
    view_count: str
        The number of views the video has.
    description: str
        The description of the video.
    published_at: str
        The timestamp when the video was published.
    thumbnail_url: str
        The URL of the video's thumbnail.
    muted_segments: Optional[VideoMutedSegments]
        A list of muted segments in the video.
    """
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


# Extension
class Extension(TypedDict):
    """
    Represents an extension.

    Attributes
    ----------
    id: str
        The ID of the extension.
    version: str
        The version of the extension.
    name: str
        The name of the extension.
    can_activate: bool
        Indicates if the extension can be activated.
    type: List[Literal['component', 'mobile', 'overlay', 'panel']]
        The types of the extension.
    """
    id: str
    version: str
    name: str
    can_activate: bool
    type: List[Literal['component', 'mobile', 'overlay', 'panel']]


class ExtensionDetails(TypedDict, total=False):
    """
    Represents details of an extension.

    Attributes
    ----------
    active: bool
        Indicates if the extension is active.
    id: NotRequired[str]
        The ID of the extension (optional).
    version: NotRequired[str]
        The version of the extension (optional).
    name: NotRequired[str]
        The name of the extension (optional).
    x: NotRequired[int]
        The x-coordinate for positioning the extension (optional).
    y: NotRequired[int]
        The y-coordinate for positioning the extension (optional).
    """
    active: bool
    id: NotRequired[str]
    version: NotRequired[str]
    name: NotRequired[str]
    x: NotRequired[int]
    y: NotRequired[int]


class ActiveExtensions(TypedDict):
    """
    Represents active extensions.

    Attributes
    ----------
    panel: Dict[str, ExtensionDetails]
        The active panel extensions.
    overlay: Dict[str, ExtensionDetails]
        The active overlay extensions.
    component: Dict[str, ExtensionDetails]
        The active component extensions.
    """
    panel: Dict[str, ExtensionDetails]
    overlay: Dict[str, ExtensionDetails]
    component: Dict[str, ExtensionDetails]


# Teams
class ChannelTeam(TypedDict):
    """
    Represents a channel team.

    Attributes
    ----------
    background_image_url: str
        The URL of the team's background image.
    banner: str
        The team's banner.
    created_at: str
        The timestamp when the team was created.
    updated_at: str
        The timestamp when the team was last updated.
    info: str
        Information about the team.
    thumbnail_url: str
        The URL of the team's thumbnail image.
    team_name: str
        The name of the team.
    team_display_name: str
        The display name of the team.
    id: str
        The ID of the team.
    """
    background_image_url: str
    banner: str
    created_at: str
    updated_at: str
    info: str
    thumbnail_url: str
    team_name: str
    team_display_name: str
    id: str


class Team(TypedDict):
    """
    Represents a team.

    Attributes
    ----------
    background_image_url: str
        The URL of the team's background image.
    banner: str
        The team's banner.
    created_at: str
        The timestamp when the team was created.
    updated_at: str
        The timestamp when the team was last updated.
    info: str
        Information about the team.
    thumbnail_url: str
        The URL of the team's thumbnail image.
    team_name: str
        The name of the team.
    team_display_name: str
        The display name of the team.
    id: str
        The ID of the team.
    users: List[SpecificUser]
        A list of users in the team.
    """
    background_image_url: str
    banner: str
    created_at: str
    updated_at: str
    info: str
    thumbnail_url: str
    team_name: str
    team_display_name: str
    id: str
    users: List[SpecificUser]
