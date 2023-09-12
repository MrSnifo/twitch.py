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
from .errors import NotFound
from .user import BaseUser

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Optional, List, Union
    from .types import stream as StreamTypes
    from .state import ConnectionState
    from datetime import datetime

__all__ = ('ChannelStream', 'Stream', 'StreamMarker', 'Category')


class Category:
    """
    Represents a category for a stream or game.

    Attributes
    ----------
    id: str
        The unique ID of the category.
    name: str
        The name of the category.

    Methods
    -------
    __str__() -> str
        Returns the name of the Category.
    __eq__(other: object) -> bool
        Checks if two Category instances are equal based on their IDs.
    __ne__(other: object) -> bool
    """
    __slots__ = ('id', 'name', '__weakref__')

    if TYPE_CHECKING:
        id: str
        name: str

    def __init__(self, data: Union[StreamTypes.Category, StreamTypes.SpecificCategory,
                                   StreamTypes.SpecificGame]) -> None:
        self._form_data(data=data)

    def __repr__(self) -> str:
        return f'<Category id={self.id} name={self.name}>'

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Category):
            return self.id == other.id
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def _form_data(self, data: Union[StreamTypes.Category, StreamTypes.SpecificCategory,
                                     StreamTypes.SpecificGame]) -> None:
        _id_keys = ('id', 'game_id', 'category_id')
        _name_keys = ('name', 'game_name', 'category_name')
        self.id = next((data.get(key) for key in _id_keys if data.get(key)), 'unknown')
        self.name = next((data.get(key) for key in _name_keys if data.get(key)), 'unknown')


class Stream:
    """
    Represents a Twitch stream.

    Attributes
    ----------
    id: str
        The unique ID of the stream.
    url: str
        The URL of the stream.
    tags: List[str]
        The tags associated with the stream.
    type: str
        The type of the stream.
    title: str
        The title of the stream.
    category: Optional[Category]
        The category associated with the stream.
    language: str
        The language of the stream.
    is_mature: bool
        Indicates if the stream is marked as mature.
    started_at: datetime
        The date and time when the stream started.
    broadcaster: BaseUser
        The user who is broadcasting the stream.
    viewer_count: int
        The current viewer count of the stream.
    thumbnail_url: str
        The URL of the stream's thumbnail.

    Methods
    -------
    __str__() -> str
        Returns the title of the Stream.
    __int__() -> int
        Returns the viewer count as an integer.
    __eq__(other: object) -> bool
        Checks if two Stream instances are equal based on their IDs or broadcaster's ID.
    __ne__(other: object) -> bool
        Checks if two Stream instances are not equal.
    """
    __slots__ = ('id', 'url', 'tags', 'type', 'title', 'category', 'language', 'is_mature', 'started_at',
                 'broadcaster', 'viewer_count', 'thumbnail_url')

    if TYPE_CHECKING:
        id: str
        url: str
        tags: List[str]
        type: str
        title: str
        category: Optional[Category]
        language: str
        is_mature: bool
        started_at: datetime
        broadcaster: BaseUser
        viewer_count: int
        thumbnail_url: str

    def __init__(self, data: StreamTypes.Stream) -> None:
        self._form_data(data=data)

    def __repr__(self) -> str:
        return f'<Stream id={self.id} broadcaster={self.broadcaster!r} viewer_count={self.viewer_count}>'

    def __str__(self) -> str:
        return self.title

    def __int__(self) -> int:
        return self.viewer_count

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Stream):
            return self.id == other.id
        if isinstance(other, BaseUser):
            return self.broadcaster.id == other.id
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def _form_data(self, data: StreamTypes.Stream) -> None:
        self.id = data['id']
        self.type = data['type'] or 'unknown'
        self.tags = data['tags']
        self.title = data['title']
        self.language = data['language']
        self.category = Category(data=data) if data['game_id'] else None
        self.is_mature = data['is_mature']
        self.started_at = convert_rfc3339(data['started_at'])
        self.broadcaster = BaseUser(data, prefix='user_')
        self.url = f'https://www.twitch.tv/{self.broadcaster.name}'
        self.viewer_count = data['viewer_count']
        self.thumbnail_url = data['thumbnail_url']


class StreamMarker:
    """
    Represents a marker set during a Twitch stream.

    Attributes
    ----------
    id: str
        The unique ID of the stream marker.
    url: Optional[str]
        The URL associated with the stream marker (optional).
    created_at: datetime
        The date and time when the marker was created.
    description: str
        The description of the stream marker.
    position_seconds: int
        The position in seconds where the marker was set.

    Methods
    -------
    __eq__(other: object) -> bool
        Checks if two StreamMarker instances are equal based on their IDs.
    __ne__(other: object) -> bool
        Checks if two StreamMarker instances are not equal.
    """
    if TYPE_CHECKING:
        id: str
        url: Optional[str]
        created_at: datetime
        description: str
        position_seconds: int

    def __init__(self, data: StreamTypes.StreamMarker) -> None:
        self._form_data(data=data)

    def __repr__(self) -> str:
        return (
            f'<StreamMarker id={self.id} description={self.description} '
            f'position_seconds={self.position_seconds}>'
        )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, StreamMarker):
            return self.id == other.id
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def _form_data(self, data: StreamTypes.StreamMarker) -> None:
        self.id = data['id']
        self.created_at = convert_rfc3339(data['created_at'])
        self.description = data['description']
        self.position_seconds = data['position_seconds']
        # `url` is missing when creating a Stream Marker.
        self.url = data.get('url')


class ChannelStream:
    """
    Represents a channel's stream-related functionality.
    """
    __slots__ = ('_b_id', '_m_id', '__state')

    def __init__(self, state: ConnectionState, broadcaster_id: str, moderator_id: str) -> None:
        self._b_id: str = broadcaster_id
        self._m_id: str = moderator_id
        self.__state: ConnectionState = state

    async def get_info(self) -> Stream:
        """
        Get information about the channel's current stream.

        Raises
        ------
        NotFound
            * Stream is not currently active.

        Returns
        -------
        Stream
            Information about the current stream.
        """
        async for streams in self.__state.http.fetch_streams(limit=1, user_ids=[self._b_id]):
            if streams:
                return Stream(data=streams[0])
            raise NotFound("The stream you're looking for is not currently active.")

    async def create_marker(self, description: str = MISSING) -> StreamMarker:
        """
        Create a marker in the channel's current stream.

        ???+ Danger
            You may not add markers:

            * If the stream is not live.
            * If the stream has not enabled video on demand (VOD).
            * If the stream is a premiere.
            * If the stream is a rerun of a past broadcast, including past premieres.

        | Scopes                     | Description             |
        | -------------------------- | ----------------------- |
        | `channel:manage:broadcast` | Create Stream Marker.   |

        Parameters
        ----------
        description: str
            The description for the marker.

        Raises
        ------
        ValueError
            * The maximum length of the description is 140 characters.
        Unauthorized
            * The user access token must include the user:manage:broadcast scope.
        Forbidden
            * The user in the access token must own the video.
            * The user must be one of the broadcaster's editors.
        NotFound
            * The user is not streaming live.
            * The user hasn't enabled video on demand (VOD).

        Returns
        -------
        StreamMarker
            Information about the created stream marker.
        """
        data = await self.__state.http.create_stream_marker(user_id=self._b_id, description=description)
        return StreamMarker(data=data)

    async def send_shoutout(self, broadcaster: Union[str, BaseUser, Stream]) -> None:
        """
        Send a shoutout to another broadcaster during the stream.

        ???+ Warning
            The broadcaster may send a Shoutout once every 2 minutes.
            They may send the same broadcaster a Shoutout once every 60 minutes.

        | Scopes                       | Description        |
        | ---------------------------- | ------------------ |
        | `moderator:manage:shoutouts` | Send a Shoutout.   |

        Raises
        ------
        NotFound
            * Unable to find the requested user.
        BadRequest
            * The broadcaster may not give themselves a Shoutout.
            * The broadcaster is not streaming live or does not have one or more viewers.
        Unauthorized
            * The user access token must include the moderator:manage:shoutouts scope.
        Forbidden
            * The user in moderator_id is not one of the broadcaster's moderators.
            * The broadcaster may not send the specified broadcaster a Shoutout.
        RateLimit
            * Exceeded the number of Shoutouts they may send within a given window.
            * Exceeded the number of Shoutouts they may send the same broadcaster within a given window.

        Parameters
        ----------
        broadcaster: Union[str, BaseUser, Stream]
            The broadcaster to send the shoutout to.
        """
        if isinstance(broadcaster, Stream):
            broadcaster = broadcaster.broadcaster
        broadcaster = await self.__state.get_user(user=broadcaster)
        await self.__state.http.send_shoutout(broadcaster_id=self._b_id, moderator_id=self._m_id,
                                              to_broadcaster_id=broadcaster.id)

    async def create_clip(self, has_delay: bool = False) -> str:
        """
        Create a clip from the channel's current stream.

        | Scopes       | Description    |
        | ------------ | -------------- |
        | `clips:edit` | Create Clip.   |

        Parameters
        ----------
        has_delay: optional
            Indicates whether the clip should include stream delay. Defaults to False.

        Raises
        ------
        Unauthorized
            * The user access token must include the clips:edit scope.
        Forbidden
            * Only followers and/or subscriber can capture clips.
            * The specified broadcaster has not enabled clips on their channel.
        NotFound
            * Stream is not currently active.

        Returns
        -------
        str
            The edit URL of the created clip.
        """
        data = await self.__state.http.create_clip(broadcaster_id=self._b_id, has_delay=has_delay)
        return data['edit_url']
