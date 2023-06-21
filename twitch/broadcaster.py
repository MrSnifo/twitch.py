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

# Core
from .types.user import (UserPayload, UserPayloadWithEmail)
from .utils import empty_to_none, parse_rfc3339_timestamp
from .stream import Stream

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Union, Optional
    from .http import HTTPClient
    from datetime import datetime


class Broadcaster:
    """
    Represents a Twitch broadcaster.
    """
    __slots__ = ('_data', '_http', 'id', 'name', 'display_name', '_type', '_broadcaster_type', '_description',
                 'profile_image_url', '_offline_image_url', 'view_count', 'email', 'created_at')

    def __init__(self, data: Union[UserPayload, UserPayloadWithEmail], http):
        self._data: Union[UserPayload, UserPayloadWithEmail] = data
        self._http: HTTPClient = http
        self.id: str = self._data['id']
        self.name: str = self._data['login']
        self.display_name: str = self._data['display_name']
        self._type: str = self._data['type']
        self._broadcaster_type: str = self._data['broadcaster_type']
        self._description: str = self._data['description']
        self.profile_image_url: str = self._data['profile_image_url']
        self._offline_image_url: str = self._data['offline_image_url']
        self.email: Optional[str] = self._data.get('email')
        self.created_at: datetime = parse_rfc3339_timestamp(timestamp=self._data['created_at'])

    def __repr__(self) -> str:
        return f'<User id={self.id} login={self.name} display_name={self.display_name}>'

    async def refresh(self) -> Broadcaster:
        """
        Refreshes the broadcaster's information from the server.
        """
        self._data = await self._http.get_client()
        return self

    @property
    def description(self) -> Optional[str]:
        """
        Returns the user's description, if available.
        """
        return empty_to_none(text=self._description)

    @property
    def url(self) -> Optional[str]:
        """
        Returns the channel URL.
        """
        return f'https://www.twitch.tv/{self.name}'

    @property
    def user_type(self) -> Optional[str]:
        """
        Returns the user's type.
        """
        return empty_to_none(text=self._type)

    @property
    def broadcaster_type(self) -> Optional[str]:
        """
        Returns the user's broadcaster type.
        """
        return empty_to_none(text=self._broadcaster_type)

    @property
    def offline_image(self) -> Optional[str]:
        """
        Returns the URL of the user's offline image, if available.
        """
        return empty_to_none(text=self._offline_image_url)

    async def get_stream(self) -> Optional[Stream]:
        """
        Retrieves the stream associated with the broadcaster.
        """
        data = await self._http.get_stream(user_id=self.id)
        if data:
            return Stream(stream=data)
        return None
