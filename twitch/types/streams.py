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

from .users import SpecificUser, Broadcaster
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from typing import List, Optional, Literal


# Raids
class RaidInfo(TypedDict):
    """
    Represents information about a raid.

    Attributes
    ----------
    created_at: str
        The timestamp when the raid was created.
    is_mature: bool
        Indicates if the raid is flagged as mature.
    """
    created_at: str
    is_mature: bool


# Streams
class StreamKey(TypedDict):
    """
    Represents a stream key.

    Attributes
    ----------
    stream_key: str
        The stream key used to start a stream.
    """
    stream_key: str


class StreamInfo(SpecificUser):
    """
    Represents a stream.

    Attributes
    ----------
    id: str
        The unique identifier for the stream.
    game_id: str
        The ID of the game being streamed.
    game_name: str
        The name of the game being streamed.
    type: str
        The type of stream (live, etc.).
    title: str
        The title of the stream.
    tags: List[str]
        A list of tags associated with the stream.
    viewer_count: int
        The number of viewers watching the stream.
    started_at: str
        The timestamp when the stream started.
    language: str
        The language of the stream.
    thumbnail_url: str
        The URL for the stream's thumbnail image.
    is_mature: bool
        Indicates if the stream is marked as mature content.
    """
    id: str
    game_id: str
    game_name: str
    type: str
    title: str
    tags: List[str]
    viewer_count: int
    started_at: str
    language: str
    thumbnail_url: str
    is_mature: bool


class StreamMarkerInfo(TypedDict):
    """
    Represents information about a stream marker.

    Attributes
    ----------
    id: str
        The unique identifier for the stream marker.
    created_at: str
        The timestamp when the marker was created.
    position_seconds: int
        The position in seconds where the marker was placed.
    description: str
        A description of the marker.
    """
    id: str
    created_at: str
    position_seconds: int
    description: str


class VideoMarker(TypedDict):
    """
    Represents a marker in a video.

    Attributes
    ----------
    id: str
        The unique identifier for the marker.
    created_at: str
        The timestamp when the marker was created.
    description: str
        A description of the marker.
    position_seconds: int
        The position in seconds where the marker was placed.
    url: str
        The URL to access the marker.
    """
    id: str
    created_at: str
    description: str
    position_seconds: int
    url: str


class Video(TypedDict):
    """
    Represents a video with markers.

    Attributes
    ----------
    video_id: str
        The unique identifier for the video.
    markers: List[Marker]
        A list of markers associated with the video.
    """
    video_id: str
    markers: List[VideoMarker]


class StreamMarker(SpecificUser):
    """
    Represents a stream marker.

    Attributes
    ----------
    videos: List[Video]
        A list of videos with associated markers.
    """
    videos: List[Video]


# Ads
class CommercialStatus(TypedDict):
    """
    Represents the status of a commercial.

    Attributes
    ----------
    length: int
        The length of the commercial in seconds.
    message: str
        A message associated with the commercial status.
    retry_after: int
        The time in seconds to wait before retrying the commercial.
    """
    length: int
    message: str
    retry_after: int


class AdSnooze(TypedDict):
    """
    Represents the snooze status of ads.

    Attributes
    ----------
    snooze_count: int
        The number of times ads have been snoozed.
    snooze_refresh_at: str
        The timestamp when the snooze refreshes.
    next_ad_at: str
        The timestamp when the next ad is scheduled.
    """
    snooze_count: int
    snooze_refresh_at: str
    next_ad_at: str


class AdSchedule(AdSnooze):
    """
    Represents an ad schedule.

    Attributes
    ----------
    duration: int
        The duration of the ad schedule.
    last_ad_at: str
        The timestamp of the last ad.
    preroll_free_time: int
        The time in seconds before preroll ads are shown.
    """
    duration: int
    last_ad_at: str
    preroll_free_time: int


# Schedule
class ScheduleCategory(TypedDict):
    """
    Represents a schedule category.

    Attributes
    ----------
    id: str
        The unique identifier for the category.
    name: str
        The name of the category.
    """
    id: str
    name: str


class ScheduleSegment(TypedDict):
    """
    Represents a segment in a schedule.

    Attributes
    ----------
    id: str
        The unique identifier for the segment.
    start_time: str
        The start time of the segment.
    end_time: str
        The end time of the segment.
    title: str
        The title of the segment.
    canceled_until: Optional[str]
        The time until which the segment is canceled, if applicable.
    category: Optional[ScheduleCategory]
        The category associated with the segment.
    is_recurring: bool
        Indicates if the segment is recurring.
    """
    id: str
    start_time: str
    end_time: str
    title: str
    canceled_until: Optional[str]
    category: Optional[ScheduleCategory]
    is_recurring: bool


class ScheduleVacation(TypedDict):
    """
    Represents a vacation in a schedule.

    Attributes
    ----------
    start_time: str
        The start time of the vacation.
    end_time: str
        The end time of the vacation.
    """
    start_time: str
    end_time: str


class Schedule(Broadcaster):
    """
    Represents a broadcaster's schedule.

    Attributes
    ----------
    segments: List[ScheduleSegment]
        A list of segments in the schedule.
    vacation: Optional[ScheduleVacation]
        The vacation period in the schedule, if applicable.
    """
    segments: List[ScheduleSegment]
    vacation: Optional[ScheduleVacation]


# CCLs
Locale = Literal[
    'bg-BG',
    'cs-CZ',
    'da-DK',
    'de-DE',
    'el-GR',
    'en-GB',
    'en-US',
    'es-ES',
    'es-MX',
    'fi-FI',
    'fr-FR',
    'hu-HU',
    'it-IT',
    'ja-JP',
    'ko-KR',
    'nl-NL',
    'no-NO',
    'pl-PL',
    'pt-BT',
    'pt-PT',
    'ro-RO',
    'ru-RU',
    'sk-SK',
    'sv-SE',
    'th-TH',
    'tr-TR',
    'vi-VN',
    'zh-CN',
    'zh-TW']


class CCLInfo(TypedDict):
    """
    Represents content classification labels (CCLs) information.

    Attributes
    ----------
    id: str
        The unique identifier for the CCL.
    description: str
        The description of the CCL.
    name: str
        The name of the CCL.
    """
    id: str
    description: str
    name: str
