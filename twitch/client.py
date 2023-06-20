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

# Core
from .gateway import EventSubWebSocket
from .state import ConnectionState
from .utils import setup_logging
from .http import HTTPClient

# Libraries
import asyncio

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Any, List, Optional, Callable
    from .user import Broadcaster

import logging
_logger = logging.getLogger(__name__)


class Client:
    """
    Represents a Twitch client for interacting with the Twitch API and receiving event notifications.

    :param client_id: The client ID associated with the Twitch application.
    :param client_secret: The client secret for the Twitch application, if applicable.
    """

    def __init__(self, client_id: str, client_secret: Optional[str] = None) -> None:
        self.client_secret = client_secret
        self.client_id = client_id
        self.loop: Optional[asyncio.AbstractEventLoop] = None
        self._connection: ConnectionState = ConnectionState(dispatcher=self.dispatch)
        self._http = HTTPClient(connection=self._connection, client_id=self.client_id, client_secret=self.client_secret)

    @property
    def user(self) -> Optional[Broadcaster]:
        return self._connection.broadcaster

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
            try:
                await self.on_error(str(error), event_name, args, kwargs)
            except asyncio.CancelledError:
                pass

    def dispatch(self, event: str, /, *args: Any, **kwargs: Any) -> asyncio.Task:
        """
        Dispatch the specified event with the given arguments.
        """
        _logger.debug('Dispatching event %s', event)
        event_name = "on_" + event
        try:
            coro = self.__getattribute__(event_name)
        except AttributeError:
            pass
        else:
            wrapped = self._run_event(coro, event_name, *args, **kwargs)
            # Schedules the task
            return self.loop.create_task(wrapped, name=f'Twitchify:{event_name}')

    @staticmethod
    async def on_error(event_name: str, error: str, /, *args: Any, **kwargs: Any) -> None:
        """
        The default error handler for events.

        :param event_name: The name of the event where the error occurred.
        :param error: The error message.
        :param args: Variable length argument list passed to the event when the error occurred.
        :param kwargs: Arbitrary keyword arguments passed to the event when the error occurred.
        """
        _logger.exception('Ignoring error: %s from %s, args: %s kwargs: %s', error, event_name, args, kwargs)

    def event(self, coro: Callable[..., Any], /):
        """
        Decorator to register an event coroutine.

        :param coro: The event coroutine to be registered.
        :raises TypeError: If the registered event is not a coroutine function.
        """
        if not asyncio.iscoroutinefunction(coro):
            raise TypeError("The registered event must be a coroutine function")

        setattr(self, coro.__name__, coro)

    async def connect(self, access_token: str, refresh_token: Optional[str]) -> None:
        """
        Establishes a connection to Twitch services.

        :param access_token: The access token for authentication.
        :param refresh_token: The refresh token for refreshing the access token, if applicable.
        """
        # Setup logger
        setup_logging()
        if self.loop is None:
            self.loop = asyncio.get_running_loop()
        # Validating the access key and opening a new session.
        validation = await self._http.open_session(access_token=access_token, refresh_token=refresh_token)
        # Retrieving the client.
        self._connection.broadcaster = await self._http.get_client()
        # Creating an EventSub websocket.
        EventSub = EventSubWebSocket(http=self._http, connection=self._connection,
                                     loop=self.loop,
                                     events=self._sub_events)
        # Creating tasks.
        tasks = [
            self.loop.create_task(self._http.Refresher(expires_in=validation['expires_in']),
                                  name="Twitchify:Refresher")
        ]
        self.dispatch('connect')
        # Makes sure that there are events to subscribe to.
        if len(EventSub.subscriptions) >= 1:
            tasks.append(self.loop.create_task(EventSub.connect(), name="Twitchify:EventSub"))

        await asyncio.gather(*tasks)

    async def start(self, access_token: str, refresh_token: Optional[str] = None) -> None:
        """
        Starts the Twitch client by establishing a connection and initiating the event loop.

        :param access_token: The access token for authentication.
        :param refresh_token: The refresh token for refreshing the access token, if applicable.
        """
        try:
            await self.connect(access_token, refresh_token)
        # Automatically close the HTTP session when an error occurs.
        except Exception as error:
            # Checks if the _http session is open.
            if self._http is not None and self._http.is_open:
                await self._http.close()
            raise error

    def run(self, access_token: str, refresh_token: Optional[str] = None):
        """
       Runs the Twitch client by establishing a connection and initiating the event loop.

       :param access_token: The access token for authentication.
       :param refresh_token: The refresh token for refreshing the access token, if applicable.
       """
        async def runner():
            await self.start(access_token, refresh_token)
        asyncio.run(runner())
