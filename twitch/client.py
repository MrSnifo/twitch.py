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

from .gateway import EventSubWebSocket
from .state import ConnectionState
from .utils import setup_logging
from .http import HTTPClient
from .channel import Channel
from .stream import Stream
from .auth import Auth

import asyncio

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Any, List, Optional, Callable
    from .types.scoopes import ScopesType
    from .broadcaster import Broadcaster

import logging
_logger = logging.getLogger(__name__)
__all__ = ('Client',)


class Client:
    """
    Represents a Twitch client for interacting with the Twitch API and receiving event
    notifications.

    :param client_id: Client id
    :param client_secret: Client secret needed to re-generate a new access token.
    """

    def __init__(self, client_id: str, client_secret: Optional[str] = None) -> None:
        setup_logging()
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._http = HTTPClient(dispatcher=self.dispatch, client_id=client_id, secret_secret=client_secret)
        self._auth = Auth(http=self._http, client_id=client_id)
        self._connection: ConnectionState = ConnectionState(dispatcher=self.dispatch,
                                                            http=self._http,
                                                            events=self._sub_events)

    @property
    def user(self) -> Broadcaster:
        """
        Retrieves the Broadcaster.

        :return: An instance of the Broadcaster class representing the user.
        """
        return self._connection.broadcaster

    async def get_channel(self) -> Channel:
        """
        Retrieves the channel associated with the broadcaster.

        :return: An instance of the Channel class representing the channel.
        """
        return await self._connection.broadcaster.get_channel()

    async def get_stream(self) -> Optional[Stream]:
        """
        Retrieves the stream of the broadcaster if currently live.

        :return: An instance of the Stream class representing the stream if live, otherwise None.
        """
        return await self._connection.broadcaster.get_stream()

    def auth(self, scopes: Optional[ScopesType] = None, verify: bool = False, port: int = 3000) -> Auth:
        """
        Authenticates with the Twitch API using OAuth 2.0 authorization code grant flow.

        :param scopes: Optional. The list of scopes to request authorization for.
        :param verify: Optional. Whether to force verification during the authorization process.
        :param port: Optional. The port to use for the local server during the authorization process.
        :return: An instance of the Auth class representing the authentication result.
        """
        if scopes:
            self._auth.scopes = scopes
        _logger.info('1. Create an app on the Twitch Developer Console:\n'
                     '   - Go to https://dev.twitch.tv/console\n'
                     '   - Sign in with your Twitch account\n'
                     '   - Click on \'Applications\' in the top navigation\n'
                     '   - Click on \'Register Your Application\'\n'
                     '   - Fill in the required details for your app\n'
                     '   - Set \'OAuth Redirect URLs\' to your redirect URI:\n'
                     '     -> Redirect URI: %s\n'
                     '   - Save your changes\n', self._auth.uri)
        _logger.info('2. Navigate to the following URL in your web browser:\n'
                     '   -> Authorization URL: %s\n', self._auth.url)
        self._auth.get_code(verify=verify, port=port)
        _logger.info('Successfully authorized with the app!\n')
        return self._auth

    @property
    def _sub_events(self) -> List[str]:
        """Retrieve the names of the subscribed events."""
        return [attr.replace('on_', '', 1) for attr in dir(self) if attr.startswith('on_')]

    async def _run_event(self, coro: Callable[..., Any], event_name: str, *args: Any, **kwargs: Any) -> None:
        """
        Execute the specified event coroutine with the given arguments.
        """
        try:
            await coro(*args, **kwargs)
        except asyncio.CancelledError:
            pass
        except Exception as error:
            await self.on_error(event_name, str(error), *args, **kwargs)

    def dispatch(self, event: str, /, *args: Any, **kwargs: Any) -> None:
        """
        Dispatch the specified event with the given arguments.
        """
        _logger.debug('Dispatching event %s', event)
        method = "on_" + event
        try:
            coro = getattr(self, method)
            if coro is not None and asyncio.iscoroutinefunction(coro):
                wrapped = self._run_event(coro, method, *args, **kwargs)
                # Schedule the task
                self._loop.create_task(wrapped, name=f'Twitchify:{method}')
        except AttributeError as error:
            _logger.error('Event: %s Error: %s', event, error)

    @staticmethod
    async def on_error(event_name: str, error: str, /, *args: Any, **kwargs: Any) -> None:
        """
        The default error handler for events.
        """
        _logger.exception('Ignoring error: %s from %s, args: %s kwargs: %s', error, event_name,
                          args, kwargs)

    def event(self, coro: Callable[..., Any], /) -> None:
        """
        Decorator to register an event coroutine.
        """
        if not asyncio.iscoroutinefunction(coro):
            raise TypeError("The registered event must be a coroutine function")
        setattr(self, coro.__name__, coro)

    async def connect(self, *, access_token: str, refresh_token: Optional[str], reconnect: bool) -> None:

        """
        Establishes a connection to Twitch services.
        """
        # Setup loop
        if self._loop is None:
            self._loop = asyncio.get_running_loop()

        # Validating the access key and opening a new session.
        validation = await self._http.open_session(token=access_token,
                                                   refresh_token=refresh_token)
        # Retrieving the client.
        await self._connection.get_client()
        # Creating an EventSub websocket.
        EventSub = EventSubWebSocket(http=self._http, connection=self._connection,
                                     loop=self._loop,
                                     events=self._sub_events)
        # Creating tasks.
        tasks = [
            self._loop.create_task(self._http.refresher(expires_in=validation['expires_in']),
                                   name="Twitchify:Refresher"),
            self._loop.create_task(EventSub.connect(reconnect=reconnect), name="Twitchify:EventSub")
        ]
        self.dispatch('connect')

        await asyncio.gather(*tasks)

    async def start(self, access_token: str, refresh_token: Optional[str] = None,
                    reconnect: bool = True) -> None:
        """
        Starts the Twitch client by establishing a connection and initiating the event loop.
        """
        try:
            await self.connect(access_token=access_token, refresh_token=refresh_token, reconnect=reconnect)
        except Exception as error:

            if self._http is not None and self._http.is_open:
                await self._http.close()
            raise error
        finally:
            pass

    def run(self, access_token: str, refresh_token: Optional[str] = None, reconnect: bool = True) -> None:
        """
        Runs the Twitch client without establishing a connection and initiating the event loop.
        """

        async def runner():
            await self.start(access_token=access_token, refresh_token=refresh_token, reconnect=reconnect)

        try:
            self._loop = asyncio.get_running_loop()
        except RuntimeError:
            self._loop = asyncio.get_event_loop()
        if self._loop.is_running():
            # Already running in an event loop, so directly run the main function.
            asyncio.run(runner())
        else:
            # No running event loop, so run the event loop and then run the main function.
            self._loop.run_until_complete(runner())
