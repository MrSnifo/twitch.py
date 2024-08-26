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

from .utils import datetime_to_str, convert_rfc3339
from .stream import Stream, BroadcasterStream
from typing import overload, TYPE_CHECKING
from .chat import Chat, BroadcasterChat

if TYPE_CHECKING:
    from .types import (Data, PData, TData, channels, moderation, streams, users, TPData, activity, DTData, bits,
                        interaction)
    from typing import Optional, List, AsyncGenerator, Literal, Dict, Any
    from .state import ConnectionState
    from .user import User
    import datetime

__all__ = ('Channel', 'BroadcasterChannel', 'ClientChannel')


class Channel:
    """
    Represents a channel.
    """

    __slots__ = ('_state', '_user_id', '_auth_user_id')

    def __init__(self, user_id: str, auth_user_id: str, *, state: ConnectionState) -> None:
        self._state: ConnectionState = state
        self._user_id: str = user_id
        self._auth_user_id: str = auth_user_id

    @property
    def chat(self) -> Chat:
        """
        Get the chat functionality associated with this channel.

        Returns
        -------
        Chat
            The `Chat` object representing the chat functionality for the channel.
        """
        return Chat(self._user_id, self._auth_user_id, state=self._state)

    @property
    def stream(self) -> Stream:
        """
        Get the streaming functionality associated with this channel.

        Returns
        -------
        Stream
            The `Stream` object representing the streaming functionality for the channel.
        """
        return Stream(self._user_id, self._auth_user_id, state=self._state)

    async def get_info(self) -> channels.ChannelInfo:
        """
        Retrieve detailed information about the channel.

        Returns
        -------
        channels.ChannelInfo
            A dictionary containing the channel's information, including details such as title, description, and more.
        """
        data: Data[List[channels.ChannelInfo]] = await self._state.http.get_channel_information(
            self._auth_user_id, [self._user_id])
        return data['data'][0]

    async def get_teams(self) -> List[channels.ChannelTeam]:
        """
        Retrieve the teams associated with the channel.

        Returns
        -------
        List[dict]
            A list of dictionaries representing the teams that the channel is part of.
        """
        data: Data[List[channels.ChannelTeam]] = await self._state.http.get_channel_teams(self._auth_user_id,
                                                                                          broadcaster_id=self._user_id)
        return data['data']

    async def get_total_followers(self) -> int:
        """
        Retrieve the total number of followers for the channel.

        | Scopes                     | Description                          |
        | -------------------------- | -------------------------------------|
        | `moderator:read:followers` | Read the followers of a broadcaster. |

        Returns
        -------
        int
            The total count of followers for the channel.
        """
        data: TData[List[channels.Follower]] = await self._state.http.get_channel_followers(
            self._auth_user_id,
            broadcaster_id=self._user_id,
            first=1)
        return data['total']

    @overload
    async def check_follower(self, user: User) -> channels.Follower:
        ...

    @overload
    async def check_follower(self, user: User) -> None:
        ...

    async def check_follower(self, user: User) -> Optional[channels.Follower]:
        """
        Check if a specific user is a follower of the channel.

        | Scopes                     | Description                          |
        | -------------------------- | -------------------------------------|
        | `moderator:read:followers` | Read the followers of a broadcaster. |

        Parameters
        ----------
        user: User
            The user to check for being a follower.

        Returns
        -------
        Optional[channels.Follower]
            A dictionary representing the follower if the user is a follower, otherwise `None`.
        """
        data: TData[List[channels.Follower]] = await self._state.http.get_channel_followers(self._auth_user_id,
                                                                                            self._user_id,
                                                                                            user_id=user.id)
        return data['data'][0] if len(data['data']) != 0 else None

    async def fetch_followers(self, *, first: int = 100) -> AsyncGenerator[List[channels.Follower], None]:
        """
        Retrieve followers for the channel in pages.

        | Scopes                     | Description                          |
        | -------------------------- | -------------------------------------|
        | `moderator:read:followers` | Read the followers of a broadcaster. |

        Parameters
        ----------
        first: int
            The maximum number of results to retrieve per page.

        Yields
        ------
        AsyncGenerator[List[channels.Follower], None]
            A generator yielding lists of dictionaries representing followers.
        """
        kwargs: Dict[str, Any] = {
            'broadcaster_id': self._user_id,
            'first': first,
            'after': None
        }
        while True:
            data: TData[List[channels.Follower]] = await self._state.http.get_channel_followers(self._auth_user_id,
                                                                                                **kwargs)
            yield data['data']
            kwargs['after'] = data['pagination'].get('cursor')
            if not kwargs['after']:
                break

    async def get_banned_users(self, __users: List[User], /) -> List[moderation.BannedUser]:
        """
        Retrieve information about banned users from the channel.

        | Scopes                          | Description                       |
        | ------------------------------- | ----------------------------------|
        | `moderation:read`               | View a channel’s moderation data. |
        | `moderator:manage:banned_users` | Ban and unban users.              |

        Parameters
        ----------
        __users: List[User]
            A list of users to check if they are banned.

        Returns
        -------
        List[moderation.BannedUser]
            A list of dictionaries representing the banned users.
        """
        data: PData[List[moderation.BannedUser]] = await self._state.http.get_banned_users(
            self._auth_user_id,
            self._user_id,
            user_ids=[user.id for user in __users])
        return data['data']

    async def fetch_banned_users(self, *, first: int = 100) -> AsyncGenerator[List[moderation.BannedUser], None]:
        """
        Retrieve banned users from the channel in pages.

        | Scopes                          | Description                                                       |
        | ------------------------------- | ------------------------------------------------------------------|
        | `moderation:read`               | View a channel’s moderation data including Moderators, Bans, ..., |
        | `moderator:manage:banned_users` | Ban and unban users.                                              |

        Parameters
        ----------
        first: int
            The maximum number of results to retrieve per page.

        Yields
        ------
        AsyncGenerator[List[moderation.BannedUser], None]
            A generator yielding lists of dictionaries representing banned users.
        """
        kwargs: Dict[str, Any] = {
            'broadcaster_id': self._user_id,
            'first': first,
            'after': None
        }
        while True:
            data: PData[List[moderation.BannedUser]] = await self._state.http.get_banned_users(self._auth_user_id,
                                                                                               **kwargs)
            yield data['data']
            kwargs['after'] = data['pagination'].get('cursor')
            if not kwargs['after']:
                break

    async def ban(self, user: User, duration: Optional[int] = None, reason: Optional[str] = None) -> None:
        """
        Ban a user from the channel.

        | Scopes                          | Description          |
        | ------------------------------- | ---------------------|
        | `moderator:manage:banned_users` | Ban and unban users. |

        Parameters
        ----------
        user: User
            The user to be banned.
        duration: Optional[int]
            The duration of the ban in minutes.
        reason: Optional[str]
            The reason for banning the user.
        """
        await self._state.http.ban_user(self._user_id, self._auth_user_id, user.id, duration=duration, reason=reason)

    async def unban(self, user: User) -> None:
        """
        Unban a user from the channel.

        | Scopes                          | Description          |
        | ------------------------------- | ---------------------|
        | `moderator:manage:banned_users` | Ban and unban users. |

        Parameters
        ----------
        user: User
            The user to be unbanned.
        """
        await self._state.http.unban_user(self._user_id, self._auth_user_id, user.id)

    @overload
    async def check_unban_request(self,
                                  user: User,
                                  *,
                                  status: Literal['pending', 'approved', 'denied', 'acknowledged', 'canceled']
                                  ) -> moderation.UnBanRequest:
        ...

    @overload
    async def check_unban_request(self,
                                  user: User,
                                  *,
                                  status: Literal['pending', 'approved', 'denied', 'acknowledged', 'canceled']
                                  ) -> None:
        ...

    async def check_unban_request(self,
                                  user: User,
                                  *,
                                  status: Literal['pending', 'approved', 'denied', 'acknowledged', 'canceled']
                                  ) -> Optional[moderation.UnBanRequest]:
        """
        Retrieve a specific unban request for a user.

        | Scopes                            | Description                            |
        | --------------------------------- | ---------------------------------------|
        | `moderator:read:unban_requests`   | View a broadcaster’s unban requests.   |
        | `moderator:manage:unban_requests` | Manage a broadcaster’s unban requests. |

        Parameters
        ----------
        user: User
            The user for whom the unban request is to be retrieved.
        status: Literal['pending', 'approved', 'denied', 'acknowledged', 'canceled']
            The status of the unban request to filter by.

        Returns
        -------
        Optional[moderation.UnBanRequest]
            A dictionary containing the details of the unban request if it exists; otherwise, None.
        """
        data: PData[List[moderation.UnBanRequest]] = await self._state.http.get_unban_requests(self._user_id,
                                                                                               self._auth_user_id,
                                                                                               status=status,
                                                                                               user_id=user.id)
        return data['data'][0] if len(data['data']) != 0 else None

    async def fetch_unban_requests(self,
                                   status: Literal['pending', 'approved', 'denied', 'acknowledged', 'canceled'],
                                   *,
                                   first: int = 100) -> AsyncGenerator[List[moderation.UnBanRequest], None]:
        """
        Retrieve unban requests from the channel in pages.

        | Scopes                            | Description                            |
        | --------------------------------- | ---------------------------------------|
        | `moderator:read:unban_requests`   | View a broadcaster’s unban requests.   |
        | `moderator:manage:unban_requests` | Manage a broadcaster’s unban requests. |

        Parameters
        ----------
        status: Literal['pending', 'approved', 'denied', 'acknowledged', 'canceled']
            The status of the unban requests to filter by.
        first: int
            The maximum number of results to retrieve per page.

        Yields
        ------
        AsyncGenerator[List[moderation.UnBanRequest], None]
            A generator yielding lists of dictionaries representing unban requests.
        """
        kwargs: Dict[str, Any] = {
            'broadcaster_id': self._user_id,
            'moderator_id': self._auth_user_id,
            'status': status.lower(),
            'first': first,
            'after': None
        }
        while True:
            data: PData[List[moderation.UnBanRequest]] = await self._state.http.get_unban_requests(**kwargs)
            yield data['data']
            kwargs['after'] = data['pagination'].get('cursor')
            if not kwargs['after']:
                break

    async def resolve_unban_request(self,
                                    request_id: str,
                                    status: Literal['approved', 'denied'],
                                    resolution_text: Optional[str] = None) -> moderation.UnBanRequest:
        """
        Resolve an unban request.

        | Scopes                            | Description                            |
        | --------------------------------- | ---------------------------------------|
        | `moderator:manage:unban_requests` | Manage a broadcaster’s unban requests. |

        Parameters
        ----------
        request_id: str
            The ID of the unban request to resolve.
        status: Literal['approved', 'denied']
            The status to set for the unban request.
        resolution_text: Optional[str]
            Optional text explaining the resolution.

        Returns
        -------
        moderation.UnBanRequest
            A dictionary containing the details of the resolved unban request.
        """
        data: Data[List[moderation.UnBanRequest]] = await self._state.http.resolve_unban_requests(
            self._user_id,
            self._auth_user_id,
            unban_request_id=request_id,
            status=status,
            resolution_text=resolution_text)
        return data['data'][0]

    async def fetch_recent_stream_markers(self, first: int = 100) -> AsyncGenerator[List[streams.StreamMarker], None]:
        """
        Retrieve recent stream markers for the channel in pages.

        | Scopes                     | Description                                 |
        | -------------------------- | --------------------------------------------|
        | `user:read:broadcast`      | View a user’s broadcasting configuration.   |
        | `channel:manage:broadcast` | Manage a channel’s broadcast configuration. |

        Parameters
        ----------
        first: int
            The maximum number of results to retrieve per page.

        Yields
        ------
        AsyncGenerator[List[streams.StreamMarker], None]
            A generator yielding lists of dictionaries representing stream markers.
        """
        kwargs: Dict[str, Any] = {
            'user_id': self._user_id,
            'first': first,
            'after': None
        }
        while True:
            data: PData[List[streams.StreamMarker]] = await self._state.http.get_stream_markers(self._auth_user_id,
                                                                                                **kwargs)
            yield data['data']
            kwargs['after'] = data['pagination'].get('cursor')
            if not kwargs['after']:
                break

    async def fetch_video_markers(self,
                                  video_id: str,
                                  first: int = 100) -> AsyncGenerator[List[streams.StreamMarker], None]:
        """
        Retrieve markers for a specific video in pages.

        | Scopes                     | Description                                 |
        | -------------------------- | --------------------------------------------|
        | `user:read:broadcast`      | View a user’s broadcasting configuration.   |
        | `channel:manage:broadcast` | Manage a channel’s broadcast configuration. |

        Parameters
        ----------
        video_id: str
            The ID of the video for which to retrieve markers.
        first: int
            The maximum number of results to retrieve per page.

        Yields
        ------
        AsyncGenerator[List[streams.StreamMarker], None]
            A generator yielding lists of dictionaries representing video markers.
        """
        kwargs: Dict[str, Any] = {
            'video_id': video_id,
            'first': first,
            'after': None
        }
        while True:
            data: PData[List[streams.StreamMarker]] = await self._state.http.get_stream_markers(self._auth_user_id,
                                                                                                **kwargs)
            yield data['data']
            kwargs['after'] = data['pagination'].get('cursor')
            if not kwargs['after']:
                break

    async def fetch_videos(self,
                           language: Optional[str] = None,
                           period: Optional[Literal['all', 'day', 'month', 'week']] = None,
                           sort: Optional[Literal['time', 'trending', 'views']] = None,
                           video_type: Optional[Literal['all', 'archive', 'highlight', 'upload']] = None,
                           first: Optional[int] = 100) -> AsyncGenerator[List[channels.Video], None]:
        """
        Retrieve videos for the channel in pages.

        Parameters
        ----------
        language: Optional[str]
            The language of the videos to filter by, or None to include all languages.
        period: Optional[Literal['all', 'day', 'month', 'week']]
            The time period for the videos, or None to include all periods.
        sort: Optional[Literal['time', 'trending', 'views']]
            The sorting method for the videos, or None to use the default sort.
        video_type: Optional[Literal['all', 'archive', 'highlight', 'upload']]
            The type of videos to retrieve, or None to include all types.
        first: Optional[int]
            The maximum number of results to retrieve per page.

        Yields
        ------
        AsyncGenerator[List[channels.Video], None]
            A generator yielding lists of dictionaries representing videos.
        """
        kwargs: Dict[str, Any] = {
            'user_id': self._user_id,
            'language': language,
            'period': period,
            'sort': sort,
            'video_type': video_type,
            'first': first,
            'after': None
        }
        while True:
            data: PData[List[channels.Video]] = await self._state.http.get_videos(self._auth_user_id, **kwargs)
            yield data['data']
            kwargs['after'] = data['pagination'].get('cursor')
            if not kwargs['after']:
                break

    async def fetch_clips(self,
                          started_at: Optional[datetime] = None,
                          ended_at: Optional[datetime] = None,
                          is_featured: Optional[bool] = None,
                          first: int = 100
                          ) -> AsyncGenerator[List[channels.Clip], None]:
        """
        Retrieve clips from the channel in pages.

        Parameters
        ----------
        started_at: Optional[datetime]
            The start date and time for filtering clips.
        ended_at: Optional[datetime]
            The end date and time for filtering clips.
        is_featured: Optional[bool]
            Whether to filter by featured clips.
        first: int
            The maximum number of results to retrieve per page.

        Yields
        ------
        AsyncGenerator[List[channels.Clip], None]
            A generator yielding lists of dictionaries representing clips.
        """
        kwargs: Dict[str, Any] = {
            'broadcaster_id': self._user_id,
            'started_at': datetime_to_str(started_at),
            'ended_at': datetime_to_str(ended_at),
            'is_featured': is_featured,
            'first': first,
            'after': None
        }
        while True:
            data: PData[List[channels.Clip]] = await self._state.http.get_clips(self._auth_user_id, **kwargs)
            yield data['data']
            kwargs['after'] = data['pagination'].get('cursor')
            if not kwargs['after']:
                break


class BroadcasterChannel(Channel):
    """
    Represents a broadcaster channel.
    """

    __slots__ = ()

    def __init__(self, user_id: str, *, state: ConnectionState) -> None:
        super().__init__(user_id, user_id, state=state)

    @property
    def chat(self) -> BroadcasterChat:
        """
        Get the chat functionality associated with broadcaster channel.

        Returns
        -------
        BroadcasterChat
            The `BroadcasterChat` object representing the chat functionality for the channel.
        """
        return BroadcasterChat(self._user_id, state=self._state)

    @property
    def stream(self) -> BroadcasterStream:
        """
        Get the streaming functionality associated with broadcaster channel.

        Returns
        -------
        BroadcasterStream
            The `BroadcasterStream` object representing the streaming functionality for the channel.
        """
        return BroadcasterStream(self._user_id, state=self._state)

    async def get_extensions(self) -> List[channels.Extension]:
        """
        Retrieve all extensions associated with the user.

        | Scopes                | Description                                        |
        | --------------------- | ---------------------------------------------------|
        | `user:read:broadcast` | View a user’s broadcasting configuration.          |
        | `user:edit:broadcast` | View and edit a user’s broadcasting configuration. |

        Returns
        -------
        List[channels.Extension]
            A list of dictionaries representing the user's extensions.
        """
        data: Data[List[channels.Extension]] = await self._state.http.get_user_extensions(self._user_id)
        return data['data']

    async def get_active_extensions(self) -> channels.ActiveExtensions:
        """
        Retrieve all active extensions associated with the user.

        | Scopes                     | Description                                         |
        | --------------------------- | ---------------------------------------------------|
        | `user:read:broadcast`       | View a user’s broadcasting configuration.          |
        | `channel:manage:extensions` | Manage a channel’s Extension configuration.        |
        | `user:edit:broadcast`       | View and edit a user’s broadcasting configuration. |

        Returns
        -------
        channels.ActiveExtensions
            A dictionary representing the currently active extensions.
        """
        data: Data[channels.ActiveExtensions] = await self._state.http.get_user_active_extensions(self._user_id)
        return data['data']

    @overload
    async def update_extension(self,
                               key: Literal['panel'],
                               *,
                               number: Literal['1', '2', '3'],
                               extension_id: str,
                               extension_version: str,
                               activate: bool,
                               x: None = None,
                               y: None = None) -> channels.ActiveExtensions:
        ...

    @overload
    async def update_extension(self,
                               key: Literal['overlay'],
                               *,
                               number: Literal[1],
                               extension_id: str,
                               extension_version: str,
                               activate: bool,
                               x: None = None,
                               y: None = None) -> channels.ActiveExtensions:
        ...

    @overload
    async def update_extension(self,
                               key: Literal['component'],
                               *,
                               number: Literal['1', '2'],
                               extension_id: str,
                               extension_version: str,
                               activate: bool,
                               x: int,
                               y: int) -> channels.ActiveExtensions:
        ...

    async def update_extension(self,
                               key: Literal['panel', 'overlay', 'component'],
                               /,
                               **kwargs: Any) -> channels.ActiveExtensions:
        """
        Update an extension based on the provided parameters.

        | Scopes                     | Description                                         |
        | --------------------------- | ---------------------------------------------------|
        | `channel:manage:extensions` | Manage a channel’s Extension configuration.        |
        | `user:edit:broadcast`       | View and edit a user’s broadcasting configuration. |

        Parameters
        ----------
        key: Literal['panel', 'overlay', 'component']
            The type of extension to update, which can be 'panel', 'overlay', or 'component'.
        **kwargs: dict
            Keyword arguments for the extension update. The available arguments depend on the `key` value:
                - `number` (Literal): The number of the extension to update.
                - `extension_id` (str): The ID of the extension to update.
                - `extension_version` (str): The version of the extension to update.
                - `activate` (bool): Whether to activate or deactivate the extension.
                - `x` (int): The x-coordinate position for 'component' extensions.
                - `y` (int): The y-coordinate position for 'component' extensions.

        Returns
        -------
        channels.ActiveExtensions
            A dictionary representing the updated active extensions.
        """
        data: Data[channels.ActiveExtensions] = await self._state.http.update_user_extensions(self._user_id,
                                                                                              key=key,
                                                                                              **kwargs)
        return data['data']

    async def update(self,
                     category_id: Optional[str] = None,
                     broadcaster_language: Optional[str] = None,
                     title: Optional[str] = None,
                     delay: Optional[int] = None,
                     tags: Optional[List[str]] = None,
                     content_classification_labels: Optional[List[channels.CCL]] = None,
                     is_branded_content: Optional[bool] = None) -> None:
        """
        Update the channel information.

        | Scopes                     | Description                                 |
        | -------------------------- | --------------------------------------------|
        | `channel:manage:broadcast` | Manage a channel’s broadcast configuration. |

        Parameters
        ----------
        category_id: Optional[str]
            The ID of the game or category.
        broadcaster_language: Optional[str]
            The language of the broadcaster.
        title: Optional[str]
            The title of the stream.
        delay: Optional[int]
            The delay in seconds for the stream.
        tags: Optional[List[str]]
            A list of tags for the stream.
        content_classification_labels: Optional[List[channels.CCL]]
            A list of content classification labels.
        is_branded_content: Optional[bool]
            Whether the content is branded.
        """
        await self._state.http.modify_channel_information(self._user_id, category_id, broadcaster_language,
                                                          title, delay, tags, content_classification_labels,
                                                          is_branded_content)

    async def get_moderators(self, __users: List[User], /) -> List[users.SpecificUser]:
        """
        Retrieve a list of specific moderators for the channel.

        | Scopes                       | Description                                                 |
        | --------------------------- | -------------------------------------------------------------|
        | `moderation:read`           | View a channel’s moderation data.                            |
        | `channel:manage:moderators` | Add or remove the moderator role from users in your channel. |

        Parameters
        ----------
        __users: List[User]
            A list of `User` objects representing the users whose moderation status is being queried.

        Returns
        -------
        List[users.SpecificUser]
            A list of dictionaries representing the specific moderators for the channel.
        """
        data: PData[List[users.SpecificUser]] = await self._state.http.get_moderators(self._user_id,
                                                                                      user_ids=[u.id for u in __users],
                                                                                      first=100)
        return data['data']

    async def fetch_moderators(self, first: int = 100) -> AsyncGenerator[List[users.SpecificUser], None]:
        """
        Fetch all moderators for the channel.

        | Scopes                       | Description                                                 |
        | --------------------------- | -------------------------------------------------------------|
        | `moderation:read`           | View a channel’s moderation data.                            |
        | `channel:manage:moderators` | Add or remove the moderator role from users in your channel. |

        Parameters
        ----------
        first: int
            The number of moderators to fetch per request.

        Yields
        ------
        AsyncGenerator[List[users.SpecificUser], None]
            An async generator yielding lists of dictionaries representing the moderators for the channel.
        """
        kwargs: Dict[str, Any] = {
            'broadcaster_id': self._user_id,
            'first': first,
            'after': None
        }
        while True:
            data: PData[List[users.SpecificUser]] = await self._state.http.get_moderators(**kwargs)
            yield data['data']
            kwargs['after'] = data['pagination'].get('cursor')
            if not kwargs['after']:
                break

    async def add_moderator(self, user: User) -> None:
        """
        Add a user as a moderator for the channel.

        | Scopes                       | Description                                                 |
        | --------------------------- | -------------------------------------------------------------|
        | `channel:manage:moderators` | Add or remove the moderator role from users in your channel. |

        Parameters
        ----------
        user: User
            The `User` object representing the user to be added as a moderator.
        """
        await self._state.http.add_channel_moderator(self._user_id, user.id)

    async def remove_moderator(self, user: User) -> None:
        """
        Remove a user from the list of moderators for the channel.

        | Scopes                       | Description                                                 |
        | --------------------------- | -------------------------------------------------------------|
        | `channel:manage:moderators` | Add or remove the moderator role from users in your channel. |


        Parameters
        ----------
        user: User
            The `User` object representing the user to be removed as a moderator.
        """
        await self._state.http.remove_channel_moderator(self._user_id, user.id)

    async def get_editors(self) -> List[channels.Editor]:
        """
        Retrieve all editors associated with the user's channel.

        | Scopes                 | Description                                              |
        | ---------------------- | ---------------------------------------------------------|
        | `channel:read:editors` | View a list of users with the editor role for a channel. |

        Returns
        -------
        List[channels.Editor]
            A list of dictionaries representing the editors of the channel.
        """
        data: Data[List[channels.Editor]] = await self._state.http.get_channel_editors(self._user_id)
        return data['data']

    async def get_vips(self, __users: List[User], /) -> List[users.SpecificUser]:
        """
        Retrieve specific VIPs from the user's channel.

        | Scopes                | Description                                            |
        | --------------------- | -------------------------------------------------------|
        | `channel:read:vips`   | Read the list of VIPs in your channel.                 |
        | `channel:manage:vips` | Add or remove the VIP role from users in your channel. |

        Parameters
        ----------
        __users: List[User]
            A list of users to check for VIP status.

        Returns
        -------
        List[users.SpecificUser]
            A list of dictionaries representing the specific VIPs in the channel.
        """
        data: PData[List[users.SpecificUser]] = await self._state.http.get_vips(self._user_id,
                                                                                user_ids=[u.id for u in __users],
                                                                                first=100)
        return data['data']

    async def fetch_vips(self, first: int = 100) -> AsyncGenerator[List[users.SpecificUser], None]:
        """
        Fetch all VIPs for the channel.

        | Scopes                | Description                                            |
        | --------------------- | -------------------------------------------------------|
        | `channel:read:vips`   | Read the list of VIPs in your channel.                 |
        | `channel:manage:vips` | Add or remove the VIP role from users in your channel. |

        Parameters
        ----------
        first: int
            The number of VIPs to fetch per request.

        Yields
        ------
        AsyncGenerator[List[users.SpecificUser], None]
            An async generator yielding lists of dictionaries representing the VIPs for the channel.
        """
        kwargs: Dict[str, Any] = {
            'broadcaster_id': self._user_id,
            'first': first,
            'after': None
        }
        while True:
            data: PData[List[users.SpecificUser]] = await self._state.http.get_vips(**kwargs)
            yield data['data']
            kwargs['after'] = data['pagination'].get('cursor')
            if not kwargs['after']:
                break

    async def add_vip(self, user: User) -> None:
        """
        Add a user as a VIP in the channel.

        | Scopes                | Description                                            |
        | --------------------- | -------------------------------------------------------|
        | `channel:manage:vips` | Add or remove the VIP role from users in your channel. |

        Parameters
        ----------
        user: User
            The user to be added as a VIP.
        """
        await self._state.http.add_channel_vip(self._user_id, user.id)

    async def remove_vip(self, user: User) -> None:
        """
        Remove a user's VIP status in the channel.

        | Scopes                | Description                                            |
        | --------------------- | -------------------------------------------------------|
        | `channel:manage:vips` | Add or remove the VIP role from users in your channel. |

        Parameters
        ----------
        user: User
            The user whose VIP status should be removed.
        """
        await self._state.http.remove_channel_vip(self._user_id, user.id)

    async def get_total_subscriptions(self) -> int:
        """
        Retrieve the total number of subscriptions for the broadcaster.

        | Scopes                      | Description                                   |
        | ---------------------------- | ---------------------------------------------|
        | `channel:read:subscriptions` | View a list of all subscribers to a channel. |

        Returns
        -------
        int
            The total number of subscriptions for the broadcaster.
        """
        data: TPData[List[channels.Subscription]] = await self._state.http.get_broadcaster_subscriptions(self._user_id,
                                                                                                         first=1)
        return data['total']

    async def get_subscription_points(self) -> int:
        """
        Retrieve the total subscription points for the broadcaster.

        | Scopes                      | Description                                   |
        | ---------------------------- | ---------------------------------------------|
        | `channel:read:subscriptions` | View a list of all subscribers to a channel. |

        Returns
        -------
        int
            The total subscription points for the broadcaster.
        """
        data: TPData[List[channels.Subscription]] = await self._state.http.get_broadcaster_subscriptions(self._user_id,
                                                                                                         first=1)
        return data['points']

    async def get_subscriptions(self, __users: List[User], /) -> List[channels.Subscription]:
        """
        Retrieve the subscription details for specific users.

        | Scopes                      | Description                                   |
        | ---------------------------- | ---------------------------------------------|
        | `channel:read:subscriptions` | View a list of all subscribers to a channel. |

        Parameters
        ----------
        __users: List[User]
            A list of users whose subscription details are to be retrieved.

        Returns
        -------
        List[channels.Subscription]
            A list of dictionaries representing the subscription details of the specified users.
        """
        data: TPData[List[channels.Subscription]] = await self._state.http.get_broadcaster_subscriptions(
            self._user_id,
            user_ids=[u.id for u in __users],
            first=100)
        return data['data']

    async def fetch_subscriptions(self, first: int = 100) -> AsyncGenerator[List[channels.Subscription], None]:
        """
        Fetch all subscriptions for the broadcaster.

        | Scopes                       | Description                                  |
        | ---------------------------- | ---------------------------------------------|
        | `channel:read:subscriptions` | View a list of all subscribers to a channel. |

        Parameters
        ----------
        first: int
            The maximum number of subscriptions to retrieve per request.

        Yields
        ------
        AsyncGenerator[List[channels.Subscription], None]
            A list of dictionaries representing the subscriptions for each page.
        """
        kwargs: Dict[str, Any] = {
            'broadcaster_id': self._user_id,
            'first': first,
            'after': None
        }
        while True:
            data: TPData[List[channels.Subscription]] = await self._state.http.get_broadcaster_subscriptions(**kwargs)
            yield data['data']
            kwargs['after'] = data['pagination'].get('cursor')
            if not kwargs['after']:
                break

    @overload
    async def get_goals(self) -> activity.Goal:
        ...

    @overload
    async def get_goals(self) -> None:
        ...

    async def get_goals(self) -> Optional[activity.Goal]:
        """
        Retrieve the current creator goals for the broadcaster.

        | Scopes               | Description                       |
        | -------------------- | ----------------------------------|
        | `channel:read:goals` | View Creator Goals for a channel. |

        Returns
        -------
        Optional[activity.Goal]
            A dictionary representing the current creator goal, or None if no goals are active.
        """
        data: Data[List[activity.Goal]] = await self._state.http.get_creator_goals(self._user_id)
        return data['data'][0] if len(data['data']) != 0 else None

    async def get_bits_leaderboard(self,
                                   period: Optional[Literal['day', 'week', 'month', 'year', 'all']] = None,
                                   started_at: Optional[datetime] = None,
                                   user: Optional[User] = None,
                                   count: int = 100) -> List[bits.Leaderboard]:
        """
        Retrieve the bits leaderboard for the broadcaster.

        | Scopes      | Description                          |
        | ----------- | -------------------------------------|
        | `bits:read` | View Bits information for a channel. |

        Parameters
        ----------
        period: Optional[Literal['day', 'week', 'month', 'year', 'all']]
            The period for which to retrieve the leaderboard.
        started_at: Optional[datetime]
            The start date for the leaderboard.
        user: Optional[User]
            A specific user to filter the leaderboard.
        count: int
            The number of leaderboard entries to retrieve.

        Returns
        -------
        List[bits.Leaderboard]
            A list of dictionaries representing the bits leaderboard entries.
        """
        kwargs: Dict[str, Any] = {
            'count': count,
            'period': period,
            'started_at': convert_rfc3339(started_at),
            'user_id': user.id if user is not None else None
        }
        data: DTData[List[bits.Leaderboard]] = await self._state.http.get_bits_leaderboard(self._user_id, **kwargs)
        return data['data']

    @overload
    async def get_charity_campaign(self) -> activity.Charity:
        ...

    @overload
    async def get_charity_campaign(self) -> None:
        ...

    async def get_charity_campaign(self) -> Optional[activity.Charity]:
        """
        Retrieve the current charity campaign for the broadcaster.

        | Scopes                 | Description                                                       |
        | ---------------------- | ------------------------------------------------------------------|
        | `channel:read:charity` | Read charity campaign details and user donations on your channel. |

        Returns
        -------
        Optional[activity.Charity]
            A dictionary representing the current charity campaign, or None if no campaign is active.
        """
        data: Data[List[activity.Charity]] = await self._state.http.get_charity_campaign(self._user_id)
        return data['data'][0] if len(data['data']) != 0 else None

    async def fetch_charity_donations(self, first: int = 100) -> AsyncGenerator[List[activity.CharityDonation], None]:
        """
        Fetch all donations for the current charity campaign.

        | Scopes                 | Description                                                       |
        | ---------------------- | ------------------------------------------------------------------|
        | `channel:read:charity` | Read charity campaign details and user donations on your channel. |

        Parameters
        ----------
        first: int
            The maximum number of donations to retrieve per request.

        Yields
        ------
        AsyncGenerator[List[activity.CharityDonation], None]
            A list of dictionaries representing the charity donations for each page.
        """
        kwargs: Dict[str, Any] = {
            'broadcaster_id': self._user_id,
            'first': first,
            'after': None
        }
        while True:
            data: PData[List[activity.CharityDonation]] = await self._state.http.get_charity_campaign_donations(
                **kwargs)
            yield data['data']
            kwargs['after'] = data['pagination'].get('cursor')
            if not kwargs['after']:
                break

    async def fetch_hype_trains(self, first: int = 100) -> AsyncGenerator[List[interaction.HypeTrain], None]:
        """
        Fetch all Hype Train events for the broadcaster.

        | Scopes                    | Description                                |
        | ------------------------- | -------------------------------------------|
        | `channel:read:hype_train` | View Hype Train information for a channel. |

        Parameters
        ----------
        first: int
            The maximum number of Hype Train events to retrieve per request.

        Yields
        ------
        AsyncGenerator[List[interaction.HypeTrain], None]
            A list of dictionaries representing the Hype Train events for each page.
        """
        kwargs: Dict[str, Any] = {
            'broadcaster_id': self._user_id,
            'first': first,
            'after': None
        }
        while True:
            data: PData[List[interaction.HypeTrain]] = await self._state.http.get_hype_train_events(**kwargs)
            yield data['data']
            kwargs['after'] = data['pagination'].get('cursor')
            if not kwargs['after']:
                break

    async def get_rewards(self,
                          reward_ids: Optional[List[str]] = None,
                          only_manageable_rewards: bool = False) -> List[interaction.Reward]:
        """
        Retrieve a list of custom rewards for the broadcaster.

        | Scopes                       | Description                                                              |
        | ---------------------------- | -------------------------------------------------------------------------|
        | `channel:read:redemptions`   | View Channel Points custom rewards and their redemptions on a channel.   |
        | `channel:manage:redemptions` | Manage Channel Points custom rewards and their redemptions on a channel. |

        Parameters
        ----------
        reward_ids: Optional[List[str]]
            A list of reward IDs to filter the results.
        only_manageable_rewards: bool
            Whether to return only rewards that can be managed by the broadcaster.

        Returns
        -------
        List[interaction.Reward]
            A list of dictionaries representing the custom rewards.
        """
        data: Data[List[interaction.Reward]] = await self._state.http.get_custom_reward(
            self._user_id,
            reward_ids,
            only_manageable_rewards)
        return data['data']

    async def create_reward(self,
                            title: str,
                            cost: int,
                            is_enabled: bool = True,
                            background_color: Optional[str] = None,
                            is_user_input_required: bool = False,
                            prompt: Optional[str] = None,
                            is_max_per_stream_enabled: bool = False,
                            max_per_stream: Optional[int] = None,
                            is_max_per_user_per_stream_enabled: bool = False,
                            max_per_user_per_stream: Optional[int] = None,
                            is_global_cooldown_enabled: bool = False,
                            global_cooldown_seconds: Optional[int] = None,
                            should_redemptions_skip_request_queue: bool = False) -> interaction.Reward:
        """
        Create a new custom reward for the broadcaster.

        | Scopes                       | Description                                                              |
        | ---------------------------- | -------------------------------------------------------------------------|
        | `channel:manage:redemptions` | Manage Channel Points custom rewards and their redemptions on a channel. |

        Parameters
        ----------
        title: str
            The title of the reward.
        cost: int
            The cost of the reward in channel points.
        is_enabled: bool
            Whether the reward is enabled.
        background_color: Optional[str]
            The background color of the reward.
        is_user_input_required: bool
            Whether user input is required to redeem the reward.
        prompt: Optional[str]
            The prompt to display for the reward.
        is_max_per_stream_enabled: bool
            Whether there is a limit on the number of times the reward can be redeemed per stream.
        max_per_stream: Optional[int]
            The maximum number of times the reward can be redeemed per stream.
        is_max_per_user_per_stream_enabled: bool
            Whether there is a limit on the number of times a user can redeem the reward per stream.
        max_per_user_per_stream: Optional[int]
            The maximum number of times a user can redeem the reward per stream.
        is_global_cooldown_enabled: bool
            Whether there is a global cooldown between redemptions.
        global_cooldown_seconds: Optional[int]
            The cooldown time in seconds between redemptions.
        should_redemptions_skip_request_queue: bool
            Whether redemptions should skip the request queue.

        Returns
        -------
        interaction.Reward
            A dictionary representing the created reward.
        """
        data: Data[List[interaction.Reward]] = await self._state.http.create_custom_rewards(
            self._user_id,
            title,
            cost,
            is_enabled,
            background_color,
            is_user_input_required,
            prompt,
            is_max_per_stream_enabled,
            max_per_stream,
            is_max_per_user_per_stream_enabled,
            max_per_user_per_stream,
            is_global_cooldown_enabled,
            global_cooldown_seconds,
            should_redemptions_skip_request_queue)
        return data['data'][0]

    async def update_reward(self,
                            reward_id: str,
                            title: Optional[str] = None,
                            cost: Optional[int] = None,
                            is_enabled: Optional[bool] = None,
                            background_color: Optional[str] = None,
                            is_user_input_required: Optional[bool] = None,
                            prompt: Optional[str] = None,
                            is_max_per_stream_enabled: Optional[bool] = None,
                            max_per_stream: Optional[int] = None,
                            is_max_per_user_per_stream_enabled: Optional[bool] = None,
                            max_per_user_per_stream: Optional[int] = None,
                            is_global_cooldown_enabled: Optional[bool] = None,
                            global_cooldown_seconds: Optional[int] = None,
                            should_redemptions_skip_request_queue: Optional[bool] = None) -> interaction.Reward:
        """
        Update an existing custom reward for the broadcaster.

        | Scopes                       | Description                                                              |
        | ---------------------------- | -------------------------------------------------------------------------|
        | `channel:manage:redemptions` | Manage Channel Points custom rewards and their redemptions on a channel. |

        Parameters
        ----------
        reward_id: str
            The ID of the reward to update.
        title: Optional[str]
            The new title of the reward.
        cost: Optional[int]
            The new cost of the reward in channel points.
        is_enabled: Optional[bool]
            Whether the reward is enabled.
        background_color: Optional[str]
            The new background color of the reward.
        is_user_input_required: Optional[bool]
            Whether user input is required to redeem the reward.
        prompt: Optional[str]
            The new prompt to display for the reward.
        is_max_per_stream_enabled: Optional[bool]
            Whether there is a limit on the number of times the reward can be redeemed per stream.
        max_per_stream: Optional[int]
            The new maximum number of times the reward can be redeemed per stream.
        is_max_per_user_per_stream_enabled: Optional[bool]
            Whether there is a limit on the number of times a user can redeem the reward per stream.
        max_per_user_per_stream: Optional[int]
            The new maximum number of times a user can redeem the reward per stream.
        is_global_cooldown_enabled: Optional[bool]
            Whether there is a global cooldown between redemptions.
        global_cooldown_seconds: Optional[int]
            The new cooldown time in seconds between redemptions.
        should_redemptions_skip_request_queue: Optional[bool]
            Whether redemptions should skip the request queue.

        Returns
        -------
        interaction.Reward
            A dictionary representing the updated reward.
        """
        data: Data[List[interaction.Reward]] = await self._state.http.update_custom_reward(
            self._user_id,
            reward_id,
            title,
            cost,
            is_enabled,
            background_color,
            is_user_input_required,
            prompt,
            is_max_per_stream_enabled,
            max_per_stream,
            is_max_per_user_per_stream_enabled,
            max_per_user_per_stream,
            is_global_cooldown_enabled,
            global_cooldown_seconds,
            should_redemptions_skip_request_queue)
        return data['data'][0]

    async def delete_reward(self, reward_id: str) -> None:
        """
        Delete an existing custom reward for the broadcaster.

        | Scopes                       | Description                                                              |
        | ---------------------------- | -------------------------------------------------------------------------|
        | `channel:manage:redemptions` | Manage Channel Points custom rewards and their redemptions on a channel. |

        Parameters
        ----------
        reward_id: str
            The ID of the reward to delete.
        """
        await self._state.http.delete_custom_reward(self._user_id, reward_id)

    async def get_reward_redemptions(self,
                                     reward_id: str,
                                     redemptions_ids: List[str],
                                     sort: Literal['oldest', 'newest'] = 'oldest'
                                     ) -> List[interaction.RewardRedemption]:
        """
        Retrieve specific redemptions for a custom reward.

        | Scopes                       | Description                                                              |
        | ---------------------------- | -------------------------------------------------------------------------|
        | `channel:read:redemptions`   | View Channel Points custom rewards and their redemptions on a channel.   |
        | `channel:manage:redemptions` | Manage Channel Points custom rewards and their redemptions on a channel. |

        Parameters
        ----------
        reward_id: str
            The ID of the reward for which to retrieve redemptions.
        redemptions_ids: List[str]
            A list of redemption IDs to filter the results.
        sort: Literal['oldest', 'newest']
            The order in which to sort the redemptions.

        Returns
        -------
        List[interaction.RewardRedemption]
            A list of dictionaries representing the redemptions.
        """
        data: PData[List[interaction.RewardRedemption]] = await self._state.http.get_custom_reward_redemption(
            self._user_id,
            reward_id,
            redemptions_ids,
            sort=sort,
            first=50)
        return data['data']

    async def fetch_reward_redemptions(self,
                                       reward_id: str,
                                       status: Literal['canceled', 'fulfilled', 'unfulfilled'],
                                       sort: Literal['oldest', 'newest'] = 'oldest',
                                       first: int = 50
                                       ) -> AsyncGenerator[List[interaction.RewardRedemption], None]:
        """
        Fetch redemptions for a custom reward.

        | Scopes                       | Description                                                              |
        | ---------------------------- | -------------------------------------------------------------------------|
        | `channel:read:redemptions`   | View Channel Points custom rewards and their redemptions on a channel.   |
        | `channel:manage:redemptions` | Manage Channel Points custom rewards and their redemptions on a channel. |

        Parameters
        ----------
        reward_id: str
            The ID of the reward for which to fetch redemptions.
        status: Literal['canceled', 'fulfilled', 'unfulfilled']
            The status of the redemptions to fetch.
        sort: Literal['oldest', 'newest']
            The order in which to sort the redemptions.
        first: int
            The maximum number of redemptions to retrieve per request.

        Yields
        ------
        AsyncGenerator[List[interaction.RewardRedemption], None]
            A list of dictionaries representing the redemptions for each page.
        """
        kwargs: Dict[str, Any] = {
            'broadcaster_id': self._user_id,
            'reward_id': reward_id,
            'status': status,
            'sort': sort,
            'first': first,
            'after': None,
        }
        while True:
            data: PData[List[interaction.RewardRedemption]] = await self._state.http.get_custom_reward_redemption(
                **kwargs)
            yield data['data']
            kwargs['after'] = data['pagination'].get('cursor')
            if not kwargs['after']:
                break

    async def update_reward_redemptions(self,
                                        reward_id: str,
                                        redemptions_ids: List[str],
                                        *,
                                        status: Literal['canceled', 'fulfilled']
                                        ) -> List[interaction.RewardRedemption]:
        """
        Update the status of specific reward redemptions.

        | Scopes                       | Description                                                              |
        | ---------------------------- | -------------------------------------------------------------------------|
        | `channel:manage:redemptions` | Manage Channel Points custom rewards and their redemptions on a channel. |

        Parameters
        ----------
        reward_id: str
            The ID of the reward for which to update redemptions.
        redemptions_ids: List[str]
            A list of redemption IDs to update.
        status: Literal['canceled', 'fulfilled']
            The new status of the redemptions.

        Returns
        -------
        List[interaction.RewardRedemption]
            A list of dictionaries representing the updated redemptions.
        """
        data: Data[List[interaction.RewardRedemption]] = await self._state.http.update_redemption_status(
            self._user_id,
            reward_id,
            redemptions_ids,
            status=status)
        return data['data']

    async def get_predictions(self, prediction_ids: List[str]) -> List[interaction.Prediction]:
        """
        Retrieve a list of predictions by their IDs.

        | Scopes                       | Description                                     |
        | ---------------------------- | ------------------------------------------------|
        | `channel:read:predictions`   | View a channel’s Channel Points Predictions.    |
        | `channel:manage:predictions` | Manage of channel’s Channel Points Predictions. |

        Parameters
        ----------
        prediction_ids: List[str]
            A list of prediction IDs to retrieve.

        Returns
        -------
        List[interaction.Prediction]
            A list of dictionaries representing the predictions.
        """
        data: PData[List[interaction.Prediction]] = await self._state.http.get_predictions(
            self._user_id,
            prediction_ids,
            first=25
        )
        return data['data']

    async def fetch_predictions(self, first: int = 25) -> AsyncGenerator[List[interaction.Prediction], None]:
        """
        Fetch broadcaster predictions.

        | Scopes                       | Description                                     |
        | ---------------------------- | ------------------------------------------------|
        | `channel:read:predictions`   | View a channel’s Channel Points Predictions.    |
        | `channel:manage:predictions` | Manage of channel’s Channel Points Predictions. |

        Parameters
        ----------
        first: int
            The maximum number of predictions to retrieve per request.

        Yields
        ------
        AsyncGenerator[List[interaction.Prediction], None]
            A list of dictionaries representing the predictions for each page.
        """
        kwargs: Dict[str, Any] = {
            'broadcaster_id': self._user_id,
            'first': first,
            'after': None
        }
        while True:
            data: PData[List[interaction.Prediction]] = await self._state.http.get_predictions(**kwargs)
            yield data['data']
            kwargs['after'] = data['pagination'].get('cursor')
            if not kwargs['after']:
                break

    async def create_prediction(self,
                                title: str,
                                outcomes: List[str],
                                window: int) -> interaction.Prediction:
        """
        Create a new prediction for the broadcaster.

        | Scopes                       | Description                                     |
        | ---------------------------- | ------------------------------------------------|
        | `channel:manage:predictions` | Manage of channel’s Channel Points Predictions. |

        Parameters
        ----------
        title: str
            The title of the prediction.
        outcomes: List[str]
            A list of possible outcomes for the prediction.
        window: int
            The duration of the prediction window in seconds.

        Returns
        -------
        interaction.Prediction
            A dictionary representing the created prediction.
        """
        data: Data[List[interaction.Prediction]] = await self._state.http.create_prediction(self._user_id,
                                                                                            title,
                                                                                            outcomes,
                                                                                            window)
        return data['data'][0]

    @overload
    async def end_prediction(self,
                             prediction_id: str,
                             status: Literal['resolved'],
                             winning_outcome_id: str
                             ) -> interaction.Prediction:
        ...

    @overload
    async def end_prediction(self,
                             prediction_id: str,
                             status: Literal['canceled', 'locked'],
                             winning_outcome_id: None = None
                             ) -> interaction.Prediction:
        ...

    async def end_prediction(self,
                             prediction_id: str,
                             status: Any[Literal['resolved', 'canceled', 'locked']],
                             winning_outcome_id: Optional[str] = None) -> interaction.Prediction:
        """
        End an existing prediction with a specified status.

        | Scopes                       | Description                                     |
        | ---------------------------- | ------------------------------------------------|
        | `channel:manage:predictions` | Manage of channel’s Channel Points Predictions. |

        Parameters
        ----------
        prediction_id: str
            The ID of the prediction to end.
        status: Literal['resolved', 'canceled', 'locked']
            The status to set for the prediction.
        winning_outcome_id: Optional[str]
            The ID of the winning outcome if the status is 'resolved'.

        Returns
        -------
        interaction.Prediction
            A dictionary representing the updated prediction.
        """
        data: Data[List[interaction.Prediction]] = await self._state.http.end_prediction(self._user_id,
                                                                                         prediction_id,
                                                                                         status,
                                                                                         winning_outcome_id)
        return data['data'][0]

    async def get_polls(self, poll_ids: List[str]) -> List[interaction.Poll]:
        """
        Retrieve a list of polls by their IDs.

        | Scopes                 | Description               |
        | ---------------------- | --------------------------|
        | `channel:read:polls`   | View a channel’s polls.   |
        | `channel:manage:polls` | Manage a channel’s polls. |

        Parameters
        ----------
        poll_ids: List[str]
            A list of poll IDs to retrieve.

        Returns
        -------
        List[interaction.Poll]
            A list of dictionaries representing the polls.
        """
        data: PData[List[interaction.Poll]] = await self._state.http.get_polls(self._user_id,
                                                                               poll_ids,
                                                                               first=20)
        return data['data']

    async def fetch_polls(self, first: int = 20) -> AsyncGenerator[List[interaction.Poll], None]:
        """
        Fetch broadcaster polls.

        | Scopes                 | Description               |
        | ---------------------- | --------------------------|
        | `channel:read:polls`   | View a channel’s polls.   |
        | `channel:manage:polls` | Manage a channel’s polls. |

        Parameters
        ----------
        first: int
            The maximum number of polls to retrieve per request.

        Yields
        ------
        AsyncGenerator[List[interaction.Poll], None]
            A list of dictionaries representing the polls for each page.
        """
        kwargs: Dict[str, Any] = {
            'broadcaster_id': self._user_id,
            'first': first,
            'after': None
        }
        while True:
            data: PData[List[interaction.Poll]] = await self._state.http.get_polls(**kwargs)
            yield data['data']
            kwargs['after'] = data['pagination'].get('cursor')
            if not kwargs['after']:
                break

    async def create_poll(self,
                          title: str,
                          choices: List[str],
                          duration: int,
                          channel_points_voting_enabled: bool = False,
                          channel_points_per_vote: Optional[int] = None) -> interaction.Poll:
        """
        Create a new poll for the broadcaster.

        | Scopes                 | Description               |
        | ---------------------- | --------------------------|
        | `channel:manage:polls` | Manage a channel’s polls. |

        Parameters
        ----------
        title: str
            The title of the poll.
        choices: List[str]
            A list of choices for the poll.
        duration: int
            The duration of the poll in seconds.
        channel_points_voting_enabled: bool
            Whether channel points voting is enabled.
        channel_points_per_vote: Optional[int]
            The number of channel points required per vote if channel points voting is enabled.

        Returns
        -------
        interaction.Poll
            A dictionary representing the created poll.
        """
        data: Data[List[interaction.Poll]] = await self._state.http.create_poll(self._user_id,
                                                                                title,
                                                                                choices,
                                                                                duration,
                                                                                channel_points_voting_enabled,
                                                                                channel_points_per_vote)
        return data['data'][0]

    async def end_poll(self, poll_id: str, status: Literal['terminated', 'archived']) -> interaction.Poll:
        """
        End an existing poll with a specified status.

        | Scopes                 | Description               |
        | ---------------------- | --------------------------|
        | `channel:manage:polls` | Manage a channel’s polls. |

        Parameters
        ----------
        poll_id: str
            The ID of the poll to end.
        status: Literal['terminated', 'archived']
            The status to set for the poll, either 'terminated' or 'archived'.

        Returns
        -------
        interaction.Poll
            A dictionary representing the updated poll.
        """
        data: Data[List[interaction.Poll]] = await self._state.http.end_poll(self._user_id, poll_id, status)
        return data['data'][0]

    async def delete_videos(self, video_ids: List[str]) -> List[str]:
        """
        Delete a list of videos by their IDs.

        | Scopes                  | Description                |
        | ----------------------- | ---------------------------|
        | `channel:manage:videos` | Manage a channel’s videos. |

        Parameters
        ----------
        video_ids: List[str]
            A list of video IDs to delete.

        Returns
        -------
        List[str]
            A list of IDs of the deleted videos.
        """
        data: Data[List[str]] = await self._state.http.delete_videos(self._user_id, video_ids)
        return data['data']


class ClientChannel(BroadcasterChannel):
    """
    Represents a client-user channel.

    !!! Danger
        The attributes are read-only.
        These attributes are automatically updated via EventSub whenever channel information changes.

    Attributes
    ----------
    title: str
        The title of the channel.
    language: str
        The language of the broadcaster's content.
    category_id: str
        The ID of the category (game) associated with the channel.
    category_name: str
        The name of the category (game) associated with the channel.
    ccl: List[channels.CCL]
        A list of content classification labels associated with the channel.
    """

    __slots__ = ('title', 'language', 'category_id', 'category_name', 'ccl')

    def __init__(self, user_id: str, /, state: ConnectionState, data: channels.ChannelInfo) -> None:
        super().__init__(user_id, state=state)
        self._state: ConnectionState = state
        self.title: str = data['title']
        self.language: str = data['broadcaster_language']
        self.category_id: str = data['game_id']
        self.category_name: str = data['game_name']
        self.ccl: List[channels.CCL] = data['content_classification_labels']
