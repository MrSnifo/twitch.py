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

from .utils import setup_logging, Scopes
from .gateway import EventSubWebSocket
from .http import HTTPClient, Server
from .state import ConnectionState

import asyncio

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Any, List, Optional, Callable, Type
    from .types.http import ScopesType
    from .broadcaster import Broadcaster
    from types import TracebackType

import logging
_logger = logging.getLogger(__name__)

__all__ = ('Client',)


class Client:
    """
    Represents a Twitch client for interacting with the Twitch API and receiving events.

    Parameters
    ----------
    client_id: :class:`List`
        Your app's registered client ID.

    client_secret: Optional[:class:`str`]
        Your app's registered client secret. Required when generating a new access token
        if the user access token is not provided. It ensures manual authorization.

    cli: Optional[:class:`bool`]
        Whether to run the client in development mode using the Twitch CLI.
        For testing purposes during development. Defaults to ``False``.

    port: :class:`int`
        The port for the Twitch **CLI websocket** and **Event subscription API**.
        Defaults to ``8080``.
    """

    def __init__(self, client_id: str, client_secret: Optional[str] = None,
                 cli: Optional[bool] = False, port: int = 8080) -> None:
        self._client_id: str = client_id
        self._client_secret: Optional[str] = client_secret
        self._cli: Optional[bool] = cli
        self._port: int = port
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._http = HTTPClient(dispatcher=self.dispatch, client_id=client_id, secret_secret=client_secret)
        self._connection: ConnectionState = ConnectionState(dispatcher=self.dispatch,
                                                            http=self._http,
                                                            events=self._sub_events)

    async def __aenter__(self) -> 'Client':
        """
        Method to be called when entering the async with block.

        Returns
        -------
        Client
            The client instance itself.
        """
        return self

    async def __aexit__(self, exc_type: Optional[Type[BaseException]],
                        exc_value: Optional[BaseException],
                        traceback: Optional[TracebackType]) -> None:
        """
        Method to be called when exiting the async with block.

        This method performs the cleanup of the session used by the client.

        Parameters
        ----------
        exc_type: Optional[Type[BaseException]]
            The type of the exception raised, if any.

        exc_value: Optional[BaseException]
            The exception object raised, if any.

        traceback: Optional[TracebackType]
            The traceback associated with the exception, if any.

        Notes
        -----
        If an exception occurs within the context block, it will be passed to this method.
        The cleanup ensures that the session used by the client is closed properly.
        """
        if self._http.is_open:
            await self._http.close()

    @property
    def user(self) -> Optional[Broadcaster]:
        """
        Optional[:class:`.Broadcaster`]: Represents the authorized client.
        Default to ``None`` if not authorized yet.
        """
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
            await self.on_error(event_name, str(error), *args, **kwargs)

    def dispatch(self, event: str, /, *args: Any, **kwargs: Any) -> None:
        """
        Dispatch a specified event with the given arguments.
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
        """|coro|
        The default error handler provided by the client.

        This method is called when an uncaught exception occurs during event processing.

        Parameters
        ----------
        event_name: str
            The name of the event that raised the error.

        error: Exception
            The exception object representing the error.

        *args: Any
            Additional positional arguments that were passed to the event handler.

        **kwargs: Any
            Additional keyword arguments that were passed to the event handler.
        """
        _logger.exception('Ignoring error: %s from %s, args: %s kwargs: %s', error, event_name,
                          args, kwargs)

    def event(self, coro: Callable[..., Any], /) -> None:
        """
        A decorator that registers an event to listen to.

        Parameters
        ----------
        coro: Callable[..., Any]
            The coroutine function representing the event to listen to.

        Example
        --------
        .. code-block:: python3

            @client.event
            async def on_ready():
                print('Ready!')

        Raises
        ------
        TypeError
            If the passed is not a coroutine.
        """
        if not asyncio.iscoroutinefunction(coro):
            raise TypeError("The registered event must be a coroutine function")
        setattr(self, coro.__name__, coro)

    async def connect(self, access_token: str, *, refresh_token: Optional[str], reconnect: bool) -> None:
        """|coro|
        Establishes a WebSocket connection for EventSub and validates the access token.

        Parameters
        ----------
        access_token: Optional[:class:`str`]
            The User access token. If not provided, a web server will
            be opened for manual authentication.

        refresh_token: Optional[:class:`str`]
            A token used for obtaining new access tokens without requiring user re-authentication.
            Requires the app's client secret.

        reconnect: :class:`bool`
            Whether to attempt reconnecting on internet or Twitch failures.
            Defaults to ``False``.
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
        if self._cli:
            EventSub.cli = f'ws://localhost:{self._port}/ws'
            self._http.cli = f'http://localhost:{self._port}/eventsub/subscriptions'
        # Creating tasks.
        tasks: List[asyncio.Task] = [
            self._loop.create_task(self._http.refresher(expires_in=validation['expires_in']),
                                   name="Twitchify:Refresher"),
            self._loop.create_task(EventSub.connect(reconnect=reconnect), name="Twitchify:EventSub")
        ]
        self.dispatch('connect')
        await asyncio.gather(*tasks)

    async def start(self, access_token: Optional[str] = None, *, refresh_token: Optional[str] = None,
                    port: int = 8080,
                    reconnect: bool = True,
                    scopes: Optional[ScopesType] = None) -> None:
        """|coro|
        A shorthand coroutine for :meth:`connect`.

        .. note: If `token` is not provided, the bot will initiate a web server for manual authentication,
                 The `refresh_token` parameter will be automatically added by the authentication process,
                 and :meth:`on_auth` will be called.
        Parameters
        ----------
        access_token: Optional[:class:`str`]
            The User access token. If not provided, a web server will
            be opened for manual authentication.

        refresh_token: Optional[:class:`str`]
            A token used for obtaining new access tokens without requiring user re-authentication.
            Requires the app's client secret.

        port: :class:`int`
            The port for the Twitch **CLI websocket** and the **authentication web server**.
            Defaults to ``8080``.

        scopes: Optional[:class:`List`]
            A list of scopes required by the Twitch API to support your app's functionality.
            If `token` is `None`, the user will manually authenticate using these scopes.
            If not provided, the default value will be all available scopes.
            Defaults to all available scopes as specified in ``None``.

        reconnect: :class:`bool`
            Whether to attempt reconnecting on internet or Twitch failures.
            Defaults to ``False``.

        Raises
        ------
        TypeError
            If the client_secret is not provided and the user access token is not provided.
            In this case, it's not possible to generate a new access token, and the client
            cannot interact with the Twitch API without authentication.
            or
            Scope does not exist.
        """
        if access_token is None:
            if scopes is None:
                scopes = Scopes
            else:
                if not all(scope in Scopes for scope in scopes):
                    raise TypeError("One or more scopes do not exist.")
            if self._client_secret:
                # Authenticates with the Twitch API using OAuth 2.0 authorization code grant flow.
                async with Server(port=port) as server:
                    auth_url = server.url(client_id=self._client_id, scopes=scopes)
                    _logger.info('1. Create an app on the Twitch Developer Console:\n'
                                 '   - Go to https://dev.twitch.tv/console\n'
                                 '   - Sign in with your Twitch account\n'
                                 '   - Click on \'Applications\' in the top navigation\n'
                                 '   - Click on \'Register Your Application\'\n'
                                 '   - Fill in the required details for your app\n'
                                 '   - Set \'OAuth Redirect URLs\' to your redirect URI:\n'
                                 '     -> Redirect URI: %s\n'
                                 '   - Save your changes\n', server.uri)
                    _logger.info('2. Navigate to the following URL in your web browser:\n'
                                 '   -> Authorization URL: %s\n', auth_url)
                    code = await server.wait_for_code()
                    access_token, refresh_token = await self._http.auth_code(code=code,
                                                                             redirect_uri=server.uri)
                    await self.on_auth(access_token=access_token, refresh_token=refresh_token)
            else:
                raise TypeError('Missing Client Secret, Unable to authorize.')
        await self.connect(access_token=access_token, refresh_token=refresh_token, reconnect=reconnect)

    def run(self, access_token: Optional[str] = None, *, refresh_token: Optional[str] = None,
            port: int = 3000,
            reconnect: bool = True,
            scopes: Optional[ScopesType] = None,
            log_level: int = logging.INFO) -> None:
        """
        Start the client and handle the event loop.
        If you want more control over the event loop, use :meth:`start`.

        .. warning::
            This function must be the last function to call as it blocks
            the execution of anything after it.

        Parameters
        ----------
        access_token: Optional[:class:`str`]
            The User access token. If not provided, a web server will
            be opened for manual authorization.

        refresh_token: Optional[:class:`str`]
            A token used for obtaining new access tokens without requiring user re-authentication.
            Requires the app's client secret.

        port: :class:`int`
            The port for the **authorization web server**.
            Defaults to ``3000``.

        reconnect: :class:`bool`
            Whether to attempt reconnecting on internet or Twitch failures.
            Defaults to ``False``.

        scopes: Optional[:class:`List`]
            A list of scopes required by the Twitch API to support your app's functionality.
            If `token` is `None`, the user will manually authenticate using these scopes.
            If not provided, the default value will be all available scopes.
            Defaults to all available scopes as specified in ``None``.

        log_level: int
            The log level for the library's logger. Can be one of the following:
            - ``logging.ERROR`` (40): Errors that indicate a problem that needs attention.
            - ``logging.WARNING`` (30): Warnings that may not be critical but should be reviewed.
            - ``logging.INFO`` (20): General information about the client activity.
            - ``logging.DEBUG`` (10): Detailed debugging information for troubleshooting.
            Defaults to ``logging.INFO``.
        """
        setup_logging(level=log_level)

        async def starter():
            async with self:
                await self.start(access_token=access_token, refresh_token=refresh_token, scopes=scopes,
                                 port=port, reconnect=reconnect)
        try:
            asyncio.run(starter())
        except KeyboardInterrupt:
            return

    async def on_auth(self, access_token: str, refresh_token: str) -> None:
        """|coro|

        A coroutine to be called after successful manual authorization.

        Parameters
        ----------
        access_token: str
            The user access token received after manual authorization.

        refresh_token: str
            The refresh token received after manual authorization.

        Note
        ----
        Store these tokens securely for future use, avoiding the need for manual authorization each time.
        """
        pass
