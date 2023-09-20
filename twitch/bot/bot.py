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

from twitch.gateway import EventSubWebSocket
from .state import ConnectionState
from .gateway import IRCWebSocket
import asyncio
import twitch

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import List, Optional, Union

import logging
_logger = logging.getLogger(__name__)

__all__ = ('Bot',)


class Bot(twitch.Client):
    """
    Represents a Twitch Bot.

    ???+ info
        This bot will automatically join its room by default.
         You can leave your own room using the `leave_chatroom` method.

        Default scopes: `user:read:email`, `chat:read`

    Parameters
    ----------
    client_id: str
        Your app's client ID.
    client_secret: Optional[str]
        Your app's client secret. Required when generating
        a new access token if the user access token is not provided.
        It ensures manual authorization or token generating.
    cli: bool
        Whether to run the client in development mode using the Twitch CLI.
        For testing purposes during development.
    port: int
        The port for the Twitch **CLI websocket** and **Eventsub subscription API**.
    """

    def __init__(self, client_id: str, client_secret: Optional[str] = None, cli: bool = False,
                 port: int = 8080) -> None:
        super().__init__(client_id, client_secret, cli, port)
        # Default scopes
        self.scopes: List[str] = ['user:read:email', 'chat:read']
        self._connection: ConnectionState = ConnectionState(dispatcher=self.dispatch, http=self.http)

    async def connect(self, access_token: str, *, refresh_token: Optional[str], reconnect: bool) -> None:
        if self.loop is None:
            await self._setup_loop()

        # Validating the access key and opening a new session.
        validation = await self.http.open_session(token=access_token, refresh_token=refresh_token)
        # Retrieving the client.
        await self._connection.setup_client()

        events = [attr.replace('on_', '', 1) for attr in dir(self) if attr.startswith('on_')]
        # Creating an EventSub websocket.
        EventSub = EventSubWebSocket(connection=self._connection, loop=self.loop, events=events)
        IRC = IRCWebSocket(connection=self._connection, username=self.user.name)
        self._connection.irc_websocket = IRC

        # Debug mode.
        if self._cli:
            EventSub.cli = f'ws://localhost:{self._port}/ws'
            self.http.cli = f'http://localhost:{self._port}/eventsub/subscriptions'
        tasks: List[asyncio.Task] = [
            self.loop.create_task(self.http.refresher(expires_in=validation['expires_in']),
                                  name="Twitchify:Refresher"),
            self.loop.create_task(IRC.connect(reconnect=reconnect), name="Twitchify:IRC")]

        await IRC.wait_for_connect()
        # Joining the room after connect.
        await self.join_chatroom(user=self.user)
        tasks.append(
            self.loop.create_task(EventSub.connect(reconnect=reconnect), name="Twitchify:EventSub")
        )
        await asyncio.gather(*tasks)

    async def join_chatroom(self, user: Union[str, twitch.BaseUser]) -> None:
        """
        Join a Twitch chat room.

        ???+ Warning
            Repeatedly trying to enter channels from which you've been banned can be seen as
            disruptive behavior and may flag your bot as troublesome. Avoid maintaining a
            list of banned channels, as you may not know if you've been unbanned.
            For functional bots, get permission (streamer opt-in) rather than promoting the bot
            without consent. Respectful behavior is crucial for a positive experience.

        Parameters
        ----------
        user: Union[str, twitch.BaseUser]
            The user or username to join the chat room of.

        Raises
        ------
        NotFound
            * Unable to find the requested user.
        """
        await self._connection.join(user=user)

    async def leave_chatroom(self, user: Union[str, twitch.BaseUser]) -> None:
        """
        Leave a Twitch chat room.

        Parameters
        ----------
        user: Union[str, twitch.BaseUser]
            The user or username to leave the chat room of.

        Raises
        ------
        NotFound
            * Unable to find the requested user.
        """
        await self._connection.leave(user=user)

    async def send(self, text: str, *, user: Union[str, twitch.BaseUser] = twitch.MISSING) -> None:
        """
        Send a message to a Twitch chat room.

        | Scopes        | Description          |
        | ------------- | -------------------- |
        | `chat:edit`   | Send chat messages.  |

        Parameters
        ----------
        user: Union[str, twitch.BaseUser]
            The user or username of the chat room to send the message to.
        text: str
            The message text to send.

        Raises
        ------
        NotFound
            * Unable to find the requested user.
        ValueError
            * The text may contain a maximum of 500 characters.
        Unauthorized
            * The user access token must include the chat:edit scope.
        """
        await self._connection.send_message(user=user, text=text)

    async def replay(self, message: Union[str, twitch.Message], text: str) -> None:
        """
        Replay to a specific message in a Twitch chat room.

        | Scopes        | Description          |
        | ------------- | -------------------- |
        | `chat:edit`   | Send chat messages.  |

        Parameters
        ----------
        message: Union[str, twitch.Message]
            The message ID or message object to reply to.
        text: str
            The reply message text.

        Raises
        ------
        NotFound
            * Unable to find the requested user.
        ValueError
            * The text may contain a maximum of 500 characters.
        Unauthorized
            * The user access token must include the chat:edit scope.
        """
        await self._connection.replay(message=message, text=text)
