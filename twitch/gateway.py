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

from .errors import (WebSocketError, WebsocketClosed, NotFound, SessionClosed, Forbidden,
                     SubscriptionError, WsReconnect)
from .utils import to_json, get_subscriptions

from json import JSONDecodeError
from aiohttp import WSMsgType
import asyncio

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .types.eventsub.subscriptions import SubscriptionInfo
    from asyncio import AbstractEventLoop
    from typing import Optional, List, Dict, Any
    from aiohttp import ClientWebSocketResponse
    from .state import ConnectionState
    from .http import HTTPClient
    from .types.gateway import Session, Subscription

import logging
_logger = logging.getLogger(__name__)


class EventSubWebSocket:
    DEFAULT_URL = 'wss://eventsub.wss.twitch.tv/ws'

    __slots__ = ('__http', '__connection', '__loop', 'subscriptions', '_ready', '_keep_alive',
                 '_ws', '_ws_switch', 'session_id', 'retry_count')

    def __init__(self, *, http: HTTPClient, cnx: ConnectionState, loop, events: List[str]) -> None:
        """
        Initialize the EventSubWebSocket.

        :param http: The HTTP client for making API requests.
        :param cnx: The ConnectionState object.
        :param loop: The event loop.
        :param events: A list of events.
        """
        self.__http: HTTPClient = http
        self.__connection: ConnectionState = cnx
        self.__loop: AbstractEventLoop = loop
        self.subscriptions: List[SubscriptionInfo] = get_subscriptions(events=events)
        # Default subscription
        self.subscriptions.append({'name': 'user.update', 'version': '1'})
        # Default Session KeepAlive.
        self._keep_alive: int = 10
        self._ws: Optional[ClientWebSocketResponse] = None
        self._ws_switch: Optional[ClientWebSocketResponse] = None
        self.session_id: Optional[str] = None
        self.retry_count: int = 0

    async def _connect(self, url) -> None:
        """
        Establish a WebSocket connection.

        :param url: The URL to connect to.
        """
        if self.__http.is_open:
            _ws = await self.__http.ws_connect(url=url)
            if self._ws is not None and not self._ws.closed:
                self._ws_switch = self._ws
                self._ws = _ws
            else:
                self._ws = _ws
            self.retry_count = 0
            await self.handle_messages()
        else:
            raise SessionClosed

    async def connect(self, url: str = DEFAULT_URL) -> None:
        """
        Connect to the WebSocket.

        :param url: The URL to connect to. Default is the DEFAULT_URL.
        """
        while True:
            try:
                await self._connect(url=url)
            except WsReconnect as reconnect_url:
                url = str(reconnect_url)
                _logger.debug('Reconnecting to URL: %s', url)
                continue
            except (OSError, WebSocketError, SessionClosed, TimeoutError) as error:
                self.retry_count += 1
                if 3 >= self.retry_count:
                    if isinstance(error, WebSocketError):
                        _logger.error('WebSocket connection closed. Retrying in %s seconds...',
                                      (5 * self.retry_count))
                    elif isinstance(error, SessionClosed):
                        _logger.error('Cannot connect because the session is closed.'
                                      ' Retrying in %s seconds...', (5 * self.retry_count))
                    elif isinstance(error, asyncio.TimeoutError):
                        _logger.error('Timeout occurred while waiting for WebSocket message. '
                                      'Retrying in %s seconds...', (5 * self.retry_count))
                    else:
                        _logger.info('Retrying to connect to the WebSocket (%s) in %s seconds...',
                                     url, (5 * self.retry_count))
                else:
                    raise  # Re-raise the original error
                await asyncio.sleep(5 * self.retry_count)

    async def handle_messages(self) -> None:
        """
        Handle incoming WebSocket messages.
        """
        while True:
            msg = await asyncio.wait_for(self._ws.receive(), timeout=(self._keep_alive + 10))
            if msg.type == WSMsgType.TEXT:
                await self.received_response(response=str(msg.data))
            elif msg.type == WSMsgType.CLOSED:
                _logger.error('WebSocket connection closed by the server')
                close_code = self._ws.close_code
                if close_code == 4004:
                    raise WebsocketClosed('Failed to reconnect to a new WebSocket within'
                                          ' the specified time.')
                elif close_code == 4007:
                    raise WebsocketClosed('Failed to reconnect to a new WebSocket.'
                                          ' The reconnect URL provided is invalid.')
                elif close_code in [4000, 4001, 4002, 4003, 4005, 4006]:
                    raise WebSocketError(
                        f'WebSocket connection closed by the server. Close code:{close_code}')
                else:
                    raise WebSocketError(
                        f'WebSocket connection closed by the server. Close code:{close_code}')
            elif msg.type == WSMsgType.ERROR:
                exception = self._ws.exception()
                error_message = str(exception) if exception else 'Unknown error occurred'
                raise WebSocketError(f'WebSocket connection closed with error:{error_message}')

    async def received_response(self, response: str) -> None:
        """
        Process the received response.

        :param response: The response received from the WebSocket.
        """
        try:
            response: dict = to_json(text=response)
        except (UnicodeDecodeError, JSONDecodeError) as error:
            _logger.error('Failed to parse response as JSON: %s. Response: %s', error, response)
            raise  # Re-raise the original error
        else:
            if response.get('metadata') is not None:
                metadata = response['metadata']
                # ====> Session Keepalive <====
                if metadata['message_type'] == 'session_keepalive':
                    _logger.debug(
                        'Received a keepalive message. The WebSocket connection is healthy.')
                # ====> Session Welcome <====
                elif metadata['message_type'] == 'session_welcome':
                    _session: Session = response['payload']['session']
                    _logger.debug('Connected to WebSocket. Session ID: %s', _session['id'])
                    # Close the old connection until the new reconnect websocket receive a
                    # Welcome message.
                    if self._ws_switch is not None and not self._ws_switch.closed:
                        # Closing the old connection.
                        await self._ws_switch.close()
                        self._ws_switch = None
                    else:
                        # Subscribing to events.
                        task = self.__http.subscribe(user_id=self.__connection.broadcaster.id,
                                                     session_id=_session['id'],
                                                     subscriptions=self.subscriptions)
                        self.__loop.create_task(task, name='Twitchify:Subscriptions')
                    if _session['id'] != self.session_id:
                        if self.session_id is not None:
                            _logger.debug('A new WebSocket Session has been detected ID: %s',
                                          _session['id'])
                        self.session_id = _session['id']
                    # KeepAlive timeout.
                    self._keep_alive = _session['keepalive_timeout_seconds']

                # ====> Session Reconnect <====
                elif metadata['message_type'] == 'session_reconnect':
                    _session: Session = response['payload']['session']
                    raise WsReconnect(url=_session['reconnect_url'])

                # ====> Subscription notification <====
                elif metadata['message_type'] == 'notification':
                    _subscription: Subscription = response['payload']['subscription']
                    _event: Dict[Any] = response['payload']['event']
                    await self.__connection.parse(method=_subscription['type'], data=_event)

                # ====> Subscription Revocation <====
                elif metadata['message_type'] == 'revocation':
                    _subscription: Subscription = response['payload']['subscription']
                    _status = _subscription['status']
                    # Revoked the authorization token that the subscription relied on.
                    if _status == 'authorization_revoked':
                        raise Forbidden(f'The user has revoked authorization for the'
                                        f' `{_subscription["type"]}` subscription.')
                    # The user mentioned in the subscription no longer exists.
                    elif _status == 'user_removed':
                        raise NotFound(
                            'The user mentioned in the subscription no longer exists.'
                        )
                    # Subscription type and version is no longer supported.
                    elif _status == 'version_removed':
                        raise SubscriptionError(subscription=_subscription['type'],
                                                version=_subscription['version'])
