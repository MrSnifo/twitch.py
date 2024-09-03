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

from .errors import ConnectionClosed
from typing import TYPE_CHECKING
from json import JSONDecodeError
import aiohttp
import asyncio
import json

if TYPE_CHECKING:
    from typing import Optional, Set, ClassVar, Any, Self
    from .state import ConnectionState
    from .client import Client


import logging
_logger = logging.getLogger(__name__)

__all__ = ('EventSubWebSocket', 'ReconnectWebSocket')


class WebSocketClosure(Exception):
    """Exception indicating closure of the WebSocket."""


class ReconnectWebSocket(Exception):
    """Exception indicating the need to reconnect to the websocket."""

    def __init__(self, url: str) -> None:
        self.url: str = url


class EventSubWebSocket:
    """Represents Twitch EventSub WebSocket."""
    DEFAULT_GATEWAY: ClassVar[str] = 'wss://eventsub.wss.twitch.tv/ws?keepalive_timeout_seconds=30'
    SESSION_WELCOME: ClassVar[str] = 'session_welcome'
    SESSION_KEEPALIVE: ClassVar[str] = 'session_keepalive'
    SESSION_RECONNECT: ClassVar[str] = 'session_reconnect'
    NOTIFICATION: ClassVar[str] = 'notification'
    REVOCATION: ClassVar[str] = 'revocation'

    def __init__(self,
                 socket: aiohttp.ClientWebSocketResponse,
                 state: ConnectionState,
                 *,
                 loop: asyncio.AbstractEventLoop) -> None:
        self.socket: aiohttp.ClientWebSocketResponse = socket
        self.loop: asyncio.AbstractEventLoop = loop
        self.session_id: Optional[str] = None
        self._subscriptions_task: Optional[asyncio.Task] = None
        self._state: ConnectionState = state
        self._timeout: Optional[int] = None

    async def close(self, code: int = 3000) -> None:
        """Close the WebSocket connection."""
        if self._subscriptions_task is not None and not self._subscriptions_task.done():
            self._subscriptions_task.cancel()
        await self.socket.close(code=code)

    @property
    def is_open(self) -> bool:
        return not self.socket.closed

    async def create_subscriptions(self, *, events: Set[str], initial: bool) -> None:
        """initial subscriptions."""
        if initial:
            for event in events:
                try:
                    await self._state.create_subscription(self._state.user.id, event, self.session_id)
                except Exception as exc:
                    _logger.exception('Error processing event `on_%s`: %s', event, str(exc))
        else:
            await self._state.initialize_after_disconnect(self.session_id)
        self._state.state_ready()

    @classmethod
    async def initialize_websocket(cls,
                                   client: Client,
                                   state: ConnectionState,
                                   gateway: Optional[str] = None,
                                   resume: bool = False,
                                   initial: bool = False) -> EventSubWebSocket:
        """Initialize websocket connection."""
        gateway = gateway or cls.DEFAULT_GATEWAY
        socket = await client.http.ws_connect(url=gateway, resume=resume)
        state.ws_connect()
        ws: Self = cls(socket, state, loop=client.loop)
        # Waits for welcome message.
        await ws.poll_handle_dispatch()
        if not resume:
            # Get default events.
            events = {attr.replace('on_', '', 1) for attr in dir(client) if attr.startswith('on_')}
            # Add additional default events.
            events.update({'channel_update', 'user_update', 'stream_online', 'stream_offline'})
            task = ws.create_subscriptions(events=events, initial=initial)
            ws._subscriptions_task = ws.loop.create_task(task, name='twitch:gateway:subscriptions')
        else:
            state.state_ready()
        return ws

    async def poll_handle_dispatch(self) -> None:
        """Polls for a DISPATCH event and manages the gateway loop."""
        try:
            # 5 seconds incase something went wrong.
            msg = await self.socket.receive(timeout=(self._timeout or 30) + 5)
            if msg.type is aiohttp.WSMsgType.TEXT:
                await self.received_message(data=msg.data)
            elif msg.type is aiohttp.WSMsgType.ERROR:
                _logger.debug('Received error %s', msg)
                raise WebSocketClosure
            elif msg.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.CLOSING, aiohttp.WSMsgType.CLOSE):
                _logger.debug('Received %s', msg)
                raise WebSocketClosure
        except (asyncio.TimeoutError, WebSocketClosure) as exc:
            code = self.socket.close_code
            raise ConnectionClosed(self.socket, code=code) from exc

    async def received_message(self, *, data: Any) -> None:
        """Handle received message."""
        try:
            data = json.loads(data)
            await self._state.socket_raw_receive(data=data)
        except (UnicodeDecodeError, JSONDecodeError) as error:
            _logger.exception('Failed to parse response as JSON: %s. Response: %s', error)
            return
        if data.get('metadata'):
            metadata = data['metadata']
            if metadata['message_type'] == self.SESSION_WELCOME:
                _session = data['payload']['session']
                _logger.debug('Connected to WebSocket. Session ID: %s', _session['id'])
                self.session_id = _session['id']
                self._timeout = _session['keepalive_timeout_seconds']
                return
            if metadata['message_type'] == self.SESSION_KEEPALIVE:
                _logger.debug('Received a keepalive message. The WebSocket connection is healthy.')
                return

            if metadata['message_type'] == self.SESSION_RECONNECT:
                await self.close()
                self._state.ws_disconnect()
                raise ReconnectWebSocket(url=data['payload']['session']['reconnect_url'])

            if metadata['message_type'] == self.NOTIFICATION:
                self._state.parse(data=data['payload'])
                return

            if metadata['message_type'] == self.REVOCATION:
                _logger.warning(
                    'Subscription Revoked: ID %s, Type "%s", Status "%s"',
                    data['payload']['subscription']['id'],
                    data['payload']['subscription']['type'],
                    data['payload']['subscription']['status'],
                )
                return
