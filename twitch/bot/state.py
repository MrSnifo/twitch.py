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

import twitch.state
import twitch

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Callable, Any, Optional, Union, Dict
    from .gateway import IRCWebSocket
    import twitch.http


import logging
_logger = logging.getLogger(__name__)

__all__ = ('ConnectionState',)


class ConnectionState(twitch.state.ConnectionState):
    """
    Represents the state of the connection.
    """
    __slots__ = ('irc_websocket',)

    def __init__(self, dispatcher: Callable[..., Any], http: twitch.http.HTTPClient) -> None:
        super().__init__(dispatcher, http)
        self.irc_websocket: Optional[IRCWebSocket] = None

    async def join(self, user: Union[str, twitch.BaseUser]) -> None:
        """
        Join a Twitch chat room.
        """
        user = await self.get_user(user)
        if not self.chat_rooms.get(user.id):
            await self.irc_websocket.join_chatroom(username=user.name)
            self.chat_rooms[user.id] = user
        else:
            raise twitch.Conflict('Bot has already joined the chat room.')

    async def leave(self, user: Union[str, twitch.BaseUser]) -> None:
        """
        Leave a Twitch chat room.
        """
        user = await self.get_user(user)
        if self.chat_rooms.get(user.id):
            await self.irc_websocket.leave_chatroom(username=user.name)
            self.chat_rooms.pop(user.id)
        else:
            raise twitch.NotFound('Bot has not joined the chat room.')

    async def send_message(self, text: str, user: Union[str, twitch.BaseUser] = twitch.MISSING) -> None:
        """
        Send a message to a Twitch chat room.
        """
        if user is twitch.MISSING:
            user = self.user
        else:
            user = await self.get_user(user)
        chatroom = self.chat_rooms.get(user.id)
        if chatroom:
            if len(text) > 500:
                raise ValueError('The text may contain a maximum of 500 characters.')
            await self.irc_websocket.send_message(username=user.name, text=text)
        else:
            raise twitch.NotFound('Bot has not joined the chat room.')

    async def replay(self, message: Union[str, twitch.Message], text: str) -> None:
        """
        Replay to a specific message in a Twitch chat room.
        """
        chatroom = self.chat_rooms.get(message.channel_id)
        if isinstance(message, twitch.Message):
            message = message.id
        if chatroom:
            if len(text) > 500:
                raise ValueError('The text may contain a maximum of 500 characters.')
            await self.irc_websocket.replay(message_id=message, username=chatroom.name, text=text)
        else:
            raise twitch.NotFound('Bot has not joined the chat room.')

    async def irc_socket_raw_receive(self, data: str) -> None:
        """
        Receive and process raw IRC messages from the WebSocket.
        """
        self.__dispatch('irc_socket_raw_receive', data)

    async def irc_connect(self) -> None:
        """
        Handle IRC connection events.
        """
        self.__dispatch('irc_connect')

    async def join_chatroom(self, username: str) -> None:
        """
        Handle events when the bot joins a chat room.
        """
        self.__dispatch('join_chatroom', username)

    async def leave_chatroom(self, username: str) -> None:
        """
        Handle events when the bot leaves a chat room.
        """
        self.__dispatch('leave_chatroom', username)

    async def message(self, data: Dict[str, Any]) -> None:
        """
        Handle incoming chat messages.
        """
        message = twitch.Message(data=data)
        self.__dispatch('message', message)

    async def whisper(self, data: Dict[str, Any]) -> None:
        """
        Handle incoming whispers.
        """
        author = twitch.BaseUser(data={'id': data['tags']['user-id'],
                                       'login': data['source']['nick'],
                                       'name': data['tags']['display-name']})
        message = data['parameters'].split(':', 1)[-1]
        self.__dispatch('message', author, message)
