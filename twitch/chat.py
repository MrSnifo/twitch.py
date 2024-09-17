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
    from typing import Optional, Literal, List, Dict, Any, AsyncGenerator, Tuple
    from .types import Data, TData, Edata, chat, users, bits, moderation, PData
    from .state import ConnectionState
    from .user import User

__all__ = ('Chat', 'BroadcasterChat')


class Chat:
    """
    Represents a channel chat.
    """
    __slots__ = ('_state', '_user_id', '_auth_user_id')

    def __init__(self, user_id: str, auth_user_id: str, *, state: ConnectionState) -> None:
        self._state: ConnectionState = state
        self._user_id: str = user_id
        self._auth_user_id: str = auth_user_id

    async def get_settings(self) -> chat.Settings:
        """
        Retrieve the current chat settings for the broadcaster.

        ???+ note
            The scopes only required if you want to include non_moderator extra keys.

        | Scopes                           | Description                                |
        | -------------------------------- | -------------------------------------------|
        | `moderator:read:chat_settings`   | View a broadcaster’s chat room settings.   |
        | `moderator:manage:chat_settings` | Manage a broadcaster’s chat room settings. |

        Returns
        -------
        chat.Settings
            A dictionary containing chat settings for the broadcaster.
        """
        data: Data[List[chat.Settings]] = await self._state.http.get_chat_settings(self._user_id,
                                                                                   self._auth_user_id)
        return data['data'][0]


    async def get_shared_chat_session(self) -> Optional[chat.SharedChatSession]:
        """
        Retrieve the shared chat session details for the broadcaster.

        Returns
        -------
        chat.SharedChatSession
            A dictionary containing details about the shared chat session.
        """
        data: Data[List[chat.SharedChatSession]] = await self._state.http.get_shared_chat_session(self._auth_user_id,
                                                                                                  self._user_id)
        return data['data'][0] if len(data['data']) != 0 else None

    async def update_settings(self,
                              emote_mode: Optional[bool] = None,
                              follower_mode: Optional[bool] = None,
                              follower_mode_duration: Optional[int] = None,
                              non_moderator_chat_delay: Optional[bool] = None,
                              non_moderator_chat_delay_duration: Optional[int] = None,
                              slow_mode: Optional[bool] = None,
                              slow_mode_wait_time: Optional[int] = None,
                              subscriber_mode: Optional[bool] = None,
                              unique_chat_mode: Optional[bool] = None) -> chat.Settings:
        """
        Update the chat settings for the broadcaster.

        | Scopes                           | Description                                |
        | -------------------------------- | -------------------------------------------|
        | `moderator:manage:chat_settings` | Manage a broadcaster’s chat room settings. |

        Parameters
        ----------
        emote_mode: Optional[bool]
            Whether to enable emote-only mode.
        follower_mode: Optional[bool]
            Whether to enable follower-only mode.
        follower_mode_duration: Optional[int]
            Duration of the follower-only mode in minutes.
        non_moderator_chat_delay: Optional[bool]
            Whether to enable chat delay for non-moderators.
        non_moderator_chat_delay_duration: Optional[int]
            Duration of the chat delay for non-moderators in seconds.
        slow_mode: Optional[bool]
            Whether to enable slow mode.
        slow_mode_wait_time: Optional[int]
            The duration of the slow mode in seconds.
        subscriber_mode: Optional[bool]
            Whether to enable subscriber-only mode.
        unique_chat_mode: Optional[bool]
            Whether to enable unique chat mode.

        Returns
        -------
        chat.Settings
            A dictionary containing the updated chat settings.
        """
        kwargs: Dict[str, Any] = {
            'emote_mode': emote_mode,
            'follower_mode': follower_mode,
            'follower_mode_duration': follower_mode_duration if follower_mode else None,
            'non_moderator_chat_delay': non_moderator_chat_delay,
            'non_moderator_chat_delay_duration': (non_moderator_chat_delay_duration
                                                  if non_moderator_chat_delay else None),
            'slow_mode': slow_mode,
            'slow_mode_wait_time': slow_mode_wait_time if slow_mode else None,
            'subscriber_mode': subscriber_mode,
            'unique_chat_mode': unique_chat_mode
        }
        data: Data[List[chat.Settings]] = await self._state.http.update_chat_settings(self._user_id,
                                                                                      self._auth_user_id,
                                                                                      **kwargs)
        return data['data'][0]

    async def get_total_chatters(self) -> int:
        """
        Get the total number of chatters in the broadcaster's chat.

        | Scopes                    | Description                                     |
        | ------------------------- | ------------------------------------------------|
        | `moderator:read:chatters` | View the chatters in a broadcaster’s chat room. |

        Returns
        -------
        int
            The total number of chatters.
        """
        data: TData[List[users.SpecificUser]] = await self._state.http.get_chatters(self._user_id,
                                                                                    self._auth_user_id,
                                                                                    first=1)
        return data['total']

    async def fetch_chatters(self, *, first: int = 100) -> AsyncGenerator[List[users.SpecificUser], None]:
        """
        Fetch a list of chatters in the broadcaster's chat.

        | Scopes                    | Description                                     |
        | ------------------------- | ------------------------------------------------|
        | `moderator:read:chatters` | View the chatters in a broadcaster’s chat room. |

        Parameters
        ----------
        first: int
            The number of chatters to fetch per request.

        Yields
        ------
        AsyncGenerator[List[users.SpecificUser], None]
            A list of dictionaries representing chatters.
        """
        kwargs: Dict[str, Any] = {
            'broadcaster_id': self._user_id,
            'moderator_id': self._auth_user_id,
            'first': first,
            'after': None
        }
        while True:
            data: TData[List[users.SpecificUser]] = await self._state.http.get_chatters(**kwargs)
            yield data['data']
            kwargs['after'] = data['pagination'].get('cursor')
            if not kwargs['after']:
                break

    async def get_emotes(self) -> Tuple[List[chat.Emote], str]:
        """
        Retrieve the emotes and template for the broadcaster's channel.

        | Scopes                    | Description                                     |
        | ------------------------- | ------------------------------------------------|
        | `moderator:read:chatters` | View the chatters in a broadcaster’s chat room. |

        Returns
        -------
        Tuple[List[chat.Emote], str]
            A tuple where the first element is a list of dictionaries representing emotes,
            and the second element is a string representing the template.
        """
        data: Edata[List[chat.Emote]] = await self._state.http.get_channel_emotes(self._auth_user_id, self._user_id)
        return data['data'], data['template']

    async def get_cheermotes(self) -> List[bits.Cheermote]:
        """
        Retrieve the cheermotes for the broadcaster's channel.

        Returns
        -------
        List[bits.Cheermote]
            A list of dictionaries representing cheermotes.
        """
        data: Data[List[bits.Cheermote]] = await self._state.http.get_cheermotes(self._auth_user_id, self._user_id)
        return data['data']

    async def get_badges(self) -> List[chat.Badge]:
        """
        Retrieve the chat badges for the broadcaster's channel.

        Returns
        -------
        List[chat.Badge]
            A list of dictionaries representing chat badges.
        """
        data: Data[List[chat.Badge]] = await self._state.http.get_channel_chat_badges(self._auth_user_id, self._user_id)
        return data['data']

    async def send_shoutout(self, user: User) -> None:
        """
        Send a shoutout to another broadcaster.

        | Scopes                       | Description                       |
        | ---------------------------- | ----------------------------------|
        | `moderator:manage:shoutouts` | Manage a broadcaster’s shoutouts. |

        Parameters
        ----------
        user: User
            The user to send a shoutout to.
        """
        await self._state.http.send_a_shoutout(self._user_id, self._auth_user_id, to_broadcaster_id=user.id)

    async def send_announcement(self,
                                message: str,
                                *,
                                color: Literal['blue', 'green', 'orange', 'purple', 'primary'] = 'primary'):
        """
        Send an announcement message to the chat.

        | Scopes                           | Description                                                       |
        | -------------------------------- | ------------------------------------------------------------------|
        | `moderator:manage:announcements` | Send announcements in channels where you have the moderator role. |

        Parameters
        ----------
        message: str
            The announcement message to send.
        color: Literal['blue', 'green', 'orange', 'purple', 'primary']
            The color of the announcement message.
        """
        await self._state.http.send_chat_announcement(self._user_id, self._auth_user_id, message=message, color=color)

    async def warn_user(self, user: User, reason: str) -> None:
        """
        Send a warning to a user in the chat.

        | Scopes                      | Description                                               |
        | --------------------------- | ----------------------------------------------------------|
        | `moderator:manage:warnings` | Warn users in channels where you have the moderator role. |

        Parameters
        ----------
        user: User
            The user to warn.
        reason: str
            The reason for the warning.
        """
        await self._state.http.warn_chat_user(self._user_id, self._auth_user_id, user_id=user.id, reason=reason)

    async def send_message(self, text: str, reply_message_id: Optional[str] = None) -> chat.SendMessageStatus:
        """
        Send a message to the chat.

        ???+ warning
            It's strongly discouraged to send messages to other channels without the owner's permission.
            Doing so could result in a permanent ban from twitch. Please be cautious.

        | Scopes           | Description                                                     |
        | ---------------- | ----------------------------------------------------------------|
        | `user:read:chat` | Join a specified chat channel as your user and appear as a bot. |

        Parameters
        ----------
        text: str
            The message text to send.
        reply_message_id: Optional[str]
            The ID of the message to reply to.

        Returns
        -------
        chat.SendMessageStatus
            A dictionary containing the status of the user sent message.
        """
        data: Data[List[chat.SendMessageStatus]] = await self._state.http.send_chat_message(
            self._user_id,
            self._auth_user_id,
            text=text,
            reply_parent_message_id=reply_message_id)
        return data['data'][0]

    async def delete_message(self, msg_id: str) -> None:
        """
        Delete a message from the chat.

        | Scopes                           | Description                                                         |
        | -------------------------------- | --------------------------------------------------------------------|
        | `moderator:manage:chat_messages` | Delete chat messages in channels where you have the moderator role. |

        Parameters
        ----------
        msg_id: str
            The ID of the message to delete.
        """
        await self._state.http.delete_chat_messages(self._user_id, self._auth_user_id, message_id=msg_id)

    async def clear_chat(self) -> None:
        """
        Clear all messages from the chat.

        | Scopes                           | Description                                                         |
        | -------------------------------- | --------------------------------------------------------------------|
        | `moderator:manage:chat_messages` | Delete chat messages in channels where you have the moderator role. |
        """
        await self._state.http.delete_chat_messages(self._user_id, self._auth_user_id)

    async def get_shieldmode(self) -> moderation.ShieldModeStatus:
        """
        Retrieve the current shield mode status for the broadcaster's channel.

        | Scopes                         | Description                                |
        | ------------------------------ | -------------------------------------------|
        | `moderator:read:shield_mode`   | View a broadcaster’s Shield Mode status.   |
        | `moderator:manage:shield_mode` | Manage a broadcaster’s Shield Mode status. |


        Returns
        -------
        moderation.ShieldModeStatus
            A dictionary representing the shield mode status.
        """
        data: Data[List[moderation.ShieldModeStatus]] = await self._state.http.get_shield_mode_status(
            self._user_id,
            self._auth_user_id)
        return data['data'][0]

    async def update_shieldmode(self, activate: bool) -> moderation.ShieldModeStatus:
        """
        Update the shield mode status for the broadcaster's channel.

        | Scopes                         | Description                                |
        | ------------------------------ | -------------------------------------------|
        | `moderator:manage:shield_mode` | Manage a broadcaster’s Shield Mode status. |

        Parameters
        ----------
        activate: bool
            Whether to activate or deactivate shield mode.

        Returns
        -------
        moderation.ShieldModeStatus
            A dictionary representing the updated shield mode status.
        """
        data: Data[List[moderation.ShieldModeStatus]] = await self._state.http.update_shield_mode_status(
            self._user_id,
            self._auth_user_id,
            is_active=activate)
        return data['data'][0]

    async def get_automod_settings(self) -> moderation.AutoModSettings:
        """
        Retrieve the current AutoMod settings for the broadcaster's channel.

        | Scopes                              | Description                              |
        | ----------------------------------- | -----------------------------------------|
        | `moderator:read:automod_settings`   | View a broadcaster’s AutoMod settings.   |
        | `moderator:manage:automod_settings` | Manage a broadcaster’s AutoMod settings. |

        Returns
        -------
        moderation.AutoModSettings
            A dictionary representing the AutoMod settings.
        """
        data: Data[List[moderation.AutoModSettings]] = await self._state.http.get_automod_settings(self._user_id,
                                                                                                   self._auth_user_id)
        return data['data'][0]

    async def update_automod_settings(self,
                                      aggression: Optional[int] = None,
                                      bullying: Optional[int] = None,
                                      disability: Optional[int] = None,
                                      misogyny: Optional[int] = None,
                                      race_ethnicity_or_religion: Optional[int] = None,
                                      sex_based_terms: Optional[int] = None,
                                      sexuality_sex_or_gender: Optional[int] = None,
                                      swearing: Optional[int] = None) -> moderation.AutoModSettings:
        """
        Update the AutoMod settings for the broadcaster's channel.

        | Scopes                              | Description                              |
        | ----------------------------------- | -----------------------------------------|
        | `moderator:manage:automod_settings` | Manage a broadcaster’s AutoMod settings. |

        Parameters
        ----------
        aggression: Optional[int]
            The level of aggression moderation.
        bullying: Optional[int]
            The level of bullying moderation.
        disability: Optional[int]
            The level of disability-related moderation.
        misogyny: Optional[int]
            The level of misogyny moderation.
        race_ethnicity_or_religion: Optional[int]
            The level of race, ethnicity, or religion-related moderation.
        sex_based_terms: Optional[int]
            The level of sex-based terms moderation.
        sexuality_sex_or_gender: Optional[int]
            The level of sexuality, sex, or gender-related moderation.
        swearing: Optional[int]
            The level of swearing moderation.

        Returns
        -------
        moderation.AutoModSettings
            A dictionary representing the updated AutoMod settings.
        """
        kwargs: Dict[str, Any] = {
            'aggression': aggression,
            'bullying': bullying,
            'disability': disability,
            'misogyny': misogyny,
            'race_ethnicity_or_religion': race_ethnicity_or_religion,
            'sex_based_terms': sex_based_terms,
            'sexuality_sex_or_gender': sexuality_sex_or_gender,
            'swearing': swearing
        }
        data: Data[List[moderation.AutoModSettings]] = await self._state.http.update_automod_settings(
            self._user_id,
            self._auth_user_id,
            **kwargs)
        return data['data'][0]

    async def update_automod_settings_level(self, overall_level: int) -> moderation.AutoModSettings:
        """
        Update the overall AutoMod settings level for the broadcaster's channel.

        | Scopes                              | Description                              |
        | ----------------------------------- | -----------------------------------------|
        | `moderator:manage:automod_settings` | Manage a broadcaster’s AutoMod settings. |

        Parameters
        ----------
        overall_level: int
            The new overall AutoMod settings level.

        Returns
        -------
        moderation.AutoModSettings
            A dictionary representing the updated AutoMod settings.
        """
        data: Data[List[moderation.AutoModSettings]] = await self._state.http.update_automod_settings(
            self._user_id,
            self._auth_user_id,
            overall_level=overall_level)
        return data['data'][0]

    async def automod_held_message(self, message_id: str, action: Literal['allow', 'deny']) -> None:
        """
        Manage a held AutoMod message by either allowing or denying it.

        | Scopes                     | Description                                 |
        | -------------------------- | --------------------------------------------|
        | `moderator:manage:automod` | Manage messages held for review by AutoMod. |

        Parameters
        ----------
        message_id: str
            The ID of the message to manage.

        action: Literal['allow', 'deny']
            The action to perform on the held message; either 'allow' or 'deny'.
        """
        await self._state.http.manage_held_automod_messages(self._auth_user_id, message_id, action)

    async def fetch_blocked_terms(self, first: int = 100) -> AsyncGenerator[List[moderation.BlockedTerm], None]:
        """
        Retrieve blocked terms for the broadcaster's channel in pages.

        | Scopes                           | Description                                   |
        | -------------------------------- | ----------------------------------------------|
        | `moderator:read:blocked_terms`   | View a broadcaster’s list of blocked terms.   |
        | `moderator:manage:blocked_terms` | Manage a broadcaster’s list of blocked terms. |

        Parameters
        ----------
        first: int
            The maximum number of blocked terms to retrieve per page.

        Yields
        ------
        AsyncGenerator[List[moderation.BlockedTerm], None]
            A list of dictionaries, each representing a blocked term.
        """
        kwargs: Dict[str, Any] = {
            'broadcaster_id': self._user_id,
            'moderator_id': self._auth_user_id,
            'first': first,
            'after': None
        }
        while True:
            data: PData[List[moderation.BlockedTerm]] = await self._state.http.get_blocked_terms(**kwargs)
            yield data['data']
            kwargs['after'] = data['pagination'].get('cursor')
            if not kwargs['after']:
                break

    async def add_blocked_term(self, text: str) -> moderation.BlockedTerm:
        """
        Add a term to the list of blocked terms for the broadcaster's channel.

        | Scopes                           | Description                                   |
        | -------------------------------- | ----------------------------------------------|
        | `moderator:manage:blocked_terms` | Manage a broadcaster’s list of blocked terms. |

        Parameters
        ----------
        text: str
            The term to be blocked.

        Returns
        -------
        moderation.BlockedTerm
            A dictionary representing the blocked term that was added.
        """
        data: Data[List[moderation.BlockedTerm]] = await self._state.http.add_blocked_term(self._user_id,
                                                                                           self._auth_user_id,
                                                                                           text=text)
        return data['data'][0]

    async def remove_blocked_term(self, term_id: str) -> None:
        """
        Remove a term from the list of blocked terms for the broadcaster's channel.

        | Scopes                           | Description                                   |
        | -------------------------------- | ----------------------------------------------|
        | `moderator:manage:blocked_terms` | Manage a broadcaster’s list of blocked terms. |

        Parameters
        ----------
        term_id: str
            The ID of the blocked term to be removed.
        """
        await self._state.http.remove_blocked_term(self._user_id, self._auth_user_id, term_id=term_id)


class BroadcasterChat(Chat):
    """
    Represents a Broadcaster channel chat.
    """
    __slots__ = ()

    def __init__(self, user_id: str, *, state: ConnectionState) -> None:
        super().__init__(user_id, user_id, state=state)

    async def automod_check_messages(self, messages: List[str]) -> List[moderation.AutoModMessageStatus]:
        """
        Check the AutoMod status of multiple messages.

        | Scopes            | Description                  |
        | ----------------- | -----------------------------|
        | `moderation:read` | View a channel’s moderation. |

        Parameters
        ----------
        messages: List[str]
            A list of messages to check.

        Returns
        -------
        List[moderation.AutoModMessageStatus]
            A list of dictionaries, each representing the AutoMod status of a message.
        """
        data: Data[List[moderation.AutoModMessageStatus]] = await self._state.http.check_automod_status(
            self._state.user.id,
            messages)
        return data['data']
