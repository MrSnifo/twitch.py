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

from urllib.parse import urlparse
from typing import TYPE_CHECKING
from aiohttp import web
import json

if TYPE_CHECKING:
    from typing import Dict, List, Any

import logging
_logger = logging.getLogger(__name__)


class WebSocket:
    """
    Manages WebSocket connections, client subscriptions, and data distribution.
    """

    __slots__ = ('clients',)

    def __init__(self) -> None:
        self.clients: Dict[str, List[web.WebSocketResponse]] = {}

    def add_client(self, ws: web.WebSocketResponse, filter_param: str) -> None:
        """Add a WebSocket client to the list associated with the filter parameter."""
        if filter_param not in self.clients:
            self.clients[filter_param] = []
        self.clients[filter_param].append(ws)
        _logger.debug('Client added with default `%s`. Total clients: %s',
                      filter_param, len(self.clients[filter_param]))

    def remove_client(self, ws: web.WebSocketResponse) -> None:
        """Remove a WebSocket client from the list of clients for its filter parameter."""
        for filter_param, clients_list in self.clients.items():
            if ws in clients_list:
                clients_list.remove(ws)
                if not clients_list:  # Clean up if no clients left for this filter
                    del self.clients[filter_param]
                _logger.debug('Client removed with default `%s`. Total clients: %s',
                              filter_param, len(clients_list))
                return

    async def handle_connection(self, request: web.Request) -> web.WebSocketResponse:
        """Handle WebSocket connection, prepare, and start interaction."""
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        # Extract the filter parameter from the URL query
        filter_param = request.query.get('default', 'all')
        self.add_client(ws, filter_param)

        try:
            await self.receive_and_echo(ws)
        finally:
            self.remove_client(ws)
            await ws.close()
        return ws

    @staticmethod
    def _format_attachment_url(path: str) -> str:
        """Prepend '/upload/' to local file names; leave URLs unchanged."""
        if urlparse(path).scheme:
            return path
        return f"/upload/{path}"

    async def send_data(self, data: Dict[str, Any], filter_key: str):
        """Send data to all clients associated with the given filter parameter."""
        clients_list = self.clients.get(filter_key, [])

        # Update 'image' and 'audio' fields with formatted URLs if necessary
        for key in ['image', 'audio']:
            if data.get(key):
                data[key] = self._format_attachment_url(data[key])

        for client in clients_list[:]:
            try:
                await client.send_str(json.dumps(data))
            except Exception as exc:
                clients_list.remove(client)
                _logger.exception('Error sending message to WebSocket client', exc)

    @staticmethod
    async def receive_and_echo(ws: web.WebSocketResponse) -> None:
        """Receive and echo back any message received from the WebSocket."""
        try:
            async for msg in ws:
                if msg.type == web.WSMsgType.TEXT:  # type: ignore
                    await ws.send_str(f'Echo: {msg.data}')  # type: ignore
                elif msg.type == web.WSMsgType.ERROR:  # type: ignore
                    _logger.error('WebSocket error: {ws.exception()}')
        except Exception as exc:
            _logger.exception('Exception while receiving WebSocket message', exc)
