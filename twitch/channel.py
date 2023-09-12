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
from __future__ import annotations

from .utils import MISSING, convert_rfc3339
from .stream import ChannelStream, Category
from .chat import ChannelChat
from .errors import NotFound
from .user import BaseUser

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Union, Optional, List, AsyncGenerator, Literal
    from .types import channel as ChannelTypes
    from .state import ConnectionState
    from datetime import datetime

__all__ = ('Video', 'VideoMutedSegments',
           'Clip',
           'Channel',
           'Follow', 'Editor', 'BitsLeaderboard', 'BannedUser', 'Subscription',
           'Schedule', 'ScheduleVacation', 'ScheduleSegment',
           'Charity', 'CharityDonation',
           'ChannelFollowers',
           'ChannelExtensions', 'Extensions', 'Extension', 'ActiveExtension', 'BaseExtension',
           'ChannelSchedule',
           'UserChannel')


# ----------------------------------
#             + Video +
# ----------------------------------
class VideoMutedSegments:
    """
    Represents muted segments within a video.

    Attributes
    ----------
    offset: int
        The offset (in seconds) where the muted segment starts.
    duration: int
        The duration (in seconds) of the muted segment.
    """
    __slots__ = ('offset', 'duration')

    if TYPE_CHECKING:
        offset: int
        duration: int

    def __init__(self, data: ChannelTypes.VideoMutedSegments) -> None:
        self._form_data(data=data)

    def __repr__(self) -> str:
        return f'<VideoMutedSegments offset={self.offset} duration={self.duration}>'

    def _form_data(self, data: ChannelTypes.VideoMutedSegments) -> None:
        self.offset = data['offset']
        self.duration = data['duration']


class Video:
    """
    Represents a video on a channel.

    Attributes
    ----------
    id: str
        The unique identifier for the video.
    url: str
        The URL of the video.
    type: str
        The type of video.
    user: BaseUser
        The user who created the video.
    title: str
        The title of the video.
    duration: str
        The duration of the video.
    language: str
        The language of the video.
    stream_id: Optional[str]
        The ID of the associated stream, if available.
    created_at: datetime
        The date and time when the video was created.
    view_count: str
        The number of views for the video.
    description: str
        The description of the video.
    is_viewable: bool
        Indicates whether the video is viewable to the public.
    published_at: datetime
        The date and time when the video was published.
    thumbnail_url: str
        The URL of the video's thumbnail.
    muted_segments: Optional[List[VideoMutedSegments]]
        A list of muted segments in the video, if available.
    is_muted_segments: bool
        Indicates whether the video has muted segments.

    Methods
    -------
    __str__() -> str
        Returns the URL of the video as a string.
    __eq__(other: object) -> bool
        Compares the current Video instance with another Video or Clip instance for equality.
    __ne__(other: object) -> bool
        Compares the current Video instance with another Video or Clip instance for inequality.
    """
    __slots__ = ('id', 'url', 'type', 'user', 'title', 'duration', 'language', 'stream_id', 'created_at',
                 'view_count', 'description', 'is_viewable', 'published_at', 'thumbnail_url',
                 'muted_segments', 'is_muted_segments')

    if TYPE_CHECKING:
        id: str
        url: str
        type: str
        user: BaseUser
        title: str
        duration: str
        language: str
        stream_id: Optional[str]
        created_at: datetime
        view_count: str
        description: str
        is_viewable: bool
        published_at: datetime
        thumbnail_url: str
        muted_segments: Optional[List[VideoMutedSegments]]
        is_muted_segments: bool

    def __init__(self, data: ChannelTypes.Video) -> None:
        self._form_data(data=data)

    def __repr__(self) -> str:
        return f'<Video id={self.id} user={self.user!r} published_at={self.published_at}>'

    def __str__(self) -> str:
        return self.url

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Video):
            return self.id == other.id
        if isinstance(other, Clip):
            return self.id == other.video_id
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def _form_data(self, data: ChannelTypes.Video) -> None:
        self.id: str = data['id']
        self.url: str = data['url']
        self.user: BaseUser = BaseUser(data, prefix='user_')
        self.type: str = data['type']
        self.title: str = data['title']
        self.duration: str = data['duration']
        self.language: str = data['language']
        self.is_viewable = data['viewable'] == 'public'
        self.stream_id: Optional[str] = data['stream_id']
        self.view_count: str = data['view_count']
        self.created_at: datetime = convert_rfc3339(data['created_at'])
        self.description: str = data['description']
        self.published_at: datetime = convert_rfc3339(data['published_at'])
        self.thumbnail_url: str = data['thumbnail_url']
        self.muted_segments = None
        if data['muted_segments']:
            self.muted_segments = [VideoMutedSegments(data=s) for s in data['muted_segments']]
        self.is_muted_segments = self.muted_segments is not None


# ---------------------------------
#             + Clip +
# ---------------------------------
class Clip:
    """
    Represents a video clip on a channel.

    Attributes
    ----------
    id: str
        The unique identifier for the clip.
    url: str
        The URL of the clip.
    title: str
        The title of the clip.
    creator: BaseUser
        The user who created the clip.
    duration: float
        The duration (in seconds) of the clip.
    language: str
        The language of the clip.
    video_id: Optional[str]
        The ID of the associated video, if available.
    embed_url: str
        The URL for embedding the clip.
    created_at: datetime
        The date and time when the clip was created.
    view_count: int
        The number of views for the clip.
    vod_offset: Optional[int]
        The offset (in seconds) within the VOD if the clip is from a VOD, if available.
    broadcaster: BaseUser
        The broadcaster associated with the clip.
    category_id: Optional[str]
        The category (game) ID, if available.
    thumbnail_url: str
        The URL of the clip's thumbnail.

    Methods
    -------
    __str__() -> str
        Returns the URL of the clip as a string.
    __eq__(other: object) -> bool
        Compares the current Clip instance with another Clip instance for equality.
    __ne__(other: object) -> bool
        Compares the current Clip instance with another Clip instance for inequality.
    """
    __slots__ = ('id', 'url', 'title', 'creator', 'duration', 'language', 'video_id', 'embed_url',
                 'created_at', 'view_count', 'vod_offset', 'broadcaster', 'category_id', 'thumbnail_url')

    if TYPE_CHECKING:
        id: str
        url: str
        title: str
        creator: BaseUser
        duration: float
        language: str
        video_id: Optional[str]
        embed_url: str
        created_at: datetime
        view_count: int
        vod_offset: Optional[int]
        broadcaster: BaseUser
        category_id: Optional[str]
        thumbnail_url: str

    def __init__(self, data: ChannelTypes.Clip) -> None:
        self._form_data(data=data)

    def __repr__(self) -> str:
        return (
            f'<Clip id={self.id}  title={self.title} video_id={self.video_id} created_at={self.created_at}>'
        )

    def __str__(self) -> str:
        return self.url

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Clip):
            return self.id == other.id
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def _form_data(self, data: ChannelTypes.Clip) -> None:
        self.id: str = data['id']
        self.url: str = data['url']
        self.title: str = data['title']
        # ``creator_login`` is missing in the payload.
        data['creator_login'] = data['creator_name'].lower()
        self.creator: BaseUser = BaseUser(data, prefix='creator_')
        self.duration: float = data['duration']
        self.language: str = data['language']
        self.video_id: Optional[str] = data['video_id'] or None
        self.embed_url: str = data['embed_url']
        self.view_count: int = data['view_count']
        self.created_at: datetime = convert_rfc3339(data['created_at'])
        self.vod_offset: Optional[int] = data['vod_offset']
        # ``broadcaster_login`` is missing in the payload.
        data['broadcaster_login'] = data['broadcaster_name'].lower()
        self.broadcaster: BaseUser = BaseUser(data, prefix='broadcaster_')
        self.category_id: Optional[str] = data['game_id'] or None
        self.thumbnail_url: str = data['thumbnail_url']


# ------------------------------------
#            + Channel +
# ------------------------------------
class Channel:
    """
    Represents a Twitch channel.

    Attributes
    ----------
    id: str
        The unique identifier for the channel.
    url: str
        The URL of the channel.
    ccls: List[str]
        Content classification labels for the channel.
    tags: List[str]
        Tags associated with the channel.
    delay: int
        The delay (in seconds) of the channel's stream.
    title: str
        The title of the channel.
    category: Optional[Category]
        The category (game) associated with the channel, if available.
    language: str
        The language of the channel.
    broadcaster: BaseUser
        The broadcaster of the channel.
    is_branded_content : bool
        Indicates whether the channel features branded content.

    Methods
    -------
    __str__() -> str
        Returns the title of the channel as a string.
    __eq__(other: object) -> bool
        Compares the current Channel instance with another Channel or BaseUser instance for equality.
    __ne__(other: object) -> bool
        Compares the current Channel instance with another Channel or BaseUser instance for inequality.
    """
    __slots__ = ('id', 'url', 'ccls', 'tags', 'delay', 'title', 'category', 'language', 'broadcaster',
                 'is_branded_content')

    if TYPE_CHECKING:
        id: str
        url: str
        ccls: List[str]
        tags: List[str]
        delay: int
        title: str
        category: Optional[Category]
        language: str
        broadcaster: BaseUser
        is_branded_content: bool

    def __init__(self, data: ChannelTypes.Channel) -> None:
        self._form_data(data=data)

    def __repr__(self) -> str:
        return f'<Channel broadcaster={self.broadcaster!r} title={self.title} category={self.category!r}>'

    def __str__(self) -> str:
        return self.title

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Channel):
            return self.broadcaster.id == other.broadcaster.id
        if isinstance(other, BaseUser):
            return self.broadcaster.id == other.id
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def _form_data(self, data: ChannelTypes.Channel) -> None:
        self.id = data['broadcaster_id']
        self.ccls = data['content_classification_labels']
        self.tags = data['tags']
        self.delay = data['delay']
        self.title = data['title']
        self.language = data['broadcaster_language']
        self.category = Category(data=data) if data['game_id'] else None
        self.broadcaster = BaseUser(data, prefix='broadcaster_')
        self.url = f'https://www.twitch.tv/{self.broadcaster.name}'
        self.is_branded_content = data['is_branded_content']


# -----------------------------------
#              + User +
# -----------------------------------
class Follow(BaseUser):
    """
    Represents a follower relationship between users.

    Attributes
    ----------
    followed_at: datetime
        The date and time when the follow relationship was established.
    """
    __slots__ = ('followed_at',)

    if TYPE_CHECKING:
        followed_at: datetime

    def __init__(self, data: Union[ChannelTypes.Followed, ChannelTypes.Follower]) -> None:
        super().__init__(data, prefix=['broadcaster_', 'user_'])
        self._update_data(data=data)

    def __repr__(self) -> str:
        return f'<Follow name={self.name} followed_at={self.followed_at}>'

    def _update_data(self, data: Union[ChannelTypes.Followed, ChannelTypes.Follower]) -> None:
        super()._update_data(data=data)
        self.followed_at = convert_rfc3339(data['followed_at'])


class Editor(BaseUser):
    """
    Represents a user with editing privileges for a channel.

    Attributes
    ----------
    added_at: datetime
        The date and time when the user was granted editing privileges.
    """
    __slots__ = ('added_at',)

    if TYPE_CHECKING:
        added_at: datetime

    def __init__(self, data: ChannelTypes.Editor) -> None:
        super().__init__(data, prefix='user_')
        self._update_data(data=data)

    def __repr__(self) -> str:
        return f'<Editor name={self.name} added_at={self.added_at}>'

    def _update_data(self, data: ChannelTypes.Editor) -> None:
        super()._update_data(data=data)
        # ``user_login`` is missing in the payload.
        data['user_login'] = data['user_name'].lower()
        self.added_at = convert_rfc3339(timestamp=data['created_at'])


class BitsLeaderboard(BaseUser):
    """
    Represents a user's position on the bits' leaderboard.

    Attributes
    ----------
    rank: int
        The user's rank on the leaderboard.
    score: int
        The user's score on the leaderboard.

    Methods
    -------
    __int__() -> int
        the user's score.
    """
    __slots__ = ('rank', 'score')

    if TYPE_CHECKING:
        rank: int
        score: str

    def __init__(self, data: ChannelTypes.UserBitsLeaderboard) -> None:
        super().__init__(data, prefix='user_')
        self._update_data(data=data)

    def __repr__(self) -> str:
        return f'<BitsLeaderboard name{self.name} rank={self.rank} score={self.score}>'

    def __int__(self) -> int:
        return self.score

    def _update_data(self, data: ChannelTypes.UserBitsLeaderboard) -> None:
        super()._update_data(data=data)
        self.rank: int = data['rank']
        self.score: int = data['score']


class BannedUser(BaseUser):
    """
    Represents a banned user in a channel.

    Attributes
    ----------
    reason: str
        The reason for the ban.
    ends_at: Optional[datetime]
        The date and time when the ban ends, if not permanent.
    banned_at: datetime
        The date and time when the user was banned.
    banned_by: BaseUser
        The user who banned the other user.
    is_permanent: bool
        Indicates whether the ban is permanent.
    """
    __slots__ = ('reason', 'ends_at', 'banned_at', 'banned_by', 'is_permanent')

    if TYPE_CHECKING:
        reason: str
        ends_at: Optional[datetime]
        banned_at: datetime
        banned_by: BaseUser
        is_permanent: bool

    def __init__(self, data: Union[ChannelTypes.BannedUser, ChannelTypes.BannedUserEvent]) -> None:
        super().__init__(data, prefix='user_')
        self._form_data(data=data)

    def __repr__(self) -> str:
        return (
            f'<BannedUser name={self.name} banned_by={self.banned_by!r} is_permanent={self.is_permanent}>'
        )

    def _form_data(self, data: Union[ChannelTypes.BannedUser, ChannelTypes.BannedUserEvent]) -> None:
        super()._update_data(data=data)
        self.reason: str = data['reason']
        self.banned_by: BaseUser = BaseUser(data, prefix=['moderator_', 'moderator_user_'])
        _created_at = data.get('created_at')
        _banned_at = data.get('banned_at')
        self.banned_at = convert_rfc3339(_created_at or _banned_at)
        _expires_at = data.get('expires_at')
        _ends_at = data.get('ends_at')
        self.ends_at: Optional[datetime] = convert_rfc3339(_expires_at or _ends_at)
        self.is_permanent = self.ends_at is None


class Subscription:
    """
    Represents a user's subscription to a channel.

    Attributes
    ----------
    tier: int
        The subscription tier.
    user: BaseUser
        The user who subscribed.
    gifter: Optional[BaseUser]
        The user who gifted the subscription, if applicable.
    is_gift: bool
        Indicates whether the subscription is a gift.
    plan_name: Optional[str]
        The name of the subscription plan, if available.

    Methods
    -------
    __eq__(other: object) -> bool
        Compares the current Subscription instance with another Subscription
        or BaseUser instance for equality.
    __ne__(other: object) -> bool
        Compares the current Subscription instance with another Subscription
        or BaseUser instance for inequality.
    """
    if TYPE_CHECKING:
        tier: int
        user: BaseUser
        gifter: Optional[BaseUser]
        is_gift: bool
        plan_name: Optional[str]

    def __init__(self, data: ChannelTypes.Subscription) -> None:
        self._form_data(data=data)

    def __repr__(self) -> str:
        return f'<Subscription user={self.user!r} tier={self.tier} is_gift={self.is_gift}>'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Subscription):
            return self.user.id == other.user.id
        if isinstance(other, BaseUser):
            return self.user.id == other.id
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def _form_data(self, data: ChannelTypes.Subscription) -> None:
        self.tier = data['tier']
        self.user = BaseUser(data, prefix=['user_', 'broadcaster_'])
        self.gifter = BaseUser(data, prefix='gifter_') if data.get('gifter_id') else None
        self.is_gift = data['is_gift']
        self.plan_name = data.get('plan_name')


# -----------------------------------
#            + Schedule +
# -----------------------------------
class ScheduleSegment:
    """
    Represents a segment in a channel's schedule.

    Attributes
    ----------
    id: str
        The unique identifier of the schedule segment.
    title: str
        The title of the schedule segment.
    category: Optional[Category]
        The category associated with the schedule segment, if available.
    end_time: datetime
        The end time of the schedule segment.
    start_time: datetime
        The start time of the schedule segment.
    is_recurring: bool
        Indicates whether the schedule segment is recurring.
    frequency_day: str
        The day of the week on which the schedule segment recurs.
    canceled_until: Optional[datetime]
        The date and time until which the schedule segment is canceled, if canceled.

    Methods
    -------
    __str__() -> str
        Returns the title of the schedule segment as a string.
    __eq__(other: object) -> bool
        Compares the current ScheduleSegment instance with another for equality.
    __ne__(other: object) -> bool
        Compares the current ScheduleSegment instance with another for inequality.
    """
    __slots__ = ('id', 'title', 'category', 'end_time', 'start_time', 'is_recurring', 'frequency_day',
                 'canceled_until')
    if TYPE_CHECKING:
        id: str
        title: str
        category: Optional[Category]
        end_time: datetime
        start_time: datetime
        is_recurring: bool
        frequency_day: str
        canceled_until: Optional[datetime]

    def __init__(self, data: ChannelTypes.ScheduleSegment) -> None:
        self._form_data(data=data)

    def __repr__(self) -> str:
        return f'<ScheduleSegment id={self.id} start_time={self.start_time} end_time={self.end_time}>'

    def __str__(self) -> str:
        return self.title

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ScheduleSegment):
            return self.id == other.id
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def _form_data(self, data: ChannelTypes.ScheduleSegment) -> None:
        self.id = data['id']
        self.title = data['title']
        self.category = Category(data=data['category']) if data['category'] else None
        self.end_time = convert_rfc3339(data['end_time'])
        self.start_time = convert_rfc3339(data['start_time'])
        self.frequency_day = self.start_time.strftime("%A")
        self.is_recurring = data['is_recurring']
        self.canceled_until = convert_rfc3339(data['canceled_until'])


class ScheduleVacation:
    """
    Represents a vacation in a channel's schedule.

    Attributes
    ----------
    start_time: datetime
        The start time of the vacation.
    end_time: datetime
        The end time of the vacation.
    """
    __slots__ = ('start_time', 'end_time')

    if TYPE_CHECKING:
        start_time: datetime
        end_time: datetime

    def __init__(self, data: ChannelTypes.ScheduleVacation) -> None:
        self._form_data(data=data)

    def __repr__(self) -> str:
        return f'<ScheduleVacation start_time={self.start_time} end_time={self.end_time}>'

    def _form_data(self, data: ChannelTypes.ScheduleVacation) -> None:
        self.start_time = convert_rfc3339(data['start_time'])
        self.end_time = convert_rfc3339(data['end_time'])


class Schedule:
    """
    Represents a channel's schedule.

    Attributes
    ----------
    segments: List[ScheduleSegment]
        A list of schedule segments.
    vacation: Optional[ScheduleVacation]
        Information about any ongoing vacation, if applicable.
    is_in_vacation: bool
        Indicates whether the channel is currently in vacation.

    Methods
    -------
    __bool__() -> bool
        Checks if the channel is currently on vacation.
    """
    __slots__ = ('segments', 'vacation', 'is_in_vacation')

    if TYPE_CHECKING:
        segments: List[ScheduleSegment]
        vacation: Optional[ScheduleVacation]
        is_in_vacation: bool

    def __init__(self, data: ChannelTypes.Schedule) -> None:
        self._form_data(data=data)

    def __repr__(self) -> str:
        return f'<Schedule is_in_vacation={self.is_in_vacation}>'

    def __bool__(self) -> bool:
        return self.is_in_vacation

    def _form_data(self, data: ChannelTypes.Schedule):
        self.segments = [ScheduleSegment(data=s) for s in data['segments']]
        self.vacation = ScheduleVacation(data=data['vacation']) if data['vacation'] else None
        self.is_in_vacation = self.vacation is not None


# ----------------------------------
#           + Charity +
# ----------------------------------
class CharityAmount:
    """
    Represents a charitable donation amount.

    Attributes
    ----------
    value: float
        The value of the donation amount.
    currency: str
        The currency in which the donation is made.

    Methods
    -------
    __float__() -> float
        Converts the donation amount to a float.
    __int__() -> int
        Converts the donation amount to an integer.
    """
    __slots__ = ('value', 'currency')

    if TYPE_CHECKING:
        value: float
        currency: str

    def __init__(self, data: ChannelTypes.CharityAmount) -> None:
        self._form_data(data=data)

    def __repr__(self) -> str:
        return f'<CharityAmount value={self.value} currency={self.currency}>'

    def __float__(self) -> float:
        return self.value

    def __int__(self) -> int:
        return int(self.value)

    def _form_data(self, data: ChannelTypes.CharityAmount) -> None:
        self.value: float = (data['value'] / 10 ** data['decimal_places'])
        self.currency: str = data['currency']


class CharityDonation(BaseUser):
    """
    Represents a charitable donation made by a user.

    Attributes
    ----------
    donation_id: str
        The unique identifier of the donation.
    campaign_id: str
        The campaign identifier associated with the donation.
    amount: CharityAmount
        The amount of the donation.

    Methods
    -------
    __eq__(other: object) -> bool
        Compares the current CharityDonation instance with another for equality.
    __ne__(other: object) -> bool
        Compares the current CharityDonation instance with another for inequality.
    """
    __slots__ = ('donation_id', 'campaign_id', 'amount')

    if TYPE_CHECKING:
        id: str
        campaign_id: str
        amount: CharityAmount

    def __init__(self, data: Union[ChannelTypes.CharityDonation, ChannelTypes.CharityDonationEvent]) -> None:
        super().__init__(data=data, prefix='user_')
        self._update_data(data=data)

    def __repr__(self) -> str:
        return f'<CharityDonation id={self.id} name={self.name} amount={self.amount!r}>'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, CharityDonation):
            return self.campaign_id == other.campaign_id
        if isinstance(other, Charity):
            return self.campaign_id == other.id
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def _update_data(self, data: Union[ChannelTypes.CharityDonation,
                                       ChannelTypes.CharityDonationEvent]) -> None:
        super()._update_data(data=data)
        self.donation_id: str = data['id']
        self.campaign_id: str = data['campaign_id']
        self.amount: CharityAmount = CharityAmount(data=data['amount'])


class Charity:
    """
    Represents a charitable organization or campaign.

    Attributes
    ----------
    id: str
        The unique identifier of the charity.
    name: str
        The name of the charity.
    logo: str
        The URL of the charity's logo.
    website: str
        The URL of the charity's website.
    description: str
        A description of the charity.
    target_amount : Optional[CharityAmount]
        The target donation amount for the charity, if defined.
    current_amount: Optional[CharityAmount]
        The current donation amount received by the charity, if available.

    Methods
    -------
    __int__() -> int
        Converts the current donation amount to an integer.
    __eq__(other: object) -> bool
        Compares the current Charity instance with another for equality.
    __ne__(other: object) -> bool
        Compares the current Charity instance with another for inequality.
    """
    __slots__ = ('id', 'name', 'logo', 'website', 'description', 'target_amount', 'current_amount')

    if TYPE_CHECKING:
        id: str
        name: str
        logo: str
        website: str
        description: str
        target_amount: Optional[CharityAmount]
        current_amount: Optional[CharityAmount]

    def __init__(self, data: Union[ChannelTypes.Charity, ChannelTypes.CharityDonation]) -> None:
        self._form_data(data=data)

    def __repr__(self) -> str:
        return f'<Charity id={self.id} name={self.name} target_amount={self.target_amount!r}>'

    def __int__(self) -> int:
        return self.current_amount or 0

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Charity):
            return self.id == other.id
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def _form_data(self, data: Union[ChannelTypes.Charity, ChannelTypes.CharityDonation]) -> None:
        self.id: str = data.get('campaign_id', data['id'])
        self.name: str = data['charity_name']
        self.logo: str = data['charity_logo']
        self.website: str = data.get('charity_website')
        self.description: str = data.get('charity_description')
        # This is None if the broadcaster has not defined a fundraising goal,
        # or it is None if it's from EventSub.
        _target_amount: Optional[ChannelTypes.CharityAmount] = data.get('target_amount')
        self.target_amount = CharityAmount(data=_target_amount) if _target_amount else None
        # This is None if it's from Event.
        _current_amount: Optional[ChannelTypes.CharityAmount] = data.get('current_amount')
        self.current_amount = CharityAmount(data=_current_amount) if _current_amount else None


# -------------------------------
#      + Channel Followers +
# -------------------------------
class ChannelFollowers:
    """
    Represents a channel's followers.
    """

    __slots__ = ('__state', '_b_id')

    def __init__(self, state: ConnectionState, broadcaster_id: str) -> None:
        self._b_id: str = broadcaster_id
        self.__state: ConnectionState = state

    async def get_total(self) -> int:
        """
        Get the total number of followers for the channel.

        Returns
        -------
        int
            The total number of followers for the channel.
        """
        data = await self.__state.http.get_channel_total_followers(broadcaster_id=self._b_id)
        return data

    async def fetch_all(self, limit: int = 4) -> AsyncGenerator[List[Follow]]:
        """
        Fetch a list of channel followers.

        ???+ Danger
            Only channel moderators or the broadcaster himself can access the list of followers.

            this will result an empty list.

        ???+ Warning
            This method uses [pagination](https://dev.twitch.tv/docs/api/guide/#pagination).
            Set the limit to -1 to retrieve all data, but be cautious of potential performance
            and rate limit impacts.

        | Scopes                     | Description             |
        | -------------------------- | ------------------------|
        | `moderator:read:followers` | Get Channel Followers.  |

        Parameters
        ----------
        limit: int
            The maximum number of followers to fetch.

        Raises
        ------
        NotFound
            * Unable to find the requested user.
            * The user is not following.
        Unauthorized
            * The user access token is missing the moderator:read:followers scope.
            * user is not a moderator for the broadcaster.

        Yields
        ------
        List[Follow]
            A list of Follow objects representing channel followers.
        """
        async for users in self.__state.http.fetch_channel_followers(limit=limit, broadcaster_id=self._b_id):
            yield [Follow(data=user) for user in users]

    async def check(self, user: Union[str, BaseUser]):
        """
        Check if a user is following the channel.

        | Scopes                     | Description             |
        | -------------------------- | ------------------------|
        | `moderator:read:followers` | Get Channel Followers.  |

        Parameters
        ----------
        user: Union[str, BaseUser]
            The user or user name to check for following.

        Raises
        ------
        NotFound
            If the user is not following the channel.
        Unauthorized
            * The user access token is missing the moderator:read:followers scope.
            * user is not a moderator for the broadcaster.

        Returns
        -------
        Follow
            A Follow object representing the user's follow status.
        """
        user = await self.__state.get_user(user)
        async for users in self.__state.http.fetch_channel_followers(limit=1,
                                                                     broadcaster_id=self._b_id,
                                                                     user_id=user.id):
            if len(users) == 1:
                return Follow(data=users[0])
            raise NotFound('The user is not following.')


# ----------------------------------
#           + Extension +
# ----------------------------------
class BaseExtension:
    """
    Represents a base extension.

    Attributes
    ----------
    id: Optional[str]
        The unique identifier of the extension.
    name: Optional[str]
        The name of the extension.
    version: Optional[str]
        The version of the extension.

    Methods
    -------
    __str__() -> str
        Returns the name of the extension or 'Empty' if the name is not available.
    __eq__(other) -> bool
        Compares the current extension with another for equality.
    __ne__(other: object) -> bool
        Compares the current extension with another for inequality.
    """
    __slots__ = ('id', 'name', 'version')

    if TYPE_CHECKING:
        id: Optional[str]
        name: Optional[str]
        version: Optional[str]

    def __init__(self, data: Union[ChannelTypes.Extension, ChannelTypes.ActiveExtension]) -> None:
        self._update_data(data=data)

    def __repr__(self) -> str:
        return f'<BaseExtension id={self.id} name={self.name} version={self.version}>'

    def __str__(self) -> str:
        return self.name or 'Empty'

    def __eq__(self, other) -> bool:
        if isinstance(other, ActiveExtension):
            if other.is_active:
                return self.id == other.id
            return False
        if isinstance(other, BaseExtension):
            return self.id == other.id
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def _update_data(self, data: Union[ChannelTypes.Extension, ChannelTypes.ActiveExtension]) -> None:
        self.id = data.get('id')
        self.name = data.get('name')
        self.version = data.get('version')


class ActiveExtension(BaseExtension):
    """
    Represents an active extension.

    Attributes
    ----------
    is_active: bool
        Indicates whether the extension is active.
    slot_number : int
        The slot number of the extension.
    x: Optional[str]
        The X-coordinate of the extension.
    y: Optional[str]
        The Y-coordinate of the extension.

    Methods
    -------
    __bool__() -> bool
        Returns True if the extension is active, False otherwise.
    __int__() -> int
        Returns the slot number of the extension as an integer.
    """
    __slots__ = ('x', 'y', 'is_active', 'slot_number')

    if TYPE_CHECKING:
        x: Optional[str]
        y: Optional[str]
        is_active: bool
        slot_number: int

    def __init__(self, data: ChannelTypes.ActiveExtension) -> None:
        super().__init__(data=data)
        self._update_data(data=data)

    def __repr__(self) -> str:
        return f'<ActiveExtension id={self.id} name={self.name} is_active={self.is_active}>'

    def __bool__(self) -> bool:
        return self.is_active

    def __int__(self) -> int:
        return self.slot_number

    def _update_data(self, data: ChannelTypes.ActiveExtension) -> None:
        super()._update_data(data=data)
        self.x = data.get('x')
        self.y = data.get('y')
        self.is_active = data['active']
        self.slot_number = data['slot_number']


class Extension(BaseExtension):
    """
    Represents an extension.

    Attributes
    ----------
    type: List[str]
        The types of the extension.
    can_activate: bool
        Indicates whether the extension can be activated.

    Methods
    -------
    __bool__() -> bool
        Returns True if the extension can be activated, False otherwise.
    """
    __slots__ = ('type', 'can_activate')

    if TYPE_CHECKING:
        type: List[str]
        can_activate: bool

    def __init__(self, data: ChannelTypes.Extension) -> None:
        super().__init__(data=data)
        self._update_data(data=data)

    def __bool__(self) -> bool:
        return self.can_activate

    def __repr__(self) -> str:
        return f'<Extension id={self.id} name={self.name} can_activate={self.can_activate}>'

    def _update_data(self, data: ChannelTypes.Extension) -> None:
        super()._update_data(data=data)
        self.type = data['type']
        self.can_activate = data['can_activate']


class Extensions:
    """
    Represents a collection of extensions.

    Attributes
    ----------
    panel: List[ActiveExtension]
        List of active extensions in the panel.
    overlay: List[ActiveExtension]
        List of active overlay extensions.
    component: List[ActiveExtension]
        List of active component extensions.
    """
    __slots__ = ('panel', 'overlay', 'component')

    if TYPE_CHECKING:
        panel: List[ActiveExtension]
        overlay: List[ActiveExtension]
        component: List[ActiveExtension]

    def __init__(self, data: ChannelTypes.Extensions) -> None:
        self._form_data(data=data)

    def __repr__(self) -> str:
        return '<Extensions>'

    def _form_data(self, data: ChannelTypes.Extensions) -> None:
        self.panel: List[ActiveExtension] = [ActiveExtension(data=ex) for ex in data['panel']]
        self.overlay: List[ActiveExtension] = [ActiveExtension(data=ex) for ex in data['overlay']]
        self.component: List[ActiveExtension] = [ActiveExtension(data=ex) for ex in data['component']]


class ChannelExtensions:
    """
    Represents extensions associated with a specific channel.
    """
    __slots__ = ('_b_id', '__state')

    def __init__(self, state: ConnectionState, broadcaster_id: str):
        self._b_id: str = broadcaster_id
        self.__state: ConnectionState = state

    async def get_active(self) -> Extensions:
        """
        Get a list of active extensions that the broadcaster has installed for each configuration.

        | Scopes                                         | Description                    |
        | ---------------------------------------------- | -------------------------------|
        | `user:read:broadcast` or `user:edit:broadcast` | Get client active extensions.  |

        Raises
        ------
        Unauthorized
            * The user access token is missing the user:read:broadcast or user:edit:broadcast scope.

        Returns
        -------
        Extensions
            An object representing the active extensions for the channel.
        """
        data = await self.__state.http.get_user_active_extensions(user_id=self._b_id)
        return Extensions(data=data)


# --------------------------------
#           + Schedule +
# --------------------------------
class ChannelSchedule:
    """
    Represents a channel's stream schedule.
    """
    __slots__ = ('_b_id', '__state')

    def __init__(self, state: ConnectionState, broadcaster_id: str):
        self._b_id: str = broadcaster_id
        self.__state: ConnectionState = state

    async def fetch_all(self, start_time: datetime = MISSING, limit: int = 4) -> AsyncGenerator[Schedule]:
        """
        Fetch all stream schedule segments for the channel.

        ???+ Warning
            This method uses [pagination](https://dev.twitch.tv/docs/api/guide/#pagination).
            Set the limit to -1 to retrieve all data, but be cautious of potential performance
            and rate limit impacts.

        Raises
        ------
        NotFound
            * The broadcaster has not created a streaming schedule.

        Parameters
        ----------
        start_time: datetime
            The start time to filter segments. Default is None.
        limit: int
            The maximum number of segments to fetch. Default is 4.

        Yields
        -------
        Schedule
            A Schedule object representing a stream schedule segment.
        """
        async for schedule in self.__state.http.fetch_channel_stream_schedule(
                limit=limit, broadcaster_id=self._b_id, start_time=start_time):
            yield Schedule(data=schedule)

    async def get_segments(self, segments: List[ScheduleSegment]) -> Schedule:
        """
        Get stream schedule segments.

        Parameters
        ----------
        segments: List[ScheduleSegment]
            A list of ScheduleSegment objects representing the segments to fetch.

        Raises
        ------
        NotFound
            * The broadcaster has not created a streaming schedule.

        Returns
        -------
        Schedule
            A Schedule object representing the fetched stream schedule segment.

        """
        segment_ids = [segment.id for segment in segments]
        async for schedule in self.__state.http.fetch_channel_stream_schedule(limit=1,
                                                                              broadcaster_id=self._b_id,
                                                                              segment_ids=segment_ids):
            return Schedule(data=schedule)


class UserChannel:
    """
    Represents a user's channel.
    """

    __slots__ = ('_b_id', '_state', '__weakref__')

    def __init__(self, state: ConnectionState, broadcaster_id: str) -> None:
        """
        Initialize a UserChannel instance.

        Parameters
        ----------
        state : ConnectionState
            The state representing the connection to a service or platform.
        broadcaster_id : str
            The ID of the broadcaster (channel) being accessed.
        """
        self._b_id: str = broadcaster_id
        self._state: ConnectionState = state

    @property
    def chat(self) -> ChannelChat:
        """
        Get an instance of the ChannelChat class for managing chat-related actions.

        Returns
        -------
        ChannelChat
            An instance of the ChannelChat class.
        """
        return ChannelChat(state=self._state, broadcaster_id=self._b_id, moderator_id=self._state.user.id)

    @property
    def stream(self) -> ChannelStream:
        """
        Get an instance of the ChannelStream class for managing stream-related actions.

        Returns
        -------
        ChannelStream
            An instance of the ChannelStream class.
        """
        return ChannelStream(state=self._state, broadcaster_id=self._b_id, moderator_id=self._state.user.id)

    @property
    def extensions(self) -> ChannelExtensions:
        """
        Get an instance of the ChannelExtensions class for managing channel extensions.

        Returns
        -------
        ChannelExtensions
            An instance of the ChannelExtensions class.
        """
        return ChannelExtensions(state=self._state, broadcaster_id=self._b_id)

    @property
    def schedule(self) -> ChannelSchedule:
        """
        Get an instance of the ChannelSchedule class for managing the channel's streaming schedule.

        Returns
        -------
        ChannelSchedule
            An instance of the ChannelSchedule class.
        """
        return ChannelSchedule(state=self._state, broadcaster_id=self._b_id)

    @property
    def followers(self) -> ChannelFollowers:
        """
        Get an instance of the ChannelFollowers class for managing channel followers and their actions.

        Returns
        -------
        ChannelFollowers
            An instance of the ChannelFollowers class.
        """
        return ChannelFollowers(state=self._state, broadcaster_id=self._b_id)

    async def get_info(self) -> Channel:
        """
        Get information about the channel.

        Returns
        -------
        Channel
            Information about the channel.
        """
        data = await self._state.http.get_channels(broadcaster_ids=[self._b_id])
        return Channel(data=data[0])

    async def ban(self, user: Union[str, BaseUser], duration: int = MISSING, reason: str = MISSING) -> None:
        """
        Ban a user from the channel's chat.

        | Scopes                          | Description   |
        | ------------------------------- | ------------- |
        | `moderator:manage:banned_users` | Ban User.     |

        Parameters
        ----------
        user: Union[str, BaseUser]
            The user or user name to be banned.
        duration: int
            The duration of the ban in seconds. For timeout, specify the timeout period.

            * The minimum timeout is 1 second and the maximum is 1,209,600 seconds (2 weeks).
        reason: str
            The reason for the ban.

        Raises
        ------
        NotFound
            * Unable to find the requested user.
        ValueError
            * Duration must be between 1 second and 1,209,600 seconds (2 weeks)
            * Reason is limited to a maximum of 500 characters.
        BadRequest
            * user may not be banned.
            * The user may not be put in a timeout.
            * The user is already banned.
        Unauthorized
            * The user access token must include the moderator:manage:banned_users scope.
        Forbidden
            * The user in moderator_id is not one of the broadcaster's moderators.
        Conflict
            * You may not update the user's ban state while someone else is updating the state.
        RateLimit
            * The app has exceeded the number of requests it may make per minute for this broadcaster.
        """
        user = await self._state.get_user(user)
        await self._state.http.ban_user(broadcaster_id=self._b_id, moderator_id=self._state.user.id,
                                        user_id=user.id, duration=duration, reason=reason)

    async def unban(self, user: Union[str, BaseUser]) -> None:
        """
        Unban a previously banned user from the channel's chat.

        | Scopes                          | Description   |
        | ------------------------------- | ------------- |
        | `moderator:manage:banned_users` | UnBan User.   |

        Parameters
        ----------
        user: Union[str, BaseUser]
            The user or user name to be unbanned.

        Raises
        ------
        NotFound
            * Unable to find the requested user.
        BadRequest
            * user may not be banned.
            * The user may not be put in a timeout.
            * The user is already banned.
        Unauthorized
            * The user access token must include the moderator:manage:banned_users scope.
        Forbidden
            * The user in moderator_id is not one of the broadcaster's moderators.
        Conflict
            * You may not update the user's ban state while someone else is updating the state.
        RateLimit
            * The app has exceeded the number of requests it may make per minute for this broadcaster.
        """
        user = await self._state.get_user(user)
        await self._state.http.unban_user(broadcaster_id=self._b_id, moderator_id=self._state.user.id,
                                          user_id=user.id)

    async def fetch_videos(self, language: str = MISSING,
                           period: Literal['all', 'day', 'month', 'week'] = 'all',
                           videos_type: Literal['all', 'archive', 'highlight', 'upload'] = 'all',
                           sort: Literal['time', 'trending', 'views'] = 'time',
                           limit: int = 4) -> AsyncGenerator[List[Video]]:
        """
        Fetch a list of videos from the channel.

        ???+ Warning
            This method uses [pagination](https://dev.twitch.tv/docs/api/guide/#pagination).
            Set the limit to -1 to retrieve all data, but be cautious of potential performance
            and rate limit impacts.

        Parameters
        ----------
        language: str
            The language of the videos.
        period: Literal['all', 'day', 'month', 'week']
            The time period to filter the videos.
        videos_type: Literal['all', 'archive', 'highlight', 'upload']
            The type of videos to filter
        sort: Literal['time', 'trending', 'views']
            The sorting order of the videos
        limit: int
            The maximum number of videos to fetch.

        Yields
        ------
        AsyncGenerator[List[Video]]
            lists of Video objects.
        """
        async for videos in self._state.http.fetch_videos(limit=limit, user_id=self._b_id, language=language,
                                                          period=period, sort=sort, videos_type=videos_type):
            yield [Video(data=video) for video in videos]

    async def fetch_clips(self, started_at: datetime = MISSING, ended_at: datetime = MISSING,
                          limit: int = 4) -> AsyncGenerator[List[Clip]]:
        """
        Fetch a list of clips from the channel.

        ???+ Warning
            This method uses [pagination](https://dev.twitch.tv/docs/api/guide/#pagination).
            Set the limit to -1 to retrieve all data, but be cautious of potential performance
            and rate limit impacts.

        Parameters
        ----------
        started_at : datetime
            The start time for filtering clips.
        ended_at : datetime
            The end time for filtering clips.
        limit : int
            The maximum number of clips to fetch.

        Yields
        ------
        AsyncGenerator[List[Clip]]
            lists of Clip objects.
        """
        async for clips in self._state.http.fetch_clips(limit=limit, broadcaster_id=self._b_id,
                                                        started_at=started_at, ended_at=ended_at):
            yield [Clip(data=clip) for clip in clips]
