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

from .broadcaster import ClientUser, ClientChannel, ClientChat, ClientStream
from .utils import setup_logging, Scopes, MISSING, EXCLUSIVE
from .channel import UserChannel, Video, Clip
from .gateway import EventSubWebSocket
from .http import HTTPClient, Server
from .stream import Category, Stream
from .state import ConnectionState
from .user import BaseUser, User
from .chat import Emote, Badge
import asyncio

from typing import TYPE_CHECKING, overload
if TYPE_CHECKING:
    from typing import Any, List, Optional, Callable, Type, Union, AsyncGenerator, Literal
    from .types import http as HttpTypes
    from types import TracebackType
    from datetime import datetime

import logging
_logger = logging.getLogger(__name__)

__all__ = ('Client',)


class Client:
    """
    Represents a Twitch client.

    ???+ info
        This client is designed to listen to EventSub events by default,
        abut it can also use the Helix API if you need more functionality.

        If you require additional features, consider using the `twitch.bot.Bot` class.

        Default scopes: `user:read:email`

    Parameters
    ----------
    client_id: str
        Your app's client ID.
    client_secret: Optional[str]
        Your app's client secret. Required when generating
        a new access token if the user access token is not provided.
        It ensures manual authorization or token generating.
    cli: bool
        Whether to run the client in development mode using the Twitch CLI.
        For testing purposes during development.
    port: int
        The port for the Twitch **CLI websocket** and **Eventsub subscription API**.
    """

    def __init__(self, client_id: str, client_secret: str = MISSING, cli: bool = False,
                 port: int = 8080) -> None:
        # Tokens.
        self._client_id: str = client_id
        self._client_secret: str = client_secret
        # Default scopes.
        self.scopes: List[str] = ['user:read:email']
        # CLI.
        self._port: int = port
        self._cli: bool = cli
        # Client.
        self.loop: Optional[asyncio.AbstractEventLoop] = None
        self.http: HTTPClient = HTTPClient(
            dispatcher=self.dispatch, client_id=client_id, secret_secret=client_secret
        )
        self._connection: ConnectionState = ConnectionState(dispatcher=self.dispatch, http=self.http)

    async def __aenter__(self) -> Client:
        return self

    async def __aexit__(self, exc_type: Optional[Type[BaseException]],
                        exc_value: Optional[BaseException],
                        traceback: Optional[TracebackType]) -> None:
        await self._setup_loop()
        if self.http.is_open:
            await self.http.close()

    async def close(self):
        await self.http.close()
        self.loop = MISSING

    @property
    def user(self) -> Optional[ClientUser]:
        """
        Represents the client.

        returns
        -------
        Optional[ClientUser]
            Client user.
        """
        return self._connection.user

    @property
    def channel(self) -> Optional[ClientChannel]:
        """
        Represents the client channel.

        returns
        -------
        Optional[ClientChannel]
            Client channel.
        """
        return self._connection.channel

    @property
    def chat(self) -> Optional[ClientChat]:
        """
        Represents the client channel chat.

        returns
        -------
        Optional[ClientChannel]
            Client channel chat.
        """
        return self._connection.chat

    @property
    def stream(self) -> Optional[ClientStream]:
        """
        Represents the client channel stream.

        returns
        -------
        Optional[ClientStream]
            Client channel stream.
        """
        return self._connection.stream

    @property
    def is_streaming(self) -> bool:
        """
        Indicates if the client is streaming.

        returns
        -------
        bool
            True if the client is streaming, False otherwise.
        """
        return self._connection.is_streaming

    async def _run_event(self, coro: Callable[..., Any], event_name: str, *args: Any, **kwargs: Any) -> None:
        # Execute the specified event coroutine with the given arguments.
        try:
            await coro(*args, **kwargs)
        except asyncio.CancelledError:
            pass
        except Exception as error:
            await self.on_error(event_name, error, *args, **kwargs)

    async def _setup_loop(self):
        loop = asyncio.get_running_loop()
        self.loop = loop

    def dispatch(self, event: str, /, *args: Any, **kwargs: Any) -> None:
        # Dispatch a specified event with the given arguments.
        method = "on_" + event
        try:
            coro = getattr(self, method)
            if coro is not None and asyncio.iscoroutinefunction(coro):
                _logger.debug('Dispatching event %s', event)
                wrapped = self._run_event(coro, method, *args, **kwargs)
                # Schedule the task
                self.loop.create_task(wrapped, name=f'Twitchify:{method}')

        except AttributeError:
            pass
        except Exception as error:
            _logger.error('Event: %s Error: %s', event, error)

    def event(self, coro: Callable[..., Any], /) -> None:
        """
        A decorator that registers an event to listen to.

        Parameters
        ----------
        coro: Callable[..., Any]
            The coroutine function representing the event to listen to.

        Raises
        ------
        TypeError
            If the function is not a coroutine.

        Example
        --------
        ```py
        @client.event
        async def on_ready():
            print('Ready!')
        ```
        """
        if not asyncio.iscoroutinefunction(coro):
            raise TypeError("The registered event must be a coroutine function")
        setattr(self, coro.__name__, coro)

    @staticmethod
    async def on_error(event_name: str, error: Exception, /, *args: Any, **kwargs: Any) -> None:
        """
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

    async def connect(self, access_token: str = MISSING, *, refresh_token: str = MISSING,
                      reconnect: bool = True) -> None:
        """
        Establishes a connection.

        ???+ Warning
            You can either use access_token alone or use refresh_token along with the client_secret
            to ensure token generation. Using only access_token may result in it expiring at any time.

        Parameters
        ----------
        access_token: str
            The User access token. If not provided, a web server will be opened for manual authentication.
        refresh_token: str
            A token used for obtaining a new access tokens, but it requires the app's client secret.
        reconnect: bool
            Whether to attempt reconnecting on internet or Twitch failures.
        """
        # Setup loop
        if self.loop is None:
            await self._setup_loop()

        # Validating the access key and opening a new session.
        validation = await self.http.open_session(access_token=access_token, refresh_token=refresh_token)
        # Retrieving the client.
        await self._connection.setup_client()

        events = [attr.replace('on_', '', 1) for attr in dir(self) if attr.startswith('on_')]
        # Creating an EventSub websocket.
        EventSub = EventSubWebSocket(connection=self._connection, loop=self.loop, events=events)
        # Debug mode.
        if self._cli:
            EventSub.cli = f'ws://localhost:{self._port}/ws'
            self.http.cli = f'http://localhost:{self._port}/eventsub/subscriptions'
        # Creating tasks.
        tasks: List[asyncio.Task] = [
            self.loop.create_task(self.http.refresher(expires_in=validation['expires_in']),
                                  name="Twitchify:Refresher"),
            self.loop.create_task(EventSub.connect(reconnect=reconnect), name="Twitchify:EventSub")
        ]
        await asyncio.gather(*tasks)

    async def start(self, access_token: str = MISSING, *, refresh_token: str = MISSING, port: int = 3000,
                    force_verify: bool = True, reconnect: bool = True, scopes: HttpTypes.Scopes = MISSING,
                    log_level: int = logging.INFO) -> None:
        """
        Connect to the Twitch API and handle authentication.

        ???+ info
            This method provides a simple way to connect to the Twitch API. If an `access_token` is provided,
            it will use that token for authorization. If not, it will initiate a web server for manual
            authentication. The `access_token` and `refresh_token` will be automatically added if obtained
            through the authorization flow.

        Parameters
        ----------
        access_token: str
            The user's access token. If not provided, a web server will be opened for manual authorization.
        refresh_token: str
            A token used for obtaining new access tokens without requiring user re-authorization.
            Requires the app's client secret.
        port: int
            The port for the Twitch CLI websocket and the authorization web server.
        force_verify: bool
            Force the user to re-authorize if True.
        scopes: List
            A list of scopes required by the Twitch API to support your app's functionality.

            If `token` is `MISSING`, the user will manually authenticate using these scopes,
            If not provided, the default value will be all available scopes.
        reconnect: bool
            Whether to attempt reconnecting on internet or Twitch failures.
        log_level: int
            The log level for the library's logger. Can be one of the following:

            - logging.ERROR (40): For critical errors.
            - logging.WARNING (30): For non-critical warnings.
            - logging.INFO (20): For general information.
            - logging.DEBUG (10): For detailed debugging information.

        Raises
        ------
        TypeError
            - If the client_secret is not provided, and the user access token is not provided.
              In this case, it's not possible to generate a new access token, and the client cannot
              interact with the Twitch API without authorization.
            - If a scope does not exist.
        """
        # Setup logger.
        setup_logging(level=log_level)
        refresh_token = None if refresh_token is MISSING else refresh_token
        if access_token is MISSING and not (refresh_token and self._client_secret):
            if self._client_secret:
                if scopes is MISSING:
                    # Global scopes.
                    self.scopes = Scopes
                else:
                    if not all(scope in Scopes for scope in scopes):
                        raise TypeError('One or more scopes do not exist.')
                    self.scopes.extend(scopes)
                # Authenticates with the Twitch API using OAuth 2.0 authorization code grant flow.
                async with Server(port=port) as server:
                    auth_url = server.url(client_id=self._client_id, scopes=self.scopes,
                                          force_verify=force_verify)
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
                    # Setup loop for dispatch.
                    if self.loop is None:
                        await self._setup_loop()
                    self.dispatch('auth_url', auth_url, server.uri)
                    code = await server.wait_for_code()
                    access_token, refresh_token = await self.http.auth_code(code=code,
                                                                            redirect_uri=server.uri)
                    self.dispatch('auth', access_token, refresh_token)
            else:
                raise TypeError('Missing Client Secret, Unable to authorize.')
        await self.connect(access_token=access_token, refresh_token=refresh_token, reconnect=reconnect)

    def run(self, access_token: str = MISSING, *, refresh_token: str = MISSING,
            port: int = 3000, force_verify: bool = True, reconnect: bool = True,
            scopes: HttpTypes.Scopes = MISSING, log_level: int = logging.INFO) -> None:
        """
        Run the client and handle the event loop.

        !!! danger
            This function must be the last function to call as it blocks
            the execution of anything after it.

        Parameters
        ----------
        access_token: str
            The user's access token. If not provided, a web server will be opened for manual authorization.
        refresh_token: str
            A token used for obtaining new access tokens without requiring user re-authorization.
            Requires the app's client secret.
        port: int
            The port for the Twitch CLI websocket and the authorization web server.
        force_verify: bool
            Force the user to re-authorize if True.
        scopes: List
            A list of scopes required by the Twitch API to support your app's functionality.

            If `token` is `MISSING`, the user will manually authenticate using these scopes,
            If not provided, the default value will be all available scopes.
        reconnect: bool
            Whether to attempt reconnecting on internet or Twitch failures.
        log_level: int
            The log level for the library's logger. Can be one of the following:

            - logging.ERROR (40): For critical errors.
            - logging.WARNING (30): For non-critical warnings.
            - logging.INFO (20): For general information.
            - logging.DEBUG (10): For detailed debugging information.
        """

        async def starter():
            async with self:
                await self.start(access_token=access_token, refresh_token=refresh_token,
                                 scopes=scopes, port=port, force_verify=force_verify,
                                 reconnect=reconnect, log_level=log_level)

        try:
            asyncio.run(starter())
        except KeyboardInterrupt:
            return

    @overload
    async def get_user(self, name: str) -> User:
        ...

    @overload
    async def get_user(self, *, id: str) -> User:
        ...

    async def get_user(self, name: str = EXCLUSIVE, id: str = EXCLUSIVE) -> User:
        """
        Retrieve user information.

        Parameters
        ----------
        name: str
            The user's name.
        id: str
            The user's ID.

        Returns
        -------
        User
            An object representing user information.
        """
        data = await self._connection.get_user_info(name=name, user_id=id)
        return data

    async def get_channel(self, user: Union[str, BaseUser]) -> UserChannel:
        """
        Retrieve a user's channel information.

        Parameters
        ----------
        user: Union[str, BaseUser]
            The user or user's name.

        Returns
        -------
        UserChannel
            An object representing the user's channel.
        """
        data = await self._connection.get_channel(user)

        return data

    async def get_category(self, name: str) -> Category:
        """
        Retrieve category information by name.

        Parameters
        ----------
        name: str
            The name of the category to retrieve.

        Returns
        -------
        Category
            An object representing the category information.
        """
        data = await self._connection.get_category(name)
        return data

    async def get_global_emotes(self) -> List[Emote]:
        """
        Retrieve global emotes available on Twitch.

        Returns
        -------
        List[Emote]
            A list of Emote objects representing global emotes.
        """
        data = await self._connection.get_global_emotes()
        return data

    async def get_global_badges(self) -> List[Badge]:
        """
        Retrieve global badges available on Twitch.

        Returns
        -------
        List[Badge]
            A list of Badge objects representing global badges.
        """
        data = await self._connection.get_global_badges()
        return data

    async def fetch_streams(
            self,
            users: List[Union[str, BaseUser]] = MISSING,
            categories: List[Union[str, Category]] = MISSING,
            stream_type: Literal['all', 'live'] = 'all',
            languages: List[str] = MISSING,
            limit: int = 4
    ) -> AsyncGenerator[List[Stream]]:
        """
        Fetch a list of live or all streams based on specified criteria.

        Parameters
        ----------
        users: List[Union[str, BaseUser]]
            A list of users or their usernames for filtering streams.
        categories: List[Union[str, Category]]
            A list of categories or their names for filtering streams.
        stream_type: Literal['all', 'live']
            The type of streams to fetch: 'all' (default) for all streams or 'live' for live streams only.
        languages: List[str]
            A list of language codes for filtering streams by language.
        limit: optional
            The maximum number of streams to fetch.

        Yields
        ------
        AsyncGenerator[List[Stream]]
            An asynchronous generator that yields lists of Stream objects matching the specified criteria.
        """
        async for streams in self._connection.fetch_streams(
                limit=limit,
                users=users,
                categories=categories,
                stream_type=stream_type,
                languages=languages):
            yield streams

    @overload
    def fetch_videos(self, videos: List[Union[Video, Clip]],
                     period: Literal['all', 'day', 'month', 'week'] = 'all',
                     videos_type: Literal['all', 'archive', 'highlight', 'upload'] = 'all',
                     sort: Literal['time', 'trending', 'views'] = 'time',
                     language: str = MISSING,
                     limit: int = 4) -> AsyncGenerator[List[Video]]:
        ...

    @overload
    def fetch_videos(self, category: Union[str, Category],
                     period: Literal['all', 'day', 'month', 'week'] = 'all',
                     videos_type: Literal['all', 'archive', 'highlight', 'upload'] = 'all',
                     sort: Literal['time', 'trending', 'views'] = 'time',
                     language: str = MISSING,
                     limit: int = 4) -> AsyncGenerator[List[Video]]:
        ...

    async def fetch_videos(self, videos: List[Union[str, Video, Clip]] = EXCLUSIVE,
                           category: Union[str, Category] = EXCLUSIVE,
                           period: Literal['all', 'day', 'month', 'week'] = 'all',
                           sort: Literal['time', 'trending', 'views'] = 'time',
                           videos_type: Literal['all', 'archive', 'highlight', 'upload'] = 'all',
                           language: str = MISSING,
                           limit: int = 4
                           ) -> AsyncGenerator[List[Video]]:

        """
        Fetch videos based on specified criteria.

        ???+ Warning
            You must choose either `videos` (list of videos) or `category` (a single category)
            as they are mutually exclusive.

        Parameters
        ----------
        videos: List[Union[Video, Clip]]
            A list of Video or Clip objects or their IDs for filtering videos.
        category: Union[str, Category]
            A category or its name for filtering videos.
        sort: Literal['time', 'trending', 'views']
            The sorting order for fetched videos.
        period: Literal['all', 'day', 'month', 'week']
            The time period for filtering videos.
        videos_type: Literal['all', 'archive', 'highlight', 'upload']
            The type of videos to fetch.
        language: str
            The language code for filtering videos by language.
        limit: int
            The maximum number of videos to fetch per batch.

        Yields
        ------
        AsyncGenerator[List[Video]]
            An asynchronous generator that yields lists of Video objects matching the specified criteria.
        """
        async for videos in self._connection.fetch_videos(
                videos=videos,
                category=category,
                period=period,
                language=language,
                sort=sort,
                videos_type=videos_type,
                limit=limit):
            yield videos

    @overload
    def fetch_clips(self, clips: List[Clip],
                    started_at: datetime = MISSING,
                    ended_at: datetime = MISSING,
                    featured: bool = False,
                    limit: int = 4) -> AsyncGenerator[List[Clip]]:
        ...

    @overload
    def fetch_clips(self, category: Union[str, Category],
                    started_at: datetime = MISSING,
                    ended_at: datetime = MISSING,
                    featured: bool = False,
                    limit: int = 4) -> AsyncGenerator[List[Clip]]:
        ...

    async def fetch_clips(self, clips: List[Union[str, Clip]] = EXCLUSIVE,
                          category: Union[str, Category] = EXCLUSIVE,
                          started_at: datetime = MISSING, ended_at: datetime = MISSING,
                          featured: bool = MISSING,
                          limit: int = 4) -> AsyncGenerator[List[Clip]]:

        """
        Fetch clips based on specified criteria.

        ???+ Warning
            You must choose either `clips` (list of clips) or
            `category` (a single category) as they are mutually exclusive.

        Parameters
        ----------
        clips: List[Clip]
            A list of Clip objects or their IDs for filtering clips.
        category: Union[str, Category]
            A category or its name for filtering clips.
        started_at: datetime
            The starting date and time for filtering clips.
        ended_at: datetime
            The ending date and time for filtering clips.
        featured: bool
            Include only featured clips if True, or non-featured clips if False.
            If not specified, all clips are returned.
        limit: int
            The maximum number of clips to fetch per batch.

        Yields
        ------
        AsyncGenerator[List[Clip]]
            An asynchronous generator that yields lists of Clip objects matching the specified criteria.
        """
        async for clips in self._connection.fetch_clips(
                clips=clips,
                category=category,
                started_at=started_at,
                ended_at=ended_at,
                featured=featured,
                limit=limit):
            yield clips
