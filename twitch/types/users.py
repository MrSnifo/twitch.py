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

from typing import TypedDict, TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List, Literal, Dict


class Broadcaster(TypedDict):
    """
    Represents a broadcaster.

    Attributes
    ----------
    broadcaster_id: str
        The unique identifier for the broadcaster.
    broadcaster_name: str
        The display name of the broadcaster.
    broadcaster_login: str
        The login name of the broadcaster.
    """
    broadcaster_id: str
    broadcaster_name: str
    broadcaster_login: str


class Moderator(TypedDict):
    """
    Represents a moderator.

    Attributes
    ----------
    moderator_id: str
        The unique identifier for the moderator.
    moderator_name: str
        The display name of the moderator.
    moderator_login: str
        The login name of the moderator.
    """
    moderator_id: str
    moderator_name: str
    moderator_login: str


class SpecificUser(TypedDict):
    """
    Represents a specific user.

    Attributes
    ----------
    user_id: str
        The unique identifier for the user.
    user_name: str
        The display name of the user.
    user_login: str
        The login name of the user.
    """
    user_id: str
    user_name: str
    user_login: str


# Auth
class OAuthToken(TypedDict):
    client_id: str
    login: str
    scopes: List[str]
    user_id: str
    expires_in: int


class OAuthRefreshToken(TypedDict):
    access_token: str
    expires_in: int
    refresh_token: str
    token_type: str


class DeviceAuthFlow(TypedDict):
    device_code: str
    expires_in: int
    interval: int
    user_code: str
    verification_uri: str


class Transport(TypedDict):
    method: Literal['webhook', 'websocket', 'conduit']
    callback: str


class EventSubSubscription(TypedDict):
    id: str
    status: Literal['webhook_callback_verification_pending', 'enabled', 'disabled']
    type: str
    version: str
    condition: Dict[str, str]
    created_at: str
    transport: Transport
    cost: int


# User

class User(TypedDict):
    """
    Represents a user.

    Attributes
    ----------
    id: str
        The unique identifier for the user.
    login: str
        The login name of the user.
    display_name: str
        The display name of the user.
    type: Literal['admin', 'global_mod', 'staff', '']
        The type of user.
    broadcaster_type: Literal['affiliate', 'partner', '']
        The broadcaster type of the user.
    description: str
        A brief description of the user.
    profile_image_url: str
        The URL to the user's profile image.
    offline_image_url: str
        The URL to the user's offline image.
    email: str
        The email address of the user.
    created_at: str
        The date and time when the user account was created, in ISO 8601 format.
    """
    id: str
    login: str
    display_name: str
    type: Literal['admin', 'global_mod', 'staff', '']
    broadcaster_type: Literal['affiliate', 'partner', '']
    description: str
    profile_image_url: str
    offline_image_url: str
    email: str
    created_at: str
