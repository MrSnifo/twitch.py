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

from .gateway import EventSubWebSocket, ReconnectWebSocket
from .utils import setup_logging, ExponentialBackoff
from .errors import HTTPException, ConnectionClosed
from .state import ConnectionState
from typing import TYPE_CHECKING
from .http import HTTPClient
import datetime
import asyncio
import aiohttp

if TYPE_CHECKING:
    from typing import Optional, Type, Self, Callable, Any, List, Tuple, Dict, AsyncGenerator, Literal
    from .types import chat, channels, search, streams, bits, analytics, users
    from .user import User, ClientUser
    from .channel import ClientChannel
    from types import TracebackType

import logging
_logger = logging.getLogger(__name__)

__all__ = ('Client',)


class Client:
    """
    A client for interacting with the Twitch API.

    The Client class enables interaction with the Twitch API. After authentication,
    it manages HTTP requests and WebSocket connections for real-time updates,
    providing access to a broad range of Helix API endpoints.

    Parameters
    ----------
    client_id: str
        The client ID used for authentication with the Twitch API.
    client_secret: Optional[str]
        The client secret used for authentication with the Twitch API. Default is None.
    **options:
        Additional configuration options:

        - cli: [bool][bool]

            Flag indicating if CLI mode is enabled.

            **Default**: `False`

            ___

        - cli_port: [int][]

            The port number used for CLI mode.

            **Default**: `8080`
            ___

        - socket_debug: [False][bool]

            Flag indicating if raw WebSocket messages should be dispatched for debugging purposes.
            If enabled, raw WebSocket messages are dispatched to the on_socket_raw_receive.

            **Default**: `False`
            ___

        - proxy: [Optional][typing.Optional][[str][str]]

            The proxy URL to use for HTTP requests.

            **Default**: `None`
            ___

        - proxy_auth: [Optional][typing.Optional][aiohttp.BasicAuth]

            Authentication details for the proxy, if required.

            **Default**: `None`
    """

    def __init__(self, client_id: str, client_secret: Optional[str] = None, **options) -> None:
        cli: bool = options.get('cli', False)
        cli_port: int = options.get('cli_port', 8080)
        _socket_debug: bool = options.get('socket_debug', False)
        proxy: Optional[str] = options.pop('proxy', None)
        proxy_auth: Optional[aiohttp.BasicAuth] = options.pop('proxy_auth', None)

        self.client_id: str = client_id
        self.client_secret: str = client_secret

        self.loop: Optional[asyncio.AbstractEventLoop] = None
        self.http: HTTPClient = HTTPClient(client_id, client_secret,
                                           loop=self.loop,
                                           proxy=proxy,
                                           proxy_auth=proxy_auth,
                                           cli=cli,
                                           cli_port=cli_port)

        self._connection: ConnectionState = ConnectionState(
            dispatcher=self.dispatch,
            custom_dispatch=self.custom_dispatch,
            http=self.http,
            socket_debug=_socket_debug
        )
        self._closing_task: Optional[asyncio.Task] = None
        self.ws: Optional[EventSubWebSocket] = None

    @property
    def user(self) -> Optional[ClientUser]:
        """
        Retrieve the current user associated with the client.

        Returns
        -------
        Optional[ClientUser]
            The current user if authenticated, otherwise None.
        """
        return self._connection.user

    @property
    def channel(self) -> Optional[ClientChannel]:
        """
        Retrieve the channel of the current user associated with the client.

        Returns
        -------
        Optional[ClientChannel]
            The channel of the current user if authenticated, otherwise None.
        """
        return self._connection.user.channel if self._connection.user is not None else None

    @property
    def total_subscription_cost(self) -> Optional[int]:
        """
        Retrieve the total cost of all active subscriptions for the current user.

        Returns
        -------
        Optional[int]
            The total cost of all active subscriptions if the user is authenticated, otherwise None.
        """
        return self._connection.total_cost

    @property
    def max_subscription_cost(self) -> Optional[int]:
        """
        Retrieve the maximum allowed total cost for all subscriptions.

        Returns
        -------
        Optional[int]
            The maximum allowed total cost for all subscriptions if the user is authenticated, otherwise None.
        """
        return self._connection.max_total_cost

    async def close(self) -> None:
        """
        Closes the connection to the Twitch API.

        This method ensures that all connections, including WebSocket and HTTP connections,
        are properly closed. If a closing task is already running, it waits for it to complete.

        If WebSocket is open, it is closed with a normal closure code (1000). After closing
        the WebSocket, it clears the connection state and closes the HTTP client.
        """
        if self._closing_task:
            return await self._closing_task

        async def _close():
            if self.ws is not None and self.ws.is_open:
                await self.ws.close(code=1000)

            self.clear()
            await self.http.close()
            self.loop = None

        self._closing_task = asyncio.create_task(_close())
        await self._closing_task

    def clear(self) -> None:
        """
        Clears the connection state and resets the closing task.

        This method is used to reset the connection state and prepare the client for a fresh
        start or clean up after closing the connection.
        """
        self._connection.clear()
        self._closing_task = None

    def is_closed(self) -> bool:
        """
        Check if the client is currently closing or closed.

        Returns
        -------
        bool
            True if the client is in the process of closing or has been closed, otherwise False.
        """
        return self._closing_task is not None

    async def __aenter__(self) -> Self:
        """
        Asynchronous context manager entry method.

        Returns
        -------
        Self
            The current instance of the client, allowing it to be used within an async context manager.
        """
        return self

    async def __aexit__(self, exc_type: Optional[Type[BaseException]],
                        exc_value: Optional[BaseException],
                        traceback: Optional[TracebackType]) -> None:
        """
        Asynchronous context manager exit method.

        Closes the HTTP client connection when exiting the async context manager.

        Parameters
        ----------
        exc_type: Optional[Type[BaseException]]
            The type of the exception raised, if any.
        exc_value: Optional[BaseException]
            The exception instance, if any.
        traceback: Optional[TracebackType]
            The traceback object, if any.
        """
        if self._closing_task:
            await self._closing_task
        else:
            await self.close()

    async def wait_until_ready(self) -> None:
        """
        Wait until the client is ready.
        """
        if self._connection.ready is None:
            raise RuntimeError(
                'Client not initialized. Ensure authorization or context manager is used before this call.'
            )
        await self._connection.ready.wait()

    async def _async_loop(self) -> None:
        # Starts the asynchronous loop for managing client operations.
        loop = asyncio.get_running_loop()
        self.loop = loop
        self.http.loop = loop

    async def setup_hook(self) -> None:
        """
        Perform additional setup before the client is ready.

        ???+ Warning
            Do not use `wait_until_ready()` within this method as it may cause
            it to freeze.

        You can configure or set up additional extensions or services as required.
        """
        pass

    @staticmethod
    async def on_error(event_name: str, error: Exception, /, *args: Any, **kwargs: Any) -> None:
        """
        Handle errors occurring during event dispatch.

        This static method logs an exception that occurred during the processing of an event.

        Parameters
        ----------
        event_name: str
            The name of the event that caused the error.
        error: Exception
            The exception that was raised.
        *args: Any
            Positional arguments passed to the event.
        **kwargs: Any
            Keyword arguments passed to the event.
        """
        _logger.exception('Ignoring error: %s from %s, args: %s kwargs: %s', error, event_name,
                          args, kwargs)

    async def _run_event(self, coro: Callable[..., Any], event_name: str, *args: Any, **kwargs: Any) -> None:
        # Run an event coroutine and handle exceptions.
        try:
            await coro(*args, **kwargs)
        except asyncio.CancelledError:
            pass
        except Exception as error:
            await self.on_error(event_name, error, *args, **kwargs)

    def custom_dispatch(self, event: str, coro: Callable[..., Any], /, *args: Any, **kwargs: Any) -> None:
        # Dispatch a custom event with a coroutine callback.
        try:
            if asyncio.iscoroutinefunction(coro):
                _logger.debug('Dispatching custom event %s', event)
                wrapped = self._run_event(coro, event, *args, **kwargs)
                # Schedule the task
                self.loop.create_task(wrapped, name=f'twitch:custom:{event}')
        except AttributeError:
            pass
        except Exception as error:
            _logger.error('Event: %s Error: %s', event, error)

    def dispatch(self, event: str, /, *args: Any, **kwargs: Any) -> None:
        # Dispatch a specified event with a coroutine callback.
        method = 'on_' + event
        try:
            coro = getattr(self, method)
            if coro is not None and asyncio.iscoroutinefunction(coro):
                _logger.debug('Dispatching event %s', event)
                wrapped = self._run_event(coro, method, *args, **kwargs)
                # Schedule the task
                self.loop.create_task(wrapped, name=f'twitch:{method}')
        except AttributeError:
            pass
        except Exception as error:
            _logger.error('Event: %s Error: %s', event, error)

    def event(self, coro: Callable[..., Any], /) -> None:
        """
        Register a coroutine function as an event handler.

        This method assigns the given coroutine function to be used as an event handler with the same
        name as the coroutine function.

        Parameters
        ----------
        coro: Callable[..., Any]
            The coroutine function to register as an event handler.

        Example
        -------
        ```py
        @client.event
        async def on_ready():
            print('Ready!')
        ```
        """
        if not asyncio.iscoroutinefunction(coro):
            raise TypeError('The registered event must be a coroutine function')
        setattr(self, coro.__name__, coro)

    async def add_custom_event(self,
                               name: str,
                               /,
                               user: User,
                               callback: Callable[..., Any],
                               *,
                               options: Optional[Dict[str, Any]] = None
                               ) -> None:
        """
        Add a custom event for a user.

        This method registers a callback function for a custom event and user.

        ???+ Warning
             You must be at least a moderator on their channel to subscribe to events on behalf of other users.

        Parameters
        ----------
        name: str
            The name of the event to subscribe to.
        user: User
            The user for whom the subscription is being created.
        callback: Callable[..., Any]
            The coroutine function to call when the event occurs.
        options: Optional[Dict[str, Any]]
            Custom event conditions.

        Example
        --------
        ```py
        async def on_yonk(data: eventsub.chat.MessageEvent):
            print(data)

        async def on_random_channel_message(data: eventsub.chat.MessageEvent):
            print(data)

        @client.event
        async def on_ready():
            user = await client.get_user('snifo')
            await client.add_custom_event('on_chat_message', user, on_random_channel_message)

            # Options not required, but sometimes we want to listen to a specific reward.
            await client.add_custom_event('on_points_reward_redemption_add', user, on_yonk, options={'reward_id': '1'})
        ```
        """
        if not asyncio.iscoroutinefunction(callback):
            raise TypeError('The registered custom event must be a coroutine function')

        if not name.startswith('on_'):
            raise TypeError('Event name must start with "on_" to be recognized as a valid custom event.')

        await self._connection.create_subscription(user.id,
                                                   name.replace('on_', '', 1),
                                                   self.ws.session_id,
                                                   callbacks=[callback],
                                                   condition_options=options)

    async def remove_custom_event(self, name: str, /, user: User) -> None:
        """
        Remove a custom event for a user.

        This method unsubscribes a user from a custom event.

        Parameters
        ----------
        name: str
            The name of the event to unsubscribe from.
        user: User
            The user whose subscription is being removed.
        """

        if not name.startswith('on_'):
            raise TypeError('Event name must start with "on_" to be recognized as a valid custom event.')

        await self._connection.remove_subscription(user.id, name.replace('on_', '', 1))

    async def authorize(self, access_token: str, refresh_token: Optional[str] = None) -> None:
        """
        Authorize the client with the given access and optionally refresh token.

        This method initializes the event loop if it's not already running,
        then calls the HTTP clients authorize method to authenticate with
        the Twitch API. After successful authorization, it initializes the
        client connection state with the user ID.

        Parameters
        ----------
        access_token: str
            The OAuth2 access token used for authentication.
        refresh_token: Optional[str], default=None
            The OAuth2 refresh token used to obtain a new access token if needed.
        """
        if self.loop is None:
            await self._async_loop()
        self._connection.ready = asyncio.Event()
        data: users.OAuthToken = await self.http.initialize_authorization(access_token, refresh_token)
        await self._connection.initialize_client(user_id=data['user_id'])
        await self.setup_hook()

    async def connect(self, *, reconnect: bool = True) -> None:
        """
        Establish a WebSocket connection to the Twitch API and handle events.

        This method tries to connect to the Twitch WebSocket server and handle
        incoming events. If the WebSocket connection is closed or errors occur,
        it handles reconnections based on the `reconnect` flag. It also logs
        connection errors and attempts to reconnect if necessary.

        Parameters
        ----------
        reconnect: bool
            Indicates whether to attempt reconnection if the WebSocket connection is lost.
        """
        kwargs: Dict[str, Any] = {'resume': False, 'initial': True}

        backoff = ExponentialBackoff()

        while not self.is_closed():
            try:
                websocket = EventSubWebSocket.initialize_websocket(self, self._connection, **kwargs)
                self.ws = await asyncio.wait_for(websocket, timeout=60.0)
                kwargs['initial'] = False
                while True:
                    await self.ws.poll_handle_dispatch()
            except ReconnectWebSocket as exc:
                _logger.debug('Websocket is reconnecting to %s', exc.url)
                kwargs['gateway'] = exc.url
                kwargs['resume'] = True

            except (OSError, HTTPException, ConnectionClosed, asyncio.TimeoutError, aiohttp.ClientError) as exc:
                self._connection.ws_disconnect()
                if not reconnect:
                    await self.close()
                    if isinstance(exc, ConnectionClosed) and exc.code == 1000:
                        return
                    raise

                if self.is_closed():
                    return

                delay = backoff.get_delay()
                _logger.exception('Attempting a reconnect in %d seconds.', delay)
                await asyncio.sleep(delay)
                kwargs['initial'] = False
                continue

    async def start(self, access_token: str, refresh_token: Optional[str] = None, *, reconnect: bool = True) -> None:
        """
        Start the client by authorizing and connecting to the Twitch API.

        This method authorizes the client with the provided access token and
        optionally refresh token. It then establishes a WebSocket connection
        to the Twitch API and starts handling events. It raises errors if the
        access token or refresh token is missing based on the client configuration.

        Parameters
        ----------
        access_token: str
            The OAuth2 access token used for authentication.
        refresh_token: Optional[str]
            The OAuth2 refresh token used to obtain a new access token if needed.
        reconnect: bool
            Indicates whether to attempt reconnection if the WebSocket connection is lost.

        Raises
        ------
        TypeError
            If the access token or refresh token is missing or if the client secret is not provided when needed.
        """
        if isinstance(self, Client) and access_token is None:
            if refresh_token and not self.client_secret:
                raise TypeError('Missing client secret.')

            if not refresh_token:
                raise TypeError('Missing client access token or refresh token.')
        await self.authorize(access_token, refresh_token)
        await self.connect(reconnect=reconnect)

    def run(self,
            access_token: Optional[str] = None,
            refresh_token: Optional[str] = None,
            *,
            reconnect: bool = True,
            log_handler: Optional[logging.Handler] = None,
            log_level: Optional[int] = None,
            root_logger: bool = False) -> None:
        """
        Start the client and run it until interrupted.

        !!! danger
            This function must be the last function to call as it blocks
            the execution of anything after it.

        This method sets up logging, initializes the client, and starts the main
        asynchronous process. The client will run and handle events until the
        process is interrupted (e.g., by a KeyboardInterrupt). The logging setup
        is customizable via parameters.

        Parameters
        ----------
        access_token: Optional[str]
            The OAuth2 access token used for authentication. If None, the client
            will need to obtain it from another source.
        refresh_token: Optional[str]
            The OAuth2 refresh token used to obtain a new access token if needed.
            If None, the client will need to obtain it from another source.
        reconnect: bool
            Indicates whether to attempt reconnection if the WebSocket connection is lost.
        log_handler: Optional[logging.Handler]
            A logging handler to be used for logging output. If None, a default handler will be set up.
        log_level: Optional[int]
            The logging level to be used. If None, a default level will be used.
        root_logger: bool
            If True, the logging configuration will apply to the root logger. Otherwise, it applies to a new logger.
        """
        if log_handler is None:
            setup_logging(handler=log_handler, level=log_level, root=root_logger)

        async def runner() -> None:
            """
            Inner function to run the main process asynchronously.
            """
            async with self:
                await self.start(access_token, refresh_token, reconnect=reconnect)

        try:
            asyncio.run(runner())
        except KeyboardInterrupt:
            return

    async def get_user(self, name: str) -> Optional[User]:
        """
        Retrieve a user by their login name.

        Parameters
        ----------
        name: str
            The login name of the user to retrieve.

        Returns
        -------
        Optional[User]
            The User object if found; otherwise, None.
        """
        data: List[User] = await self._connection.get_users(user_logins=[name])
        return data[0] if len(data) != 0 else None

    def get_user_by_id(self, __id: str, /) -> User:
        """
        Retrieve a user by their ID.

        ???+ note
            This method directly creates a User object with the provided ID, making it faster
            as it avoids an additional API request to retrieve the user ID.

        Parameters
        ----------
        __id: str
            The ID of the user to retrieve.

        Returns
        -------
        User
            The User object initialized with the given ID.
        """
        return self._connection.get_user(__id)

    async def get_users(self,
                        names: Optional[List[str]] = None,
                        ids: Optional[List[str]] = None) -> List[User]:
        """
        Retrieve multiple users by their names or IDs.

        ???+ note
            Using IDs is efficient as it avoids extra requests. If names are provided,
            it makes a single request to fetch all users by name.

        Parameters
        ----------
        names: Optional[List[str]]
            A list of user login names to retrieve.
        ids: Optional[List[str]]
            A list of user IDs to retrieve.

        Returns
        -------
        List[User]
            A list of User objects corresponding to the provided names or IDs.
        """
        data: List[User] = await self._connection.get_users(ids, names)
        return data

    async def get_users_chat_color(self, __users: List[User], /) -> List[chat.UserChatColor]:
        """
        Retrieve chat color information for a list of users.

        Parameters
        ----------
        __users: List[User]
            A list of User objects for which to retrieve chat color settings.

        Returns
        -------
        List[chat.UserChatColor]
            A list of dictionaries where each dictionary contains users chat color settings.
        """
        data: List[chat.UserChatColor] = await self._connection.get_users_chat_color(__users)
        return data

    async def get_team(self, name: str) -> channels.Team:
        """
        Retrieve a team by its name.

        Parameters
        ----------
        name: str
            The name of the team to retrieve.

        Returns
        -------
        channels.Team
            A dictionary representing the team's information.
        """
        data: Optional[channels.Team] = await self._connection.get_team_info(team_name=name)
        return data

    async def get_team_by_id(self, __id: str, /) -> channels.Team:
        """
        Retrieve a team by its ID.

        Parameters
        ----------
        __id: str
            The ID of the team to retrieve.

        Returns
        -------
        Optional[channels.Team]
            A dictionary representing the team's information.
        """
        data: Optional[channels.Team] = await self._connection.get_team_info(team_id=__id)
        return data

    async def get_global_emotes(self) -> Tuple[List[chat.Emote], str]:
        """
        Retrieve global emotes and the template URL.

        Returns
        -------
        Tuple[List[chat.Emote], str]
            A tuple containing a list of dictionaries representing global emotes and a template URL string.
        """
        data: Tuple[List[chat.Emote], str] = await self._connection.get_global_emotes()
        return data

    async def get_emote_sets(self, emote_set_ids: List[str]) -> Tuple[List[chat.Emote], str]:
        """
        Retrieve emotes for specific emote sets.

        Parameters
        ----------
        emote_set_ids: List[str]
            A list of emote set IDs to retrieve emotes for.

        Returns
        -------
        Tuple[List[chat.Emote], str]
            A tuple containing a list of dictionaries representing emotes and a template URL string.
        """
        data: Tuple[List[chat.Emote], str] = await self._connection.get_emote_sets(emote_set_ids)
        return data

    async def get_global_chat_badges(self) -> List[chat.Badge]:
        """
        Retrieve global chat badges.

        Returns
        -------
        List[chat.Badge]
            A list of dictionaries representing global chat badges.
        """
        data: List[chat.Badge] = await self._connection.get_global_chat_badges()
        return data

    async def fetch_channels_search(self,
                                    query: str,
                                    live_only: bool = False,
                                    first: int = 100) -> AsyncGenerator[List[search.ChannelSearch], None]:
        """
        Search for channels.

        Parameters
        ----------
        query: str
            The search query.
        live_only: bool
            Whether to return only live channels, by default False.
        first: int
            The maximum number of results to retrieve, by default 100.

        Yields
        ------
        AsyncGenerator[List[search.ChannelSearch], None]
            A list of dictionaries representing channels matching the search query.
        """
        async for result in self._connection.fetch_channels_search(query, live_only, first):
            yield result

    async def fetch_streams(self,
                            user_logins: Optional[List[str]] = None,
                            user_ids: Optional[List[str]] = None,
                            category_ids: Optional[List[str]] = None,
                            stream_type: Literal['all', 'live'] = 'all',
                            language: Optional[str] = None,
                            first: int = 100) -> AsyncGenerator[List[streams.StreamInfo], None]:
        """
        Fetch streams based on various filters.

        Parameters
        ----------
        user_logins: Optional[List[str]]
            A list of user logins to filter streams by, by default None.
        user_ids: Optional[List[str]]
            A list of user IDs to filter streams by, by default None.
        category_ids: Optional[List[str]]
            A list of category IDs to filter streams by, by default None.
        stream_type: Literal['all', 'live']
            The type of streams to retrieve, by default 'all'.
        language: Optional[str]
            The language to filter streams by, by default None.
        first: int
            The maximum number of results to retrieve, by default 100.

        Yields
        ------
        AsyncGenerator[List[streams.Stream], None]
            A list of dictionaries representing streams matching the filters.
        """
        async for result in self._connection.fetch_streams(user_logins,
                                                           user_ids,
                                                           category_ids,
                                                           stream_type,
                                                           language,
                                                           first):
            yield result

    async def fetch_videos_by_ids(self,
                                  video_ids: List[str],
                                  language: Optional[str] = None,
                                  period: Optional[Literal['all', 'day', 'month', 'week']] = None,
                                  sort: Optional[Literal['time', 'trending', 'views']] = None,
                                  video_type: Optional[Literal['all', 'archive', 'highlight', 'upload']] = None,
                                  first: Optional[int] = 100) -> AsyncGenerator[List[channels.Video], None]:
        """
        Fetch videos by their IDs.

        Parameters
        ----------
        video_ids: List[str]
            A list of video IDs to retrieve.
        language: Optional[str]
            The language to filter videos by, by default None.
        period: Optional[Literal['all', 'day', 'month', 'week']]
            The period to filter videos by, by default None.
        sort: Optional[Literal['time', 'trending', 'views']]
            The sorting order for the videos, by default None.
        video_type: Optional[Literal['all', 'archive', 'highlight', 'upload']]
            The type of videos to retrieve, by default None.
        first: Optional[int]
            The maximum number of results to retrieve, by default 100.

        Yields
        ------
        AsyncGenerator[List[channels.Video], None]
            A list of dictionaries representing videos matching the filters.
        """
        async for result in self._connection.fetch_videos(None,
                                                          video_ids,
                                                          language,
                                                          period,
                                                          sort,
                                                          video_type,
                                                          first):
            yield result

    async def fetch_videos_by_category(self,
                                       category_id: str,
                                       language: Optional[str] = None,
                                       period: Optional[Literal['all', 'day', 'month', 'week']] = None,
                                       sort: Optional[Literal['time', 'trending', 'views']] = None,
                                       video_type: Optional[Literal['all', 'archive', 'highlight', 'upload']] = None,
                                       first: Optional[int] = 100) -> AsyncGenerator[List[channels.Video], None]:
        """
        Fetch videos by category ID.

        Parameters
        ----------
        category_id: str
            The ID of the category to retrieve videos from.
        language: Optional[str]
            The language to filter videos by, by default None.
        period: Optional[Literal['all', 'day', 'month', 'week']]
            The period to filter videos by, by default None.
        sort: Optional[Literal['time', 'trending', 'views']]
            The sorting order for the videos, by default None.
        video_type: Optional[Literal['all', 'archive', 'highlight', 'upload']]
            The type of videos to retrieve, by default None.
        first: Optional[int]
            The maximum number of results to retrieve, by default 100.

        Yields
        ------
        AsyncGenerator[List[channels.Video], None]
            A list of dictionaries representing videos matching the filters.
        """
        async for result in self._connection.fetch_videos(category_id,
                                                          None,
                                                          language,
                                                          period,
                                                          sort,
                                                          video_type,
                                                          first):
            yield result

    async def fetch_clips_by_ids(self,
                                 clip_ids: List[str],
                                 started_at: Optional[datetime.datetime] = None,
                                 ended_at: Optional[datetime.datetime] = None,
                                 is_featured: Optional[bool] = None,
                                 first: int = 100) -> AsyncGenerator[List[channels.Clip], None]:
        """
        Fetch clips by their IDs.

        Parameters
        ----------
        clip_ids: List[str]
            A list of clip IDs to retrieve.
        started_at: Optional[datetime.datetime]
            The start time to filter clips by, by default None.
        ended_at: Optional[datetime.datetime]
            The end time to filter clips by, by default None.
        is_featured: Optional[bool]
            Whether to retrieve only featured clips, by default None.
        first: int
            The maximum number of results to retrieve, by default 100.

        Yields
        ------
        AsyncGenerator[List[channels.Clip], None]
            A list of dictionaries representing clips matching the filters.
        """
        async for result in self._connection.fetch_clips(None,
                                                         clip_ids,
                                                         started_at,
                                                         ended_at,
                                                         is_featured,
                                                         first):
            yield result

    async def fetch_clips_by_category(self,
                                      category_id: str,
                                      started_at: Optional[datetime.datetime] = None,
                                      ended_at: Optional[datetime.datetime] = None,
                                      is_featured: Optional[bool] = None,
                                      first: int = 100) -> AsyncGenerator[List[channels.Clip], None]:
        """
        Fetch clips by category ID.

        Parameters
        ----------
        category_id: str
            The ID of the category to retrieve clips from.
        started_at: Optional[datetime.datetime]
            The start time to filter clips by, by default None.
        ended_at: Optional[datetime.datetime]
            The end time to filter clips by, by default None.
        is_featured: Optional[bool]
            Whether to retrieve only featured clips, by default None.
        first: int
            The maximum number of results to retrieve, by default 100.

        Yields
        ------
        AsyncGenerator[List[channels.Clip], None]
            A list of dictionaries representing clips matching the filters.
        """
        async for result in self._connection.fetch_clips(category_id,
                                                         None,
                                                         started_at,
                                                         ended_at,
                                                         is_featured,
                                                         first):
            yield result

    async def get_content_classification_labels(self, locale: streams.Locale = 'en-US') -> List[streams.CCLInfo]:
        """
        Retrieve content classification labels.

        Parameters
        ----------
        locale: streams.Locale
            The locale to retrieve labels for, by default 'en-US'.

        Returns
        -------
        List[streams.CCLInfo]
            A list of dictionaries representing content classification labels.
        """
        data: List[streams.CCLInfo] = await self._connection.get_content_classification_labels(locale)
        return data

    async def get_global_cheermotes(self) -> List[bits.Cheermote]:
        """
        Retrieve global cheermotes.

        Returns
        -------
        List[bits.Cheermote]
            A list of dictionaries representing global cheermotes.
        """
        data: List[bits.Cheermote] = await self._connection.get_global_cheermotes()
        return data

    async def fetch_top_categories(self, first: int = 100) -> AsyncGenerator[List[search.Game], None]:
        """
        Fetch the top categories on Twitch.

        Parameters
        ----------
        first: int
            The maximum number of results to retrieve, by default 100.

        Yields
        ------
        AsyncGenerator[List[search.Game], None]
            A list of dictionaries representing the top categories.
        """
        async for result in self._connection.fetch_top_games(first):
            yield result

    async def get_categories(self,
                             names: Optional[List[str]] = None,
                             ids: Optional[List[str]] = None,
                             igdb_ids: Optional[List[str]] = None) -> List[search.Game]:
        """
        Retrieve game categories by name, ID, or IGDB ID.

        Parameters
        ----------
        names: Optional[List[str]]
            A list of game names to filter by, by default None.
        ids: Optional[List[str]]
            A list of game IDs to filter by, by default None.
        igdb_ids: Optional[List[str]]
            A list of IGDB IDs to filter by, by default None.

        Returns
        -------
        List[search.Game]
            A list of dictionaries representing game categories.
        """
        data: List[search.Game] = await self._connection.get_games(game_names=names, game_ids=ids, igdb_ids=igdb_ids)
        return data

    async def fetch_categories_search(self, query: str,
                                      first: int = 100) -> AsyncGenerator[List[search.CategorySearch], None]:
        """
        Search for categories by a query string.

        Parameters
        ----------
        query: str
            The search query.
        first: int
            The maximum number of results to retrieve, by default 100.

        Yields
        ------
        AsyncGenerator[List[search.CategorySearch], None]
            A list of dictionaries representing categories matching the search query.
        """
        async for result in self._connection.fetch_categories_search(query, first):
            yield result

    async def fetch_extension_analytics(self,
                                        extension_id: Optional[str] = None,
                                        analytics_type: Literal['overview_v2'] = 'overview_v2',
                                        started_at: Optional[datetime.datetime] = None,
                                        ended_at: Optional[datetime.datetime] = None,
                                        first: int = 100) -> AsyncGenerator[List[analytics.Extension], None]:
        """
        Fetch analytics data for extensions.

        Parameters
        ----------
        extension_id: Optional[str]
            The ID of the extension to filter by, by default None.
        analytics_type: Literal['overview_v2']
            The type of analytics data to retrieve, by default 'overview_v2'.
        started_at: Optional[datetime.datetime]
            The start time to filter analytics by, by default None.
        ended_at: Optional[datetime.datetime]
            The end time to filter analytics by, by default None.
        first: int
            The maximum number of results to retrieve, by default 100.

        Yields
        ------
        AsyncGenerator[List[analytics.Extension], None]
            A list of dictionaries representing extension analytics data.
        """
        async for result in self._connection.fetch_extension_analytics(extension_id,
                                                                       analytics_type,
                                                                       started_at,
                                                                       ended_at,
                                                                       first):
            yield result

    async def fetch_game_analytics(self,
                                   game_id: Optional[str] = None,
                                   analytics_type: Literal['overview_v2'] = 'overview_v2',
                                   started_at: Optional[datetime.datetime] = None,
                                   ended_at: Optional[datetime.datetime] = None,
                                   first: int = 100) -> AsyncGenerator[List[analytics.Game], None]:
        """
        Fetch analytics data for games.

        Parameters
        ----------
        game_id: Optional[str]
            The ID of the game to filter by, by default None.
        analytics_type: Literal['overview_v2']
            The type of analytics data to retrieve, by default 'overview_v2'.
        started_at: Optional[datetime.datetime]
            The start time to filter analytics by, by default None.
        ended_at: Optional[datetime.datetime]
            The end time to filter analytics by, by default None.
        first: int
            The maximum number of results to retrieve, by default 100.

        Yields
        ------
        AsyncGenerator[List[analytics.Game], None]
            A list of dictionaries representing game analytics data.
        """
        async for result in self._connection.fetch_game_analytics(game_id,
                                                                  analytics_type,
                                                                  started_at,
                                                                  ended_at,
                                                                  first):
            yield result
