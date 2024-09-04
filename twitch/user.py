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

from .channel import Channel, BroadcasterChannel, ClientChannel
from typing import TYPE_CHECKING, overload
from .utils import convert_rfc3339
from datetime import datetime

if TYPE_CHECKING:
    from .types import users, PData, chat, Data, PEdata, activity, channels, streams, TData
    from typing import Optional, Dict, Any, Tuple, List, AsyncGenerator, Literal, Union
    from .state import ConnectionState

__all__ = ('User', 'Broadcaster', 'ClientUser')


class BaseUser:
    """
    Represents base class of user.

    Attributes
    ----------
    id: str
        The unique identifier for the user.
    """
    __slots__ = ('id',)

    if TYPE_CHECKING:
        id: str

    def __init__(self, user_id: str) -> None:
        self._update(user_id=user_id)

    def __repr__(self) -> str:
        # Return a string representation of the BaseUser instance.
        return f'<BaseUser id={self.id}>'

    def __eq__(self, other: object) -> bool:
        """
        Check if this user is equal to another user by comparing IDs.

        Parameters
        ----------
        other: object
            The object to compare with.

        Returns
        -------
        bool
            True if the other object is a BaseUser with the same ID, False otherwise.
        """
        if isinstance(other, BaseUser):
            return self.id == other.id
        return False

    def __ne__(self, other: object) -> bool:
        """
        Check if this user is not equal to another user.

        Parameters
        ----------
        other: object
            The object to compare with.

        Returns
        -------
        bool
            True if the other object is not a BaseUser or has a different ID, False otherwise.
        """
        return not self.__eq__(other)

    def _update(self, user_id: str) -> None:
        # Update the user's ID.
        self.id = user_id


class User(BaseUser):
    """
    Represents a user with additional functionality.

    Attributes
    ----------
    id: str
        The unique identifier for the user.
    """
    __slots__ = ('_state',  '_auth_user_id', '__weakref__')

    def __init__(self, user_id: str, auth_user_id: str, *, state: ConnectionState) -> None:
        super().__init__(user_id=user_id)
        self._state: ConnectionState = state
        self._auth_user_id: str = auth_user_id

    @property
    def channel(self) -> Channel:
        """
        Get the channel associated with this user.

        Returns
        -------
        Channel
            The channel object representing the user's channel.
        """
        return Channel(self.id, self._auth_user_id, state=self._state)

    async def get_info(self) -> users.User:
        """
        Retrieve the full information about the user.

        Returns
        -------
        users.User
            A dictionary containing the user's information.
        """
        data: Data[List[users.User]] = await self._state.http.get_users(self._auth_user_id,
                                                                        user_ids=[self.id])
        return data['data'][0]

    async def get_chat_color(self) -> str:
        """
        Retrieve the chat color associated with the user.

        Returns
        -------
        str
            The hexadecimal color code representing the user's chat color.
        """
        data: Data[List[chat.UserChatColor]] = await self._state.http.get_user_chat_color(self._auth_user_id,
                                                                                          user_ids=[self.id])
        return data['data'][0]['color']


class Broadcaster(User):
    """
    Represents a broadcaster.

    Attributes
    ----------
    id: str
        The unique identifier for the broadcaster.
    """
    __slots__ = ()

    def __init__(self, user_id: str, *, state: ConnectionState) -> None:
        super().__init__(user_id, user_id, state=state)

    @property
    def channel(self) -> BroadcasterChannel:
        """
        Retrieve the broadcaster channel.

        Returns
        -------
        Optional[BroadcasterChannel]
            The channel of the current user.
        """
        return BroadcasterChannel(self.id, state=self._state)

    async def update(self, description: Optional[str]) -> users.User:
        """
        Update the user's profile information.

        | Scopes      | Description           |
        | ----------- | ----------------------|
        | `user:edit` | Manage a user object. |

        Parameters
        ----------
        description: Optional[str]
            The new description to set for the user, by default None.

        Returns
        -------
        users.User
            The updated `users.User` object with the new description.
        """
        data: Data[List[users.User]] = await self._state.http.update_user(self.id, description)
        return data['data'][0]

    async def fetch_emotes(self, user: Optional[User] = None) -> AsyncGenerator[Tuple[List[chat.Emote], str], None]:
        """
        Fetch emotes associated with the user or broadcaster.

        | Scopes            | Description                      |
        | ----------------- | ---------------------------------|
        | `user:read:emote` | View emotes available to a user. |

        Parameters
        ----------
        user: Optional[User]
            The user whose emotes to retrieve. If None, retrieves emotes for the broadcaster.

        Yields
        ------
        AsyncGenerator[Tuple[List[chat.Emote], str], None]
            A tuple where the first element is a list of `chat.Emote` dictionaries, and the second
            element is the template used for the emotes.
        """
        kwargs: Dict[str, Any] = {
            'user_id': self.id,
            'broadcaster_id': user.id if user else self.id,
            'after': None
        }
        while True:
            data: PEdata[List[chat.Emote]] = await self._state.http.get_user_emotes(**kwargs)
            yield data['data'], data['template']
            kwargs['after'] = data['pagination'].get('cursor')
            if not kwargs['after']:
                break

    async def fetch_drops_entitlements(self,
                                       entitlement_ids: Optional[List[str]] = None,
                                       game_id: Optional[str] = None,
                                       fulfillment_status: Optional[Literal['claimed', 'fulfilled']] = None,
                                       first: int = 200) -> AsyncGenerator[List[activity.Entitlement], None]:
        """
        Fetch drop entitlements for the user.

        Parameters
        ----------
        entitlement_ids: Optional[List[str]]
            A list of entitlement IDs to filter by, by default None.
        game_id: Optional[str]
            The game ID to filter entitlements by, by default None.
        fulfillment_status: Optional[Literal['claimed', 'fulfilled']]
            The fulfillment status to filter by, by default None.
        first: int
            The maximum number of entitlements to retrieve per request, by default 200.

        Yields
        ------
        AsyncGenerator[List[activity.Entitlement], None]
            A list of `activity.Entitlement` dictionaries representing the entitlements.
        """
        kwargs: Dict[str, Any] = {
            'entitlement_ids': entitlement_ids,
            'user_id': self.id,
            'game_id': game_id,
            'fulfillment_status': fulfillment_status,
            'first': first,
            'after': None
        }
        while True:
            data: PData[List[activity.Entitlement]] = await self._state.http.get_drops_entitlements(**kwargs)
            yield data['data']
            kwargs['after'] = data['pagination'].get('cursor')
            if not kwargs['after']:
                break

    async def update_drops_entitlements(self,
                                        entitlement_ids: List[str],
                                        fulfillment_status: Literal['claimed', 'fulfilled']
                                        ) -> List[activity.EntitlementsUpdate]:
        """
        Update the fulfillment status of drop entitlements.

        Parameters
        ----------
        entitlement_ids: List[str]
            A list of entitlement IDs to be updated.
        fulfillment_status: Literal['claimed', 'fulfilled']
            The new fulfillment status to set for the entitlements.

        Returns
        -------
        List[activity.EntitlementsUpdate]
            A list of `activity.EntitlementsUpdate` dictionaries representing the updated entitlements.
        """
        data: Data[List[activity.EntitlementsUpdate]] = await self._state.http.update_drops_entitlements(
            self.id,
            entitlement_ids,
            fulfillment_status)
        return data['data']

    async def update_chat_color(self, color: Union[str, chat.UserChatColors]) -> None:
        """
        Update the user's chat color.

        | Scopes                   | Description                                        |
        | ------------------------ | ---------------------------------------------------|
        | `user:manage:chat_color` | Update the color used for the user’s name in chat. |

        ???+ note
            To specify a color using a hexadecimal code, the user must have Turbo or Prime status.

        Parameters
        ----------
        color: Union[str, chat.UserChatColors]
            The new color to set for the user's chat messages. Can be a color code or a predefined color.
        """
        await self._state.http.update_user_chat_color(self.id, color)

    async def block(self,
                    user: User,
                    source_context: Literal['chat', 'whisper'] = None,
                    reason: Literal['harassment', 'spam', 'other'] = None) -> None:
        """
        Block a specified user.

        | Scopes                      | Description                      |
        | --------------------------- | ---------------------------------|
        | `user:manage:blocked_users` | Manage the block list of a user. |

        Parameters
        ----------
        user: User
            The user to block.
        source_context: Literal['chat', 'whisper']
            The context in which the block is applied, by default None.
        reason: Literal['harassment', 'spam', 'other']
            The reason for blocking the user, by default None.
        """
        await self._state.http.block_user(self.id, user.id, source_context, reason)

    async def unblock(self, user: User) -> None:
        """
        Unblock a previously blocked user.

        | Scopes                      | Description                      |
        | --------------------------- | ---------------------------------|
        | `user:manage:blocked_users` | Manage the block list of a user. |

        Parameters
        ----------
        user: User
            The user to unblock.
        """
        await self._state.http.unblock_user(self.id, user.id)

    async def fetch_blocked_users(self, first: int = 100) -> AsyncGenerator[List[users.SpecificUser], None]:
        """
        Fetch the list of users blocked by the broadcaster.

        | Scopes                    | Description                    |
        | ------------------------- | -------------------------------|
        | `user:read:blocked_users` | View the block list of a user. |

        Parameters
        ----------
        first: int
            The maximum number of results to retrieve per page, by default 100.

        Yields
        ------
        AsyncGenerator[List[users.SpecificUser], None]
            A list of dictionaries representing the blocked users.
        """
        kwargs: Dict[str, Any] = {
            'broadcaster_id': self.id,
            'first': first,
            'after': None
        }
        while True:
            data: PData[List[users.SpecificUser]] = await self._state.http.get_user_block_list(**kwargs)
            yield data['data']
            kwargs['after'] = data['pagination'].get('cursor')
            if not kwargs['after']:
                break

    async def whisper(self, user: User, message: str) -> None:
        """
        Send a whisper message to a specified user.

        !!! Warning
            This action requires a verified phone number.

        | Scopes                 | Description                                                                  |
        | ---------------------- | -----------------------------------------------------------------------------|
        | `user:manage:whispers` | Receive whispers sent to your user, and send whispers on your user’s behalf. |

        Parameters
        ----------
        user: User
            The user to whom the whisper message will be sent.
        message: str
            The content of the whisper message.
        """
        await self._state.http.send_whisper(self.id, user.id, message)

    @overload
    async def check_followed(self, user: User) -> channels.Follows:
        ...

    @overload
    async def check_followed(self, user: User) -> None:
        ...

    async def check_followed(self, user: User) -> Optional[channels.Follows]:
        """
        Check if the broadcaster is following a specified user.

        | Scopes              | Description                               |
        | ------------------- | ------------------------------------------|
        | `user:read:follows` | View the list of channels a user follows. |

        Parameters
        ----------
        user: User
            The user to check for a follow relationship.

        Returns
        -------
        Optional[channels.Follows]
            A dictionary if the broadcaster follows the specified user; otherwise, None.
        """
        data: TData[List[channels.Follows]] = await self._state.http.get_followed_channels(self.id,
                                                                                           broadcaster_id=user.id)
        return data['data'][0] if len(data['data']) != 0 else None

    async def get_total_followed(self) -> int:
        """
        Retrieve the total number of channels followed by the broadcaster.

        | Scopes              | Description                               |
        | ------------------- | ------------------------------------------|
        | `user:read:follows` | View the list of channels a user follows. |

        Returns
        -------
        int
            The total number of channels followed by the broadcaster.
        """
        data: TData[List[channels.Follows]] = await self._state.http.get_followed_channels(self.id, first=1)
        return data['total']

    async def fetch_followed(self, first: int = 100) -> AsyncGenerator[List[channels.Follows], None]:
        """
        Fetch the list of channels followed by the broadcaster.

        | Scopes              | Description                               |
        | ------------------- | ------------------------------------------|
        | `user:read:follows` | View the list of channels a user follows. |

        Parameters
        ----------
        first: int
            The maximum number of results to retrieve per page, by default 100.

        Yields
        ------
        AsyncGenerator[List[channels.Follows], None]
            A list of dictionaries representing the followed channels.
        """
        kwargs: Dict[str, Any] = {
            'user_id': self.id,
            'first': first,
            'after': None
        }
        while True:
            data: TData[List[channels.Follows]] = await self._state.http.get_followed_channels(**kwargs)
            yield data['data']
            kwargs['after'] = data['pagination'].get('cursor')
            if not kwargs['after']:
                break

    async def fetch_followed_streaming(self, first: int = 100) -> AsyncGenerator[List[streams.StreamInfo], None]:
        """
        Fetch the list of currently streaming channels followed by the broadcaster.

        | Scopes              | Description                               |
        | ------------------- | ------------------------------------------|
        | `user:read:follows` | View the list of channels a user follows. |

        Parameters
        ----------
        first: int
            The maximum number of results to retrieve per page, by default 100.

        Yields
        ------
        AsyncGenerator[List[streams.Stream], None]
            A list of dictionaries representing the streams from followed channels.
        """
        kwargs: Dict[str, Any] = {
            'user_id': self.id,
            'first': first,
            'after': None
        }
        while True:
            data: PData[List[streams.StreamInfo]] = await self._state.http.get_followed_streams(**kwargs)
            yield data['data']
            kwargs['after'] = data['pagination'].get('cursor')
            if not kwargs['after']:
                break

    @overload
    async def check_user_subscription(self, user: User) -> channels.SubscriptionCheck:
        ...

    @overload
    async def check_user_subscription(self, user: User) -> None:
        ...

    async def check_user_subscription(self, user: User) -> Optional[channels.SubscriptionCheck]:
        """
        Check if the broadcaster is subscribed to the specified user.

        | Scopes                    | Description                                                    |
        | ------------------------- | ---------------------------------------------------------------|
        | `user:read:subscriptions` | View if an authorized user is subscribed to specific channels. |

        Parameters
        ----------
        user: User
            The user to check for a subscription relationship.

        Returns
        -------
        Optional[channels.SubscriptionCheck]
            A dictionary representing if the broadcaster is subscribed to the specified user; otherwise, None.
        """
        data: Data[List[channels.SubscriptionCheck]] = await self._state.http.check_user_subscription(self.id, user.id)
        return data['data'][0] if len(data['data']) != 0 else None

    async def fetch_moderated_channels(self, first: int = 100) -> AsyncGenerator[List[users.Broadcaster], None]:
        """
        Fetch the list of channels moderated by the broadcaster.

        | Scopes                         | Description                                                 |
        | ------------------------------ | ------------------------------------------------------------|
        | `user:read:moderated_channels` | Read the list of channels you have moderator privileges in. |

        Parameters
        ----------
        first: int
            The maximum number of results to retrieve per page, by default 100.

        Yields
        ------
        AsyncGenerator[List[users.Broadcaster], None]
            A list of dictionaries representing the channels moderated by the broadcaster.
        """
        kwargs: Dict[str, Any] = {
            'user_id': self.id,
            'first': first,
            'after': None
        }
        while True:
            data: PData[List[users.Broadcaster]] = await self._state.http.get_moderated_channels(**kwargs)
            yield data['data']
            kwargs['after'] = data['pagination'].get('cursor')
            if not kwargs['after']:
                break


class ClientUser(Broadcaster):
    """
    Represents a user associated with the client.

    !!! Danger
        The attributes are read-only.
        These attributes are automatically updated via EventSub whenever user information changes.

    Attributes
    ----------
    id: str
        The unique identifier for the user.
    name: str
        The login name of the user.
    display_name: str
        The display name of the user.
    description: str
        A brief description or bio of the user.
    email: Optional[str]
        The email address of the user, if available and accessible. Requires `user:read:email` scope.
    joined_at: datetime
        The date and time when the user joined Twitch.
    """

    __slots__ = ('_channel_data', 'name', 'display_name', 'description', 'joined_at', 'email')

    def __init__(self,
                 *,
                 state: ConnectionState,
                 user_data: users.User,
                 channel_data: channels.ChannelInfo,
                 ) -> None:
        super().__init__(user_data['id'], state=state)
        self._channel_data: channels.ChannelInfo = channel_data
        self.name: str = user_data['login']
        self.display_name: str = user_data['display_name']
        self.description: str = user_data['description']
        self.joined_at: datetime = convert_rfc3339(user_data['created_at'])
        # Requires user:read:email scope
        self.email: Optional[str] = user_data.get('email') or None

    @property
    def channel(self) -> ClientChannel:
        """
        Retrieve the client-user channel.

        Returns
        -------
        Optional[broadcasterChannel]
            The channel of the current user.
        """
        return ClientChannel(self.id, state=self._state, data=self._channel_data)

    async def update(self, description: Optional[str]) -> users.User:
        """
        Update the user's profile information.

        | Scopes      | Description           |
        | ----------- | ----------------------|
        | `user:edit` | Manage a user object. |

        Parameters
        ----------
        description: Optional[str]
            The new description to set for the user, by default None.

        Returns
        -------
        users.User
            The updated `users.User` object with the new description.
        """
        data: Data[List[users.User]] = await self._state.http.update_user(self.id, description)
        self.description = data['data'][0]['description']
        return data['data'][0]
