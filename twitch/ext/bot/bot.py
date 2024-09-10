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
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, overload
import twitch

if TYPE_CHECKING:
    from twitch.user import User, Broadcaster
    from typing import Optional, List


import logging
_logger = logging.getLogger(__name__)

__all__ = ('Bot',)


class Bot(twitch.Client):
    """
    A class that extends the functionality of the `Client` class.

    This extension adds capabilities for managing multiple users and their tokens,
    allowing the bot to perform actions on behalf of registered users for more flexibility.

    Parameters
    ----------
    client_id: str
        The client ID used to authenticate with the Twitch API.
    client_secret: Optional[str]
        The client secret used for authentication. Default is None.
    **options:
        Additional configuration options:

        - cli: [bool][bool]

            Flag indicating if CLI mode is enabled.

            **Default**: `False`

            ___

        - cli_port: [int][]

            The port number used for CLI mode.

            **Default**: `8080`
            ___

        - socket_debug: [False][bool]

            Flag indicating if raw WebSocket messages should be dispatched for debugging purposes.
            If enabled, raw WebSocket messages are dispatched to the on_socket_raw_receive.

            **Default**: `False`
            ___

        - proxy: [Optional][typing.Optional][[str][str]]

            The proxy URL to use for HTTP requests.

            **Default**: `None`
            ___

        - proxy_auth: [Optional][typing.Optional][aiohttp.BasicAuth]

            Authentication details for the proxy, if required.

            **Default**: `None`
    """
    def __init__(self, client_id: str, client_secret: Optional[str] = None, **options) -> None:
        super().__init__(client_id=client_id, client_secret=client_secret, **options)

    def get_broadcasters(self) -> List[Broadcaster]:
        """
        Retrieve a list of registered broadcasters.

        This method fetches and returns a list of all broadcasters that have been registered
        and are managed by the connection.

        Returns
        -------
        List[Broadcaster]
            A list of Broadcaster objects representing all registered broadcasters.
        """
        return self._connection.get_broadcasters()

    async def get_broadcaster(self, user: User) -> Broadcaster:
        """
        Retrieve a registered broadcaster.

        Parameters
        ----------
        user: User
            The user whose broadcaster details are being requested.

        Returns
        -------
        Broadcaster
            The broadcaster object corresponding to the user.
        """
        return await self._connection.get_broadcaster(user.id)

    async def get_broadcaster_by_id(self, __id: str, /) -> Broadcaster:
        """
        Retrieve a registered broadcaster using their ID.

        Parameters
        ----------
        __id: str
            The ID of the broadcaster.

        Returns
        -------
        Broadcaster
            The broadcaster object corresponding to the ID.
        """
        return await self._connection.get_broadcaster(__id)

    def is_registered(self, user: User) -> bool:
        """
        Check if a broadcaster is registered with the bot.

        Parameters
        ----------
        user: User
            The user to check registration status for.

        Returns
        -------
        bool
            True if the user is registered, False otherwise.
        """
        return self._connection.is_registered(user.id)

    @overload
    async def register_user(self, *, access_token: str, refresh_token: None = None) -> Broadcaster:
        ...

    @overload
    async def register_user(self, *, refresh_token: str, access_token: None = None) -> Broadcaster:
        ...

    @overload
    async def register_user(self, *, access_token: str, refresh_token: str) -> Broadcaster:
        ...

    async def register_user(self, *,
                            access_token: Optional[str] = None,
                            refresh_token: Optional[str] = None) -> Broadcaster:
        """
        Register a broadcaster with an access token, refresh token, or both.

        !!! Warning
            If you are planning to use only a refresh token, a client secret is required.

        Parameters
        ----------
        access_token: Optional[str]
            Access token for the user.
        refresh_token: Optional[str]
            Refresh token for the user.

        Returns
        -------
        Broadcaster
            The broadcaster object corresponding to the registered user.
        """
        if access_token is None and refresh_token:
            if self.client_secret is None:
                raise TypeError('Missing client secret.')

        return await self._connection.register_user(access_token, refresh_token)

    async def unregister_user(self, user: User) -> None:
        """
        Unregister a broadcaster from the bot.

        Parameters
        ----------
        user: User
            The user to remove from registration.
        """
        await self._connection.remove_user(user.id)
