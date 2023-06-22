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

from datetime import datetime
from .utils import parse_rfc3339_timestamp, empty_to_none, cache_decorator
from .types.user import UserType, UserImages, Tier, Types
from .channel import Channel
from .stream import Stream

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .types import channel as ch
    from .types import stream as stm
    from typing import Optional
    from .http import HTTPClient


class Images:
    """
    Represents images associated with a Twitch user.

    :param user: The user's image data.
    """
    def __init__(self, *, user: UserImages) -> None:
        self.profile = user['profile_image_url']
        self.offline = user['offline_image_url']

    def __repr__(self) -> str:
        return f'<Images profile={self.profile} offline={self.profile}>'


class Broadcaster:
    """
    Represents a Twitch broadcaster.

    :param http: The HTTPClient instance for making HTTP requests.
    :param user: The user data representing the broadcaster.
    """
    def __init__(self, *, http: HTTPClient, user: UserType):
        self.__http = http
        self.id: str = user['id']
        self.name: str = user['login']
        self.display_name: str = user['display_name']
        self.email: Optional[str] = empty_to_none(text=user['email'])
        self.images: Images = Images(user=user)
        # Set the broadcaster tier.
        self.tier: Tier = user['broadcaster_type'] if user['broadcaster_type'] else 'regular'
        # Set the user type.
        self.type: Types = user['type'] if user['type'] else 'regular'
        self.joined_at: datetime = parse_rfc3339_timestamp(user['created_at'])
        # Updating the channel description from the user.
        self.bio = empty_to_none(text=user['description'])

    @cache_decorator(expiry_seconds=20)
    async def get_channel(self) -> Channel:
        """
        Retrieve the channel associated with the broadcaster.

        :return: An instance of the Channel class representing the channel.
        :rtype: Channel
        """
        data: ch.Channel = await self.__http.get_channel(broadcaster_id=self.id)
        _channel = Channel(channel=data)
        _channel.description = self.bio
        return _channel

    @cache_decorator(expiry_seconds=12)
    async def get_stream(self) -> Optional[Stream]:
        """
        Retrieve the stream of the broadcaster if currently live.

        :return: An instance of the Stream class representing the stream if live, otherwise None.
        :rtype: Optional[Stream]
        """
        data: Optional[stm.Stream] = await self.__http.get_stream(user_id=self.id)
        if data:
            _stream = Stream(stream=data)
            return _stream
        return None
