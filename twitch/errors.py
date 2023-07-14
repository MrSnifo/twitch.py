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


class UnknownError(Exception):
    """
    Exception raised cause of an unknown error.
    """
    pass


class TwitchException(Exception):
    """
    Base exception class for Twitchify.
    """
    pass


class TwitchServerError(TwitchException):
    """
    Exception raised when an operation in the Client class fails.
    """

    def __init__(self):
        super().__init__('Twitch API server error.')


# ------------------------------------------
#              HTTP Exception
# ------------------------------------------

class HTTPException(TwitchException):
    """
    Exception raised when an HTTP request operation fails.
    """
    pass


class SessionClosed(HTTPException):
    """
    Exception raised when the session is not open.
    """
    pass


class BadRequest(HTTPException):
    """
    Exception raised when Twitch refuses the request.
    """

    def __init__(self, message: str = ''):
        super().__init__(message)


class Unauthorized(HTTPException):
    """
    Exception raised when the request is unauthorized.
    """

    def __init__(self, message: str = ''):
        super().__init__(message)


class Forbidden(HTTPException):
    """
    Exception raised when the request is Forbidden.
    """

    def __init__(self, message: str = ''):
        super().__init__(message)


# -------------------------------------------
#                  Websocket
# -------------------------------------------

class WebSocketError(HTTPException):
    """
    Exception raised when a websocket error occurs.
    """

    def __init__(self, message: str = ''):
        super().__init__(message)


class WebsocketClosed(WebSocketError):
    """
    Exception raised when the websocket connection is closed.
    """
    pass


class WebsocketUnused(WebSocketError):
    """
    Exception is raised when no subscription has been created within 10 seconds.
    """


class WsReconnect(WebSocketError):
    """
    Exception raised to indicate that WebSocket should reconnect to a new URL.
    """
    def __init__(self, url: str):
        super().__init__(url)


# -------------------------------------------
#              Client Exception
# -------------------------------------------

class ClientException(TwitchException):
    """
    Exception raised when a Client operation fails.
    """
    pass


class NotFound(ClientException):
    """
    Exception raised when the user does not exist.
    """

    def __init__(self, message: str = 'Unable to find the requested user.'):
        super().__init__(message)


# ------------------------------------------
#               Auth Exception
# ------------------------------------------
class AuthorizationError(ClientException):
    """
    Exception raised when access is denied.
    """

    def __init__(self, message: str):
        super().__init__(message)
