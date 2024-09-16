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

from typing import TYPE_CHECKING
from .template import Template
from aiohttp import web

if TYPE_CHECKING:
    from .attachment import Attachment
    from .geteway import WebSocket
    from typing import Optional

import logging
_logger = logging.getLogger(__name__)


class Route:
    """
    Handles HTTP and WebSocket routes for the application.
    """
    __slots__ = ('gateway', 'attachment', 'default_template')

    def __init__(self, router: web.Application.router, gateway: WebSocket, attachment: Attachment):
        self.gateway: WebSocket = gateway
        self.attachment: Attachment = attachment
        router.add_get('/', self.handle_request)
        router.add_get('/ws', self.websocket_handler)
        router.add_get('/upload/{filename}', self.serve_file)

        # Loading template.
        self.default_template: str = str(Template())

    async def handle_request(self, request: web.Request) -> web.Response:
        """Handle HTTP requests to the main page."""
        response = web.Response(text=self.default_template, content_type='text/html')
        return response

    async def serve_file(self, request: web.Request) -> web.Response:
        """Serve uploaded files from the /upload endpoint."""
        filename: str = request.match_info['filename']
        file_content: Optional[bytes] = self.attachment.get_attachment(filename)
        if not file_content:
            _logger.warning('File not found: %s', filename)
            return web.Response(text='File not found', status=404)
        return web.Response(body=file_content, content_type='application/octet-stream')

    async def websocket_handler(self, request: web.Request) -> web.WebSocketResponse:
        """Handle WebSocket connections."""
        ws = await self.gateway.handle_connection(request)
        return ws
