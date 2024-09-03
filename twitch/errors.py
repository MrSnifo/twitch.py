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

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Dict, Optional, Any, Union
    from aiohttp import ClientWebSocketResponse
    from aiohttp import ClientResponse


__all__ = ('TwitchException',
           'ClientException',
           'HTTPException',
           'TwitchServerError',
           'Forbidden',
           'NotFound',
           'AuthFailure',
           'ConnectionClosed',
           'UnregisteredUser')


class TwitchException(Exception):
    """
    Base exception for twitch.py.
    """
    pass


class ClientException(TwitchException):
    """
    Exception raised when an operation in the Client class fails.
    """
    pass


class HTTPException(TwitchException):
    """Exception raised for failed HTTP requests."""

    def __init__(self, response: ClientResponse, message: Optional[Union[str, Dict[str, Any]]]):
        self.response = response
        self.status = response.status if hasattr(response, 'status') else 0

        if isinstance(message, dict):
            self.code = message.get('status', 0)
            self.text = message.get('message', '')
        else:
            self.text = message or ''
            self.code = 0
        super().__init__(f'{self.response.reason} (error code: {self.code}): {self.text}')


class TwitchServerError(HTTPException):
    """Exception raised when a 500 range status code occurs."""
    pass


class Forbidden(HTTPException):
    """Exception raised when status code 403 occurs."""
    pass


class NotFound(HTTPException):
    """Exception raised when status code 404 occurs."""
    pass


class AuthFailure(ClientException):
    """Exception raised when authentication fails, typically due to invalid credentials."""
    pass


class UnregisteredUser(ClientException):
    """Exception raised when the user is UnregisteredUse."""
    pass


class ConnectionClosed(ClientException):
    """
    Exception raised when the WebSocket connection is closed unexpectedly.
    """

    def __init__(self, socket: ClientWebSocketResponse, *, code: Optional[int] = None):
        self.code: int = code or socket.close_code or -1
        self.reason: str = ''
        super().__init__(f'WebSocket closed with {self.code} close code.')
