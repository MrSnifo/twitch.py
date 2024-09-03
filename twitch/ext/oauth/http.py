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

from twitch import __version__, __github__, errors, utils
from typing import TYPE_CHECKING
import aiohttp
import asyncio
import socket
import time

if TYPE_CHECKING:
    from typing import Any, List, Optional, ClassVar
    from twitch.types import users

import logging
_logger = logging.getLogger(__name__)

__all__ = ('HTTPClient',)


class HTTPClient:
    """Represents an asynchronous HTTP client for sending HTTP requests."""

    OAUTH2: ClassVar[str] = 'https://id.twitch.tv/oauth2/'

    def __init__(self, client_id: str, *, loop: Optional[asyncio.AbstractEventLoop] = None) -> None:
        self.__session: Optional[aiohttp.ClientSession] = None
        self.user_agent: str = f'twitch.py/{__version__} (GitHub: {__github__})'
        self.client_id: str = client_id
        self.loop: asyncio.AbstractEventLoop = loop

    async def close(self) -> None:
        """
        Closes the underlying session if it exists.
        """
        if self.__session is not None and not self.__session.closed:
            await self.__session.close()

    async def clear_session(self) -> None:
        """
        Clears the session and cancels any pending keep-alive tasks.
        """
        if self.__session and self.__session.closed:
            self.__session = None

    async def request(self, method: str, path: str, **kwargs: Any) -> Any:
        """
        Make an HTTP request with the provided route and keyword arguments.
        """
        if self.__session is None:
            connector = aiohttp.TCPConnector(limit=0, family=socket.AF_INET)
            self.__session = aiohttp.ClientSession(connector=connector)

        url = self.OAUTH2 + path
        kwargs['headers'] = {'Client-ID': self.client_id}

        for attempt in range(3):
            try:
                async with self.__session.request(method, url, **kwargs) as response:
                    _logger.debug('%s >> %s with %s has returned status code %s', method, url,
                                  kwargs.get('data'),
                                  response.status)
                    data = await utils.json_or_text(response)
                    if 300 > response.status >= 200:
                        _logger.debug('%s << %s has received %s', method, url, data)
                        return data
                    if response.status == 403:
                        raise errors.Forbidden(response, data)
                    elif response.status >= 500:
                        raise errors.TwitchServerError(response, data)
                    else:
                        raise errors.HTTPException(response, data)
            except OSError as e:
                if attempt < 2 and e.errno in (54, 10054):
                    await asyncio.sleep(1 + attempt * 2)
                    continue
                raise

    async def start_device_auth_flow(self, scopes: List[str]) -> users.DeviceAuthFlow:
        """
        Starts the device authorization flow.
        """
        scopes = list(dict.fromkeys(scopes))
        body = {
            'client_id': self.client_id,
            'scopes': ' '.join(scopes)
        }
        data = await self.request('POST', 'device', data=body)
        return data

    async def poll_for_token(self, device_code: str, expires_in: int, interval: int) -> users.OAuthRefreshToken:
        """
        Polls the Twitch API to check if the user has authorized the application.
        """
        start_time = time.time()
        while time.time() - start_time < (expires_in - 15):
            await asyncio.sleep(interval)
            try:
                data = await self.check_device_code(device_code=device_code)
                _logger.debug('Successfully authorized using device code flow.')
                return data
            except errors.HTTPException as error:
                if error.text in ['authorization_pending', 'slow_down']:
                    continue
                raise
        raise TimeoutError('Authorization expired.')

    async def check_device_code(self, device_code: str) -> Any:
        """
        Checks the device code to obtain the access token.
        """
        body = {
            'client_id': self.client_id,
            'device_code': device_code,
            'grant_type': 'urn:ietf:params:oauth:grant-type:device_code'
        }
        data = await self.request('POST', 'token', data=body,
                                  headers={'Content-Type': 'application/x-www-form-urlencoded'})
        return data

    async def revoke_token(self, token: str) -> None:
        """
        Revokes a token.
        """
        body = {
            'client_id': self.client_id,
            'token': token,
        }
        await self.request('POST', 'revoke', data=body)

