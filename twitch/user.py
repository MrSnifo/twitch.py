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
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .types.eventsub import (channel as chl, user as us)
    from typing import Union, Optional, Dict, Any
    from datetime import datetime


class User:
    """
    Represents a user.
    """
    __slots__ = ('id', 'name', 'display_name')

    def __init__(self, *, user: Dict[str, Any], prefix: str = 'user') -> None:
        self.id: str = user.get(f'{prefix}_id') or '0'
        self.name: str = user.get(f'{prefix}_login') or 'anonymous'
        self.display_name: str = user.get(f'{prefix}_name') or 'Anonymous'

    def __repr__(self) -> str:
        return f'<User id={self.id} login={self.name} display_name={self.display_name}>'


class Follower(User):
    """
    Represents a follower user.
    """
    __slots__ = 'followed_at'

    def __init__(self, *, channel: chl.Follow) -> None:
        super().__init__(user=channel)
        self.followed_at: datetime = parse_rfc3339_timestamp(timestamp=channel['followed_at'])

    def __repr__(self) -> str:
        return f'<Follower {super().__repr__()} followed_at={self.followed_at}>'


class Update(User):
    """
    Represents a user updated his information.
    """
    __slots__ = ('description', 'email', 'email_verified')

    def __init__(self, *, update: us.Update) -> None:
        super().__init__(user=update)
        self.description: str = update['description']
        self.email: Optional[str] = update.get('email')  # Requires user:read:email scope
        self.email_verified: bool = update['email_verified']

    def __repr__(self) -> str:
        return f'<Update user={super().__repr__()} description={self.description} email={self.email}>'


class Broadcaster:
    """
    Represents a Twitch user.
    """

    __slots__ = ('id', 'name', 'display_name', '_type', '_broadcaster_type', '_description', 'profile_image_url',
                 '_offline_image_url', 'view_count', 'email', '_created_at')

    def __init__(self, data: Union[UserPayload, UserPayloadWithEmail]):
        self.id: str = data['id']
        self.name: str = data['login']
        self.display_name: str = data['display_name']
        self._type: str = data['type']
        self._broadcaster_type: str = data['broadcaster_type']
        self._description: str = data['description']
        self.profile_image_url: str = data['profile_image_url']
        self._offline_image_url: str = data['offline_image_url']
        self.view_count = int(data['view_count'])
        self.email: Optional[str] = data.get('email')
        self._created_at: str = data['created_at']

    def __repr__(self) -> str:
        return f'<User id={self.id} login={self.name} display_name={self.display_name}>'

    @property
    def description(self) -> Optional[str]:
        """
        Returns the user's description, if available.

        Returns:`Optional[str]`
        """
        return empty_to_none(text=self._description)

    @property
    def url(self) -> Optional[str]:
        """
        Returns the channel url.

        Returns:`str`
        """
        return f'https://www.twitch.tv/{self.name}'

    @property
    def user_type(self) -> Optional[str]:
        """
        Returns the user's type.

        Returns:`Optional[str]`
            The user's type, or None if it's a normal user.
            Possible values are 'admin ', 'global_mod', 'staff', or None.
        """
        return empty_to_none(text=self._type)

    @property
    def broadcaster_type(self) -> Optional[str]:
        """
        Returns the user's broadcaster type.

        Returns:`Optional[str]`
            The user's broadcaster type, or None if it's a normal broadcaster.
            Possible values are 'affiliate', 'partner', or None.
        """
        return empty_to_none(text=self._broadcaster_type)

    @property
    def offline_image(self) -> Optional[str]:
        """
        Returns the URL of the user's offline image, if available.

        Returns:`Optional[str]`
        """
        return empty_to_none(text=self._offline_image_url)

    @property
    def created_at(self) -> datetime:
        """
        Returns the UTC date and time when the user's account was created.

        Returns:`Optional[str]`
        """
        return parse_rfc3339_timestamp(timestamp=self._created_at)
