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

from .utils import convert_rfc3339

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Dict, Union, Optional, List, Any
    from .types import user as UserTypes
    from datetime import datetime

__all__ = ('BaseUser',  'User', 'UserEmail', 'UserImages')


class BaseUser:
    """
    Represents basic information about a user.

    Attributes
    ----------
    id: str
        The unique identifier for the user.
    name: str
        The username or login name of the user.
    display_name: str
        The display name of the user, typically a more user-friendly version of the name.

    Methods
    -------
    __str__() -> str
        Returns the username (login name) as a string when the instance is converted to a string.
    __eq__(other: object) -> bool
        Checks if two BaseUser instances are equal based on their IDs.
    __ne__(other: object) -> bool
        Checks if two BaseUser instances are not equal based on their IDs.
    """
    __slots__ = ('id', 'name', 'display_name', '__prefix')

    if TYPE_CHECKING:
        id: str
        name: str
        display_name: str

    def __init__(self, data: Dict[str, Any], *, prefix: Optional[Union[str, List[str]]] = None) -> None:
        self.__prefix = prefix
        self._update_data(data=data)

    def __repr__(self) -> str:
        return f'<BaseUser id={self.id} login={self.name} display_name={self.display_name}>'

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other: object) -> bool:
        if isinstance(other, BaseUser):
            return self.id == other.id
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def _update_data(self, data: Dict[str, ...]) -> None:
        if self.__prefix is None:
            self.__prefix = ['']
        if isinstance(self.__prefix, str):
            self.__prefix = [self.__prefix]
        user_prefix = next((prefix for prefix in self.__prefix if data.get(f'{prefix}id')), '')
        self.id = data.get(f'{user_prefix}id', '0')
        self.name = data.get(f'{user_prefix}login', 'anonymous')
        self.display_name = data.get('display_name') or data.get(f'{user_prefix}name', 'Anonymous')


class UserEmail:
    """
    Represents user email information.

    Attributes
    ----------
    email: str
        The user's email address.
    is_verified: bool
        Indicates whether the email address is verified.

    Methods
    -------
    __str__() -> str
        Returns the email address as a string.
    __bool__() -> bool
        Returns True if the email address is not None, indicating its presence.
    """
    __slots__ = ('email', 'is_verified')

    if TYPE_CHECKING:
        email: str
        is_verified: bool

    def __init__(self, data: Union[UserTypes.User, UserTypes.UserUpdateEvent]) -> None:
        self._update_data(data=data)

    def __repr__(self) -> str:
        return f'<Email email={self.email} is_verified={self.is_verified}>'

    def __str__(self) -> str:
        return self.email

    def __bool__(self) -> bool:
        return self.email is not None

    def _update_data(self, data: Union[UserTypes.User, UserTypes.UserUpdateEvent]) -> None:
        self.email: str = data.get('email')
        self.is_verified: bool = data.get('email_verified') if data.get('email_verified') else True


class UserImages:
    """
    Represents user profile and offline images.

    Attributes
    ----------
    offline: str
        URL of the user's offline image.
    profile: str
        URL of the user's profile image.

    Methods
    -------
    __str__() -> str
        Returns the profile image URL as a string.
    """
    __slots__ = ('offline', 'profile')

    if TYPE_CHECKING:
        offline: str
        profile: str

    def __init__(self, data: UserTypes.UserImages) -> None:
        self._update_data(data=data)

    def __repr__(self) -> str:
        return f'<UserImages profile={self.profile} offline={self.offline}>'

    def __str__(self) -> str:
        return self.profile

    def _update_data(self, data: UserTypes.UserImages) -> None:
        self.profile = data['profile_image_url']
        self.offline = data['offline_image_url']


class User(BaseUser):
    """
    Represents a Twitch user with extended attributes.

    Attributes
    ----------
    type: str
        The type of user (e.g., 'normal', 'partner').
    email: Optional[UserEmail]
        The user's email address if available.
    images: UserImages
        User profile and offline images.
    created_at: datetime
        The date and time when the user account was created.
    description: str
        The user's description or bio.
    broadcaster_type: str
        The broadcaster type (e.g., 'normal', 'affiliate').
    """
    __slots__ = ('type', 'email', 'images', 'created_at', 'description', 'broadcaster_type',
                 '__weakref__')

    if TYPE_CHECKING:
        type: str
        email: Optional[UserEmail]
        images: UserImages
        created_at: datetime
        description: str
        broadcaster_type: str

    def __init__(self, data: UserTypes.User) -> None:
        super().__init__(data=data)
        self._update_data(data=data)

    def __repr__(self) -> str:
        return f'<User id={self.id} name={self.name} created_at={self.created_at}>'

    def _update_data(self, data: UserTypes.User) -> None:
        super()._update_data(data=data)
        self.type = data['type'] or 'normal'
        self.email = UserEmail(data=data) or None
        self.images = UserImages(data=data)
        self.created_at = convert_rfc3339(data['created_at'])
        self.description = data['description']
        self.broadcaster_type = data['broadcaster_type'] or 'normal'
