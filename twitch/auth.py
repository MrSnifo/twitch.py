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

from .utils import Scopes, generate_random_state
from .errors import AuthorizationError
from . import __version__, __github__

from aiohttp import web
import urllib.parse
import asyncio

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .types.scoopes import ScopesType
    from .http import HTTPClient
    from .types.http import Token
    from typing import Optional

import logging
access_logger = logging.getLogger('aiohttp.access')
access_logger.setLevel(logging.WARNING)
_logger = logging.getLogger(__name__)

__all__ = ('Auth',)


class Auth:
    """
    Authorization code grant flow

    :param http: The HTTP client for making API requests.
    :param client_id: The client application ID.
    """
    __slots__ = ('_http', '_client_id', 'access_token', 'refresh_token', 'scopes', '_host', '_port',
                 '_force_verify', '_code', '_query', '_state', '_app', '_shutdown_event')

    def __init__(self, http: HTTPClient, client_id: str) -> None:
        self._http: HTTPClient = http
        self._client_id: str = client_id
        # Default values
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.scopes: ScopesType = Scopes
        self._host: str = 'localhost'
        self._port: int = 3000
        self._force_verify: bool = False
        self._code: Optional[str] = None
        self._query: Optional[web.Request.query] = None
        # Help prevent Cross-Site Request Forgery (CSRF) attacks.
        self._state: str = generate_random_state()
        # Application.
        self._app = web.Application()
        self._app.router.add_get('/{tail:.*}', self.handle_redirect)
        # Shutdown the server after receiving one response
        self._shutdown_event = asyncio.Event()

    def __repr__(self) -> str:
        return f'<Auth access_token={self.access_token} refresh_token={self.refresh_token}>'

    @property
    def uri(self) -> str:
        """Get the URI of the server."""
        return f'http://{self._host}:{self._port}'

    @property
    def url(self) -> str:
        """Get the authorization URL."""
        if 'user:read:email' not in self.scopes:
            self.scopes.append('user:read:email')
        # Removing duplicates.
        self.scopes = list(dict.fromkeys(self.scopes))
        encoded_scope = '+'.join(urllib.parse.quote(s) for s in self.scopes)
        url = f'https://id.twitch.tv/oauth2/authorize?response_type=code&client_id={self._client_id}' \
              f'&force_verify={self._force_verify}&redirect_uri={self.uri}&scope={encoded_scope}' \
              f'&state={self._state}'
        return url

    async def handle_redirect(self, request: web.Request) -> web.Response:
        """
        Handle the redirect from Twitch authorization.

        :param request: The web request.
        """
        _logger.debug('Received request to URL: %s', request.rel_url)
        query_params = request.query
        if (query_params.get('code') or query_params.get('error')) \
                and self._state == query_params.get('state'):
            await self.shutdown(query=query_params)
            if query_params.get('code'):
                self._code = query_params.get('code')
                html = f'''
                    <html>
                        <body>
                            <h1>Redirect Completed</h1>
                            <p><a href="{__github__}">Twitchify</a> Version: {__version__}</p>
                            <p>You can now close this page.</p>
                        </body>
                    </html>
                    '''
                return web.Response(
                    text=html,
                    content_type='text/html'
                )
            if query_params.get('error'):
                error_description = query_params.get('error_description')
                return web.Response(status=403, text=error_description.replace('+', ' '))
        return web.Response(status=403, text='')

    async def run_server(self) -> None:
        """Run the server."""
        runner = web.AppRunner(self._app)
        await runner.setup()
        uri = urllib.parse.urlparse(self.uri)
        site = web.TCPSite(runner, uri.hostname, uri.port)
        _logger.debug('Starting the authorization server.')
        await site.start()
        _logger.debug('Server is now running on %s', self.uri)
        await self._shutdown_event.wait()
        if self._code is not None:
            response: Token = await self._http.auth_code(code=self._code, redirect_uri=self.uri)
            if response is not None:
                self.access_token: str = response['access_token']
                self.refresh_token: str = response['refresh_token']
        _logger.debug('Shutting down the authorization server.')
        await runner.cleanup()
        await runner.shutdown()

    async def shutdown(self, query: web.Request.query) -> None:
        """
        Shutdown the server.

        :param query: The web request query.
        """
        _logger.debug('Shutting down the server app.')
        await self._app.shutdown()
        await self._app.cleanup()
        self._query = query
        self._shutdown_event.set()

    def get_code(self, verify: bool = False, port: int = 3000) -> str:
        """
        Get the authorization code.

        :param verify: Whether to force verification.
        :param port: The server port to use.
        """
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.get_event_loop()
        if verify:
            self._force_verify = verify
        if port:
            self._port = port
        loop.run_until_complete(self.run_server())
        if self._query.get('error'):
            error_description = self._query.get('error_description')
            raise AuthorizationError(message=error_description.replace('+', ' ') + '.')
        if self._query.get('code') is None:
            raise AuthorizationError(message='Failed to authorize.')
        return self._query.get('code')
