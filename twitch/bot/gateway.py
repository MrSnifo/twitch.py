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

import asyncio
import aiohttp
import twitch

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Optional, List, ClassVar
    from .state import ConnectionState


import logging
_logger = logging.getLogger(__name__)

__all__ = ('IRCWebSocket',)


class IRCWebSocket:
    """
    Represents an IRC WebSocket connection.
    """
    BASE: ClassVar[str] = 'wss://irc-ws.chat.twitch.tv:443'

    __slots__ = ('_ws', '__connection', 'message_queue', '_connect', 'semaphore',
                 'username', 'lock')

    def __init__(self, connection: ConnectionState, username: str):
        self._ws: Optional[aiohttp.ClientWebSocketResponse] = None
        self.__connection: ConnectionState = connection
        self.message_queue = asyncio.Queue(maxsize=10)
        self._connect: asyncio.Event = asyncio.Event()
        self.semaphore = asyncio.Semaphore(10)
        self.username: str = username
        self.lock = asyncio.Lock()

    async def wait_for_connect(self) -> None:
        """
        Wait for the WebSocket connection to be established.
        """
        await self._connect.wait()

    async def connect(self, reconnect: bool) -> None:
        """
        Establish a WebSocket connection to Twitch IRC servers.
        """
        try:
            _retry = 0
            while True:
                _retry = (_retry % 6) + 1  # Cycle from 1 to 6 and back to 1
                try:
                    self._ws = await self.__connection.http.ws_connect(url=self.BASE)
                    await self.authenticate()
                    await self.join_rooms()
                    await self.handle_messages()
                except (twitch.WebsocketClosed, twitch.SessionClosed, asyncio.TimeoutError,
                        twitch.Unauthorized) as error:
                    if isinstance(error, twitch.SessionClosed):
                        _logger.error('Failed to establish a WebSocket connection due to a closed session. '
                                      'Retrying in %s seconds...', _retry * 5)
                    else:
                        _logger.error('WebSocket connection failed: %s Retrying in %s seconds...',
                                      str(error), _retry * 5)
                    await asyncio.sleep(5 * _retry)
                except (twitch.WebSocketError, aiohttp.ClientConnectorError) as error:
                    if not self.__connection.http.is_force_closed:
                        if reconnect:
                            _logger.error('IRC WebSocket connection error: %s Retrying in %s seconds...',
                                          str(error), _retry * 5)
                            await asyncio.sleep(5 * _retry)
                        else:
                            raise
                    else:
                        raise
        finally:
            self._connect.set()

    async def authenticate(self) -> None:
        """
        Authenticate the WebSocket connection with the Twitch server.
        """
        token = self.__connection.http.get_token()
        if token:
            await self._ws.send_str('CAP REQ :twitch.tv/membership twitch.tv/tags twitch.tv/commands')
            await self._ws.send_str(f'PASS oauth:{token}')
            await self._ws.send_str(f'NICK {self.username}')
        else:
            raise twitch.SessionClosed

    async def join_rooms(self) -> None:
        """
        Join Twitch chat rooms associated with the connection.
        """
        if len(self.__connection.chat_rooms.values()) > 0:
            _channels = ','.join(f"#{user.name}" for user in self.__connection.chat_rooms.values())
            await self._ws.send_str(f'JOIN {_channels}')

    async def join_chatroom(self, username: str) -> None:
        """
        Join a specific user's chat room.
        """
        _logger.debug('Bot is joining %s chat room.', username)
        await self._ws.send_str(f'JOIN #{username}')

    async def leave_chatroom(self, username: str) -> None:
        """
        Leave a specific user's chat room.
        """
        _logger.debug('Bot is leaving %s chat room.', username)
        await self._ws.send_str(f'PART #{username}')

    async def send_message(self, username: str, text: str) -> None:
        """
        Send a message to a specific chat room.
        """
        async with self.semaphore:
            await self.message_queue.put(f'PRIVMSG #{username} :{text}')
            await self._send_next()

    async def _send_next(self):
        """
        A safe way to send message.
        """
        async with self.lock:
            while not self.message_queue.empty():
                message = await self.message_queue.get()
                await self._ws.send_str(message)
                # Ratelimit lock, temporary solution.
                await asyncio.sleep(1.45)

    async def replay(self, message_id: str, username: str, text: str) -> None:
        """
        Reply to a sp specific message.
        """
        async with self.semaphore:
            await self.message_queue.put(f'@reply-parent-msg-id={message_id} PRIVMSG #{username} :{text}')
            await self._send_next()

    async def handle_messages(self) -> None:
        """
        Handle incoming messages from the WebSocket.
        """
        while True:
            msg = await asyncio.wait_for(self._ws.receive(), timeout=None)
            if msg.type == aiohttp.WSMsgType.TEXT:
                await self.received_response(response=str(msg.data))
            elif msg.type == aiohttp.WSMsgType.CLOSED:
                close_code = self._ws.close_code
                exception = self._ws.exception()
                error_message = str(exception) if exception else 'Unknown'
                raise twitch.WebsocketClosed(message=f'IRC Connection has been closed,'
                                                     f' Close code: {close_code} Cause: {error_message}.')
            elif msg.type == aiohttp.WSMsgType.ERROR:
                exception = self._ws.exception()
                error_message = str(exception) if exception else 'Unknown error occurred.'
                raise twitch.WebSocketError(message=error_message)

    async def received_response(self, response: str) -> None:
        """
        Process and handle incoming IRC messages.
        """
        await self.__connection.irc_socket_raw_receive(response)
        messages: List[str] = response.split('\r\n')
        for message in messages:
            if message != '':
                try:
                    parsed = twitch.ircv3_to_json(message)
                    if parsed['command']['command'] == 'PRIVMSG':
                        await self.__connection.message(data=parsed)
                        return
                    if parsed['command']['command'] == 'GLOBALUSERSTATE':
                        await self.__connection.irc_connect()
                        self._connect.set()
                        return
                    if parsed['command']['command'] == 'USERSTATE':
                        await self.__connection.join_chatroom(parsed['command']['channel'])
                        return
                    if parsed['command']['command'] == 'PART':
                        await self.__connection.leave_chatroom(parsed['command']['channel'])
                        return
                    if parsed['command']['command'] == 'WHISPER':
                        await self.__connection.whisper(data=parsed)
                        return
                    if parsed['command']['command'] == 'NOTICE':
                        error_message = parsed['parameters'].split(':', 1)[-1].lower()
                        if 'authentication failed' in error_message:
                            raise twitch.Unauthorized(f'IRC server {error_message}.')
                        if 'permission to perform that action' in error_message.lower():
                            raise twitch.Unauthorized(
                                'The user access token must include the chat:edit scope.'
                            )
                        if 'sending messages too quickly.' in error_message.lower():
                            _logger.error('bot is sending messages too quickly.')
                            return
                        raise twitch.Forbidden(error_message)
                except (twitch.Unauthorized, twitch.Forbidden) as error:
                    if isinstance(error, twitch.Unauthorized) and 'chat:edit' in str(error):
                        _logger.exception('Ignoring parsing error: %s', error)
                    else:
                        raise
                except Exception as error:
                    _logger.exception('Ignoring parsing error: [%s] %s', message, error)
