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

from .channel import (Schedule, ScheduleSegment, Video, Clip, BannedUser, ChannelExtensions, Extension,
                      Extensions, Follow, Charity, CharityDonation, UserChannel, Editor, BitsLeaderboard,
                      ChannelSchedule, Subscription)
from .stream import ChannelStream, Stream, Category
from .reward import BaseReward, Redemption, Reward
from .chat import ChannelChat, ChannelAutoMod
from .user import BaseUser, User, UserEmail
from .prediction import Prediction, Outcome
from .alerts import Goal, HypeTrain
from .utils import convert_rfc3339
from .errors import BadRequest
from .errors import NotFound
from .utils import MISSING
from .poll import Poll
from time import time

from typing import TYPE_CHECKING, overload
if TYPE_CHECKING:
    from typing import Union, Optional, AsyncGenerator, List, Literal, Tuple
    from .types import channel as ChannelTypes
    from .types import user as UserTypes
    from .types import chat as ChatTypes
    from .state import ConnectionState
    from datetime import datetime

__all__ = ('ClientColor', 'ClientUser',
           'ClientCharity',
           'ClientPoll', 'ClientPrediction',
           'ClientReward', 'ClientRewardRedemption',
           'ClientModerators', 'ClientVips',
           'ClientExtensions',
           'ClientSchedule',
           'ClientChat', 'ClientAutoMod',
           'ClientStream',
           'ClientChannel')


# -------------------------------
#         + Client User +
# -------------------------------
class ClientColor:
    """
    Represents the chat color of the client.

    !!! warning
        The only way to access this class is through [ClientUser][twitch.broadcaster.ClientUser].
    """
    __slots__ = ('_id', '__state')

    def __init__(self, state: ConnectionState, user_id: str):
        self._id: str = user_id
        self.__state: state = state

    async def get(self) -> Optional[str]:
        """
        Retrieve the chat color of the client.

        Returns:
            Optional[str]: The chat color of the user or None if it has not been set.
        """
        data = await self.__state.http.get_users_chat_color(user_ids=[self._id])
        return data[0]

    @overload
    async def update(self, color: ChatTypes.UserColors) -> None:
        ...

    @overload
    async def update(self, color: str) -> None:
        ...

    async def update(self, color: Union[str, ChatTypes.UserColors]) -> None:
        """
        Updates the chat color of the client.

        ???+ warning "Color Specification"
            To specify a color using a hexadecimal code, the user must have Turbo or Prime status.

        | Scopes                   | Description                    |
        | ------------------------ | -------------------------------|
        | `user:manage:chat_color` | Update chat color.             |

        Parameters
        ----------
        color: Union[str, UserTypes.UserColors]:
            The color to set for the user's chat.

            Accepted color names: `blue`, `blue_violet`, `cadet_blue`, `chocolate`, `coral`, `dodger_blue`,
            `firebrick`, `golden_rod`, `green`, `hot_pink`, `orange_red`, `red`, `sea_green`, `spring_green`,
            `yellow_green`.

            Alternatively, you can specify a color using a hexadecimal code.

            Turbo and Prime users are allowed to use hexadecimal codes.

        Raises
        ------
        BadRequest
            * The color query parameter is required.
            * The named color in the color query parameter is not valid.
            * To specify a Hex color code, the user must be a Turbo or Prime user.
        Unauthorized
            * The user access token must include the user:manage:chat_color scope.
        """
        await self.__state.http.update_user_chat_color(user_id=self._id, color=color)


class ClientUser(BaseUser):
    """
    Represents a client user.

    !!! Danger
        The attributes are read-only.

        These attributes are automatically updated via EventSub whenever user information changes.

        Additional requests are unnecessary to fetch basic user information.

        To obtain additional information, such as `type`, `broadcaster_type`,
        and `images`, use the `get_info()` method.

    Attributes
    ----------
    email: Optional[UserEmail]
        The verified email address of the client.
    description: str
        The description (bio) of the client.
    joined_at: datetime
        The UTC date and time when the user’s account was created.
    """
    __slots__ = ('_state', 'email', 'joined_at', 'description')

    def __init__(self, state: ConnectionState, data: UserTypes.User) -> None:
        super().__init__(data=data)
        self._state: ConnectionState = state
        self.email: Optional[UserEmail] = UserEmail(data=data) or None
        self.joined_at: datetime = convert_rfc3339(data['created_at'])
        self.description: str = data['description']

    @property
    def color(self) -> ClientColor:
        """
        Returns the user's color.

        Returns
        -------
        ClientColor
            The user's color.
        """
        return ClientColor(state=self._state, user_id=self.id)

    async def get_info(self) -> User:
        """
        Fetches and returns detailed information about the client.

        Returns
        -------
        User
            Detailed user information.
        """
        user = await self._state.get_user_info(user_id=self.id)
        return user

    async def update(self, description: Optional[str]) -> User:
        """
        Updates the user's description and returns the updated user information.

        | Scopes                   | Description                       |
        | ------------------------ | --------------------------------- |
        | `user:edit`              | Update the client's description.  |

        Parameters
        ----------
        description: Optional[str]
            The new description for the user.

        Raises
        ------
        ValueError
            * The string in the description query parameter is too long.
        Unauthorized
            * The user access token must include the user:edit scope.

        Returns
        -------
        User
            Updated user information.
        """
        data = await self._state.http.update_user(description=description)
        return User(data=data)

    async def block(self, user: Union[BaseUser, str],
                    location: Literal['chat', 'whisper'] = MISSING,
                    reason: Literal['harassment', 'spam', 'other'] = MISSING) -> None:
        """
        Blocks a user with optional location and reason.

        ???+ Info
            Adding the parameters `location` or `reason` will not have any effect, as those details
            will not be displayed when retrieving the list of blocked users.

        | Scopes                      | Description     |
        | --------------------------- | ----------------|
        | `user:manage:blocked_users` | Block a user.   |

        Parameters
        ----------
        user: Union[BaseUser, str]
            The user to be blocked.
        location: Literal['chat', 'whisper']
            The location where the block will apply (chat or whisper).
        reason: Literal['harassment', 'spam', 'other']
            The reason for blocking (harassment, spam, other).

        Raises
        ------
        NotFound
            * Unable to find the requested user.
        BadRequest
            * The ID in target_user_id cannot be the same as the user ID in the access token.
            * The location or reason is not valid.
        Unauthorized
            * The user access token must include the user:manage:blocked_users scope.
        """
        user = await self._state.get_user(user)
        await self._state.http.block_user(target_user_id=user.id, source_context=location, reason=reason)

    async def unblock(self, user: Union[str, BaseUser]) -> None:
        """
        Unblocks a previously blocked user.

        | Scopes                      | Description       |
        | --------------------------- | ----------------- |
        | `user:manage:blocked_users` | Unblock a user.   |

        Parameters
        ----------
        user: Union[str, BaseUser]
            The user to be unblocked.

        Raises
        ------
        NotFound
            * Unable to find the requested user.
        Unauthorized
            * The user access token must include the user:manage:blocked_users scope.
        """
        user = await self._state.get_user(user)
        await self._state.http.unblock_user(target_user_id=user.id)

    async def fetch_block_list(self, limit: int = 4) -> AsyncGenerator[List[BaseUser]]:
        """
        Retrieves the list of blocked users.

        ???+ Warning
            This method uses [pagination](https://dev.twitch.tv/docs/api/guide/#pagination).
            Set the limit to -1 to retrieve all data, but be cautious of potential performance
            and rate limit impacts.

        | Scopes                    | Description                                |
        | ------------------------- | -------------------------------------------|
        | `user:read:blocked_users` | Retrieve all users blocked by the client.  |

        Parameters
        ----------
        limit: int
            The maximum number of blocked users to fetch.

        Raises
        ------
        Unauthorized
            * The user access token must include the user:read:blocked_users scope.

        Yields
        -------
        List[BaseUser]
            A list of blocked users.

        """
        async for users in self._state.http.fetch_user_block_list(limit=limit, broadcaster_id=self.id):
            yield [BaseUser(user, prefix='user_') for user in users]

    async def whisper(self, user: Union[str, BaseUser], message: str) -> None:
        """
        Send a Whisper Message to a User.

        !!! Warning
            This action requires a verified phone number.

        | Scopes                      | Description         |
        | --------------------------- | ------------------- |
        | `user:manage:whispers`      | Send a Whisper.     |

        Parameters
        ----------
        user: Union[str, User, BaseUser]
            User ID or user object.
        message: Optional[str]
            The message to send as a whisper. The message must not be empty.

            The maximum message lengths are as follows:

            * 500 characters if the recipient user hasn't received a whisper from you before.
            * 10,000 characters if the recipient user has received a whisper from you before.

            Messages exceeding the maximum length will be truncated.

        Raises
        ------
        NotFound
            * Unable to find the requested user.
        BadRequest
            * The message field must not contain an empty string.
            * The user that you're sending the whisper to doesn't allow whisper messages.
            * Whisper messages may not be sent to suspended users.
        Unauthorized
            * The user in the from_user_id query parameter must have a verified phone number.
            * The user access token must include the user:manage:whispers scope.
            * This ID in from_user_id must match the user ID in the user access token.
        Forbidden
            * Suspended users may not send whisper messages.
            * The account that's sending the message doesn't allow sending whispers.
        RateLimit
            * The sending user exceeded the number of whisper requests that they may make.
        """
        user = await self._state.get_user(user)
        await self._state.http.send_whisper(from_user_id=self.id, to_user_id=user.id, message=message)

    async def check_follow(self, user: Union[str, BaseUser]) -> Follow:
        """
        Checks if the client is following another user.

        Parameters
        ----------
        user: Union[str, BaseUser]
            The user to check for follow status.

        Raises
        ------
        NotFound
            * Unable to find the requested user.
            * The user is not following.

        Returns
        -------
        Follow
            Follow information if the user is following the specified user.
        """
        user = await self._state.get_user(user)
        async for users in self._state.http.fetch_followed_channels(limit=1, broadcaster_id=user.id,
                                                                    user_id=self._state.user.id):
            if len(users) == 1:
                return Follow(data=users[0])
            raise NotFound('The user is not following.')

    async def fetch_followed(self, limit: int = 4) -> AsyncGenerator[List[Follow]]:
        """
        Retrieves the list of users that client follows.

        ???+ Warning
            This method uses [pagination](https://dev.twitch.tv/docs/api/guide/#pagination).
            Set the limit to -1 to retrieve all data, but be cautious of potential performance
            and rate limit impacts.

        | Scopes                   | Description            |
        | ------------------------ | ---------------------- |
        | `user:read:follows`      | Get Followed Channels. |

        Parameters
        ----------
        limit: int
            The maximum number of users to fetch.

        Raises
        ------
        Unauthorized
            * The user access token is missing the user:read:follows scope.

        Yields
        -------
        List[Follow]
            A list of users that the client follows.
        """
        async for users in self._state.http.fetch_followed_channels(limit=limit, user_id=self.id):
            yield [Follow(data=user) for user in users]

    async def fetch_followed_streaming(self, limit: int = 4) -> AsyncGenerator[List[Stream]]:
        """
        Retrieves the list of streams from users that the client follows.

        | Scopes                   | Description            |
        | ------------------------ | ---------------------- |
        | `user:read:follows`      | Get Followed Channels. |

        ???+ Warning
            This method uses [pagination](https://dev.twitch.tv/docs/api/guide/#pagination).
            Set the limit to -1 to retrieve all data, but be cautious of potential performance
            and rate limit impacts.

        Parameters
        ----------
        limit: int
            The maximum number of streams to fetch.

        Raises
        ------
        Unauthorized
            * The user access token is missing the user:read:follows scope.

        Yields
        -------
        List[Stream]
            A list of streams from users that the current user follows.
        """
        async for broadcasters in self._state.http.fetch_followed_streams(limit=limit, user_id=self.id):
            yield [Stream(data=broadcaster) for broadcaster in broadcasters]

    async def check_subscription(self, user: Union[str, BaseUser]) -> Subscription:
        """
        Checks if the client is subscribed to another user's channel.

        | Scopes                     | Description              |
        | -------------------------- | ------------------------ |
        | `user:read:subscriptions`  | Check User Subscription. |

        Parameters
        ----------
        user: Union[str, BaseUser]
            The user to check for subscription status.

        Raises
        ------
        NotFound
            * Unable to find the requested user.
        Unauthorized
            * TThe user access token must include the user:read:subscriptions scope.

        Returns
        -------
        Subscription
            Subscription information if the user is subscribed to the specified user's channel.
        """
        user = await self._state.get_user(user)
        try:
            data = await self._state.http.check_user_subscription(broadcaster_id=user.id,
                                                                  user_id=self._state.user.id)
            return Subscription(data=data)
        except NotFound as error:
            raise NotFound('The user is not subscribed.') from error


# -------------------------------
#       + Channel Charity +
# -------------------------------
class ClientCharity:
    """
    Represents a client for managing charity campaigns and donations.

    ???+ Warning
        The broadcaster must be a partner or affiliate.
    """

    __slots__ = ('__state',)

    def __init__(self, state: ConnectionState) -> None:
        self.__state: ConnectionState = state

    async def get(self) -> Optional[Charity]:
        """
        Retrieve information about the currently active charity campaign.

        | Scopes                 | Description           |
        | ---------------------- | --------------------- |
        | `channel:read:charity` | Get Charity Campaign. |

        Raises
        ------
        Unauthorized
            * The user access token must include the channel:read:charity scope.
        Forbidden
            * The broadcaster is not a partner or affiliate.

        Returns
        -------
        Optional[Charity]
            Information about the active charity campaign, or None if no campaign is active.
        """
        data = await self.__state.http.get_charity_campaigns(broadcaster_id=self.__state.user.id)
        return Charity(data=data) if len(data) > 0 else None

    async def fetch_donations(self, limit: int = 4) -> AsyncGenerator[List[CharityDonation]]:
        """
        Fetch a list of charity donations made during the charity campaign.

        ???+ Warning
            This method uses [pagination](https://dev.twitch.tv/docs/api/guide/#pagination).
            Set the limit to -1 to retrieve all data, but be cautious of potential performance
            and rate limit impacts.

        | Scopes                 | Description                     |
        | ---------------------- | ------------------------------- |
        | `channel:read:charity` | Get Charity Campaign Donations. |

        Parameters
        ----------
        limit: int
            The maximum number of donations to fetch.

        Raises
        ------
        Unauthorized
            * The user access token must include the channel:read:charity scope.
        Forbidden
            * The broadcaster is not a partner or affiliate.

        Yields
        ------
        List[CharityDonation]
            A list of charity donation objects.
        """
        async for donations in self.__state.http.fetch_charity_campaigns_donations(
                broadcaster_id=self.__state.user.id,
                limit=limit):
            yield [CharityDonation(data=donation) for donation in donations]


# ------------------------------
#        + Channel Poll +
# ------------------------------
class ClientPoll:
    """
    Represents a client for managing polls on a broadcaster's channel.
    """
    __slots__ = ('__state',)

    def __init__(self, state: ConnectionState) -> None:
        self.__state: ConnectionState = state

    async def fetch_all(self, polls: List[Poll] = MISSING, limit: int = 4) -> AsyncGenerator[List[Poll]]:
        """
        Fetch a list of polls on the broadcaster's channel.

        ???+ Warning
            This method uses [pagination](https://dev.twitch.tv/docs/api/guide/#pagination).
            Set the limit to -1 to retrieve all data, but be cautious of potential performance
            and rate limit impacts.

        | Scopes                                         | Description |
        | ---------------------------------------------- | ----------- |
        | `channel:read:polls` or `channel:manage:polls` | Get Polls.  |

        Parameters
        ----------
        polls: List[Poll]
            A list of Poll objects representing existing polls.
        limit: int
            The maximum number of polls to fetch.

        Raises
        ------
        Unauthorized
            * The user access token is missing the channel:read:polls scope.

        Yields
        ------
        List[Poll]
            A list of Poll objects representing the fetched polls.
        """
        poll_ids = [poll.id for poll in polls] if isinstance(polls, list) else MISSING
        async for polls in self.__state.http.fetch_polls(limit=limit, broadcaster_id=self.__state.user.id,
                                                         poll_ids=poll_ids):
            yield [Poll(data=poll) for poll in polls]

    async def create(self, title: str,
                     choices: List[str], duration: int, points_per_vote: int = MISSING) -> Poll:
        """
        Create a new poll on the broadcaster's channel.

        | Scopes                 | Description  |
        | ---------------------- | ------------ |
        | `channel:manage:polls` | Create Poll. |

        Parameters
        ----------
        title: str
            The title or question for the poll.
        choices: List[str]
            A list of choices for the poll.
        duration: int
            The duration of the poll in seconds.
        points_per_vote: int
            The number of points awarded for each vote.

        Raises
        ------
        Unauthorized
            * The user access token is missing the channel:read:polls scope.
        BadRequest
            * The broadcaster already has a poll that's running.
        ValueError
            * The title may contain a maximum of 60 characters.
            * Choices must contain a minimum of 2 choices and up to a maximum of 5 choices.
            * The minimum is 15 seconds and the maximum is 1800 seconds (30 minutes).
            * The minimum of points_per_vote is 1 and the maximum is 1000000.

        Returns
        -------
        Poll
            The newly created Poll object.
        """
        data = await self.__state.http.create_poll(broadcaster_id=self.__state.user.id,
                                                   title=title, choices=choices, duration=duration,
                                                   points_per_vote=points_per_vote)
        return Poll(data=data)

    async def create_copy(self, poll: Poll) -> Poll:
        """
        Create a copy of an existing poll on the broadcaster's channel.

        | Scopes                 | Description  |
        | ---------------------- | ------------ |
        | `channel:manage:polls` | Create Poll. |

        Parameters
        ----------
        poll: Poll
            The Poll object representing the poll to be copied.

        Raises
        ------
        Unauthorized
            * The user access token is missing the channel:read:polls scope.
        BadRequest
            * The broadcaster already has a poll that's running.

        Returns
        -------
        Poll
            The newly created Poll object, which is a copy of the original poll.
        """
        settings = poll.to_json()
        data = await self.__state.http.create_poll(broadcaster_id=self.__state.user.id, **settings)
        return Poll(data=data)

    async def end(self, poll: Poll, archive: bool = False) -> Poll:
        """
        End a poll on the broadcaster's channel.

        | Scopes                 | Description  |
        | ---------------------- | ------------ |
        | `channel:manage:polls` | End Poll.    |

        Parameters
        ----------
        poll: Poll
            The Poll object representing the poll to be ended.
        archive: bool
            If True, the poll will be archived. If False, the poll will be terminated.

        Raises
        ------
        Unauthorized
            * The user access token is missing the channel:read:polls scope.
        BadRequest
            * The poll must be active to terminate or archive it.

        Returns
        -------
        Poll
            The Poll object with updated status.
        """
        data = await self.__state.http.end_poll(broadcaster_id=self.__state.user.id,
                                                poll_id=poll.id, archive=archive)
        return Poll(data=data)


# ------------------------------
#     + Channel Prediction +
# ------------------------------
class ClientPrediction:
    """
    Represents a client for managing Twitch Predictions.
    """

    def __init__(self, state: ConnectionState) -> None:
        self.__state: ConnectionState = state

    async def fetch_all(self, predictions: List[Prediction] = MISSING, limit: int = 4) \
            -> AsyncGenerator[List[Prediction]]:
        """
        Fetches predictions associated with the broadcaster's channel.

        ???+ Warning
            This method uses [pagination](https://dev.twitch.tv/docs/api/guide/#pagination).
            Set the limit to -1 to retrieve all data, but be cautious of potential performance
            and rate limit impacts.

        | Scopes                                                     | Description      |
        | ---------------------------------------------------------- | ---------------- |
        | `channel:read:predictions` or `channel:manage:predictions` | Get Predictions. |


        Parameters
        ----------
        predictions: List[Prediction]
            A list of Prediction objects to filter the results.
        limit: int
            The maximum number of predictions to fetch.

        Raises
        ------
        TypeError
            * The maximum number of predictions you may specify is 25.
        Unauthorized
            * The user access token must include the channel:read:predictions scope.

        Yields
        -------
        List[Prediction]
            A list of Prediction objects.
        """
        prediction_ids = [prediction.id for prediction in predictions] \
            if isinstance(predictions, list) else MISSING
        async for predictions in self.__state.http.fetch_predictions(limit=limit,
                                                                     broadcaster_id=self.__state.user.id,
                                                                     prediction_ids=prediction_ids):
            yield [Prediction(data=prediction) for prediction in predictions]

    async def create(self, title: str, outcomes: List[str], duration: int) -> Prediction:
        """
        Creates a new prediction for the broadcaster's channel.

        | Scopes                       | Description        |
        | ---------------------------- | ------------------ |
        | `channel:manage:predictions` | Create Prediction. |

        Parameters
        ----------
        title: str
            The title of the prediction.
        outcomes: List[str]
            A list of possible outcomes for the prediction.
        duration: int
            The duration of the prediction window in seconds.

        Raises
        ------
        ValueError
            * The title is limited to a maximum of 45 characters.
            * List must contain a minimum of 2 outcomes and up to a maximum of 10 outcomes.
            * The outcome title is limited to a maximum of 25 characters.
            * The minimum of duration is 30 seconds and the maximum is 1800 seconds.
        BadRequest
            * The broadcaster already has a prediction that's running.
        Unauthorized
            * The user access token must include the channel:manage:predictions scope.
        RateLimit
            * The broadcaster exceeded the number of requests that they may make.

        Returns
        -------
        Prediction
            A Prediction object representing the created prediction.

        Example
        -------
        ```py
        channel = client.channel
        await channel.prediction.create(title='which color do you like!', outcomes=['blue', 'gingerline'])
        ```
        """
        outcomes = [{'title': outcome} for outcome in outcomes]
        data = await self.__state.http.create_prediction(broadcaster_id=self.__state.user.id, title=title,
                                                         outcomes=outcomes, prediction_window=duration)
        return Prediction(data=data)

    async def create_copy(self, prediction: Prediction) -> Prediction:
        """
        Creates a copy of an existing prediction.

        | Scopes                       | Description        |
        | ---------------------------- | ------------------ |
        | `channel:manage:predictions` | Create Prediction. |

        Parameters
        ----------
        prediction: Prediction
            The Prediction object to copy settings from.

        Raises
        ------
        BadRequest
            * The broadcaster already has a prediction that's running.
        Unauthorized
            * The user access token must include the channel:manage:predictions scope.
        RateLimit
            * The broadcaster exceeded the number of requests that they may make.

        Returns
        -------
        Prediction
            A Prediction object representing the created prediction.
        """
        settings = prediction.to_json()
        data = await self.__state.http.create_prediction(broadcaster_id=self.__state.user.id, **settings)
        return Prediction(data=data)

    async def lock(self, prediction: Prediction) -> Prediction:
        """
        Locks an ongoing prediction.

        | Scopes                       | Description     |
        | ---------------------------- | --------------- |
        | `channel:manage:predictions` | End Prediction. |

        Parameters
        ----------
        prediction: Prediction
            The Prediction object representing the prediction to be locked.

        Raises
        ------
        BadRequest
            * To update the prediction's status to LOCKED, its current status must be ACTIVE.
        Unauthorized
            * The user access token must include the channel:manage:predictions scope.

        Returns
        -------
        Prediction
            A Prediction object representing the locked prediction.

        """
        data = await self.__state.http.end_prediction(broadcaster_id=self.__state.user.id,
                                                      prediction_id=prediction.id, status='LOCKED')
        return Prediction(data=data)

    async def resolve(self, prediction: Prediction, outcome: Outcome) -> Prediction:
        """
        Resolves an ongoing prediction.

        | Scopes                       | Description     |
        | ---------------------------- | --------------- |
        | `channel:manage:predictions` | End Prediction. |

        Parameters
        ----------
        prediction: Prediction
            The Prediction object representing the prediction to be resolved.
        outcome: Outcome
            The winning outcome of the prediction.

        Raises
        ------
        BadRequest
            * Prediction's status must be ACTIVE or LOCKED.
        Unauthorized
            * The user access token must include the channel:manage:predictions scope.

        Returns
        -------
        Prediction
            A Prediction object representing the resolved prediction.

        """
        data = await self.__state.http.end_prediction(broadcaster_id=self.__state.user.id,
                                                      prediction_id=prediction.id, status='RESOLVED',
                                                      winning_outcome_id=outcome.id)
        return Prediction(data=data)

    async def cancel(self, prediction: Prediction) -> Prediction:
        """
        Cancels an ongoing prediction.

        | Scopes                       | Description     |
        | ---------------------------- | --------------- |
        | `channel:manage:predictions` | End Prediction. |

        Parameters
        ----------
        prediction: Prediction
            The Prediction object representing the prediction to be canceled.

        Raises
        ------
        BadRequest
            * Prediction's status must be ACTIVE or LOCKED.
        Unauthorized
            * The user access token must include the channel:manage:predictions scope.

        Returns
        -------
        Prediction
            A Prediction object representing the canceled prediction.

        """
        data = await self.__state.http.end_prediction(broadcaster_id=self.__state.user.id,
                                                      prediction_id=prediction.id, status='CANCELED')
        return Prediction(data=data)


# ------------------------------
#       + Channel Reward +
# ------------------------------
class ClientRewardRedemption:
    """
    Represents a client for managing Twitch Channel Points reward redemptions.
    """
    __slots__ = ('_state',)

    def __init__(self, state: ConnectionState) -> None:
        self._state: ConnectionState = state

    async def fetch_all(self, reward: BaseReward,
                        status: Literal['CANCELED', 'FULFILLED', 'UNFULFILLED'] = 'UNFULFILLED',
                        recent: bool = False, limit: int = 4) -> AsyncGenerator[List[Redemption]]:
        """
        Fetches custom reward redemptions.

        ???+ Warning
            This method uses [pagination](https://dev.twitch.tv/docs/api/guide/#pagination).
            Set the limit to -1 to retrieve all data, but be cautious of potential performance
            and rate limit impacts.

        | Scopes                                                     | Description                   |
        | ---------------------------------------------------------- | ----------------------------- |
        | `channel:read:redemptions` or `channel:manage:redemptions` | Get Custom Reward Redemption. |

        Parameters
        ----------
        reward: BaseReward
            The BaseReward object representing the custom reward.
        status: Literal['CANCELED', 'FULFILLED', 'UNFULFILLED']
            The status of the redemptions to return.
        recent: bool
            Whether to fetch recent redemptions.
        limit: int
            The maximum number of redemptions to fetch. Defaults to 4.

        Raises
        ------
        Unauthorized
            * The user access token must include the channel:read:redemptions or channel:manage:redemptions
             scope.
        Forbidden
            * The ID in the Client-Id header must match the client ID used to create the custom reward.
            * The broadcaster is not a partner or affiliate.

        Yields
        -------
        List[Redemption]
            A list of Redemption objects representing the fetched redemptions.

        """
        async for redemptions in self._state.http.fetch_custom_reward_redemption(
                limit=limit,
                broadcaster_id=self._state.user.id,
                reward_id=reward.id,
                status=status,
                recent=recent):
            yield [Redemption(data=redemption) for redemption in redemptions]

    async def get_redemptions(self, reward: BaseReward, redemptions: List[Redemption],
                              recent: bool = False) -> List[Redemption]:
        """
        Fetches specific custom reward redemptions.

        | Scopes                                                     | Description                   |
        | ---------------------------------------------------------- | ----------------------------- |
        | `channel:read:redemptions` or `channel:manage:redemptions` | Get Custom Reward Redemption. |

        Parameters
        ----------
        reward: BaseReward
            The BaseReward object representing the custom reward.
        redemptions: List[Redemption]
            A list of Redemption objects to fetch.
        recent: bool
            Whether to fetch recent redemptions.

        Raises
        ------
        TypeError
            * The maximum number of redemption you may specify is 50.
        NotFound
            * All the redemptions not found.
        Unauthorized
            * The user access token must include the channel:read:redemptions or channel:manage:redemptions
             scope.
        Forbidden
            * The ID in the Client-Id header must match the client ID used to create the custom reward.
            * The broadcaster is not a partner or affiliate.

        Returns
        -------
        List[Redemption]
            A list of Redemption objects representing the fetched redemptions.

        """
        redemption_ids = [redemption.id for redemption in redemptions]
        async for redemptions in self._state.http.fetch_custom_reward_redemption(
                limit=1,
                broadcaster_id=self._state.user.id,
                reward_id=reward.id,
                redemption_ids=redemption_ids,
                recent=recent):
            return [Redemption(data=redemption) for redemption in redemptions]

    async def update(self, reward: BaseReward, redemptions: List[Redemption],
                     fulfill: bool = True) -> List[Redemption]:
        """
        Updates the status of custom reward redemptions.

        ???+ Warning
            You may update a redemption only if its status is `UNFULFILLED`.

        | Scopes                       | Description               |
        | ---------------------------- | ------------------------- |
        | `channel:manage:redemptions` | Update Redemption Status. |

        Parameters
        ----------
        reward: BaseReward
            The BaseReward object representing the custom reward.
        redemptions: List[Redemption]
            A list of Redemption objects to be updated.
        fulfill: bool
            Whether to fulfill the redemptions (True) or cancel them (False).

        Raises
        ------
        NotFound
            * The custom reward not found.
            * The redemptions not found or their statuses weren't marked as UNFULFILLED.
        Unauthorized
            * The user access token must include the channel:read:redemptions scope.
        Forbidden
            * The ID in the Client-Id header must match the client ID used to create the custom reward.
            * The broadcaster is not a partner or affiliate.

        Returns
        -------
        List[Redemption]
            A list of Redemption objects representing the updated redemptions.
        """
        redemption_ids = [redemption.id for redemption in redemptions if redemption.status == 'UNFULFILLED']
        if len(redemption_ids) >= 1:
            data = await self._state.http.update_redemption_status(broadcaster_id=self._state.user.id,
                                                                   reward_id=reward.id,
                                                                   redemption_ids=redemption_ids,
                                                                   fulfill=fulfill)
            return [Redemption(data=redemption) for redemption in data]
        return []


class ClientReward:
    """
    Represents a client for managing Twitch Channel Points rewards.

    ???+ Warning
        The broadcaster must be a partner or affiliate.
    """

    __slots__ = ('_state',)

    def __init__(self, state: ConnectionState) -> None:
        self._state: ConnectionState = state

    @property
    def redemptions(self) -> ClientRewardRedemption:
        """
        Access the client for managing reward redemptions.

        This property allows accessing the client for managing reward redemptions.

        Returns
        -------
        ClientRewardRedemption
            A ClientRewardRedemption instance.
        """
        return ClientRewardRedemption(state=self._state)

    async def get_all(self,
                      rewards: List[Union[Reward, Redemption]] = MISSING,
                      only_manageable_rewards: bool = False) -> List[Reward]:
        """
        Fetches all custom rewards associated with the broadcaster's channel.

        | Scopes                                                     | Description        |
        | ---------------------------------------------------------- | ------------------ |
        | `channel:read:redemptions` or `channel:manage:redemptions` | Get Custom Reward. |

        Parameters
        ----------
        rewards: List[Union[Reward, Redemption]]
            A list of Reward or Redemption objects to filter the results.
        only_manageable_rewards: bool
            If True, only rewards that the broadcaster can manage will be returned.

        Raises
        ------
        TypeError
            * The maximum number of rewards you may specify is 100.
        Unauthorized
            * The user access token must include the channel:read:redemptions or channel:manage:redemptions
             scope.
        Forbidden
            * The broadcaster is not a partner or affiliate.
        NotFound
            * All the custom rewards specified were not found.

        Returns
        -------
        List[Reward]
            A list of Reward objects representing the custom rewards.
        """
        reward_ids = [
            i.id if isinstance(i, Reward) else
            i.reward.id if isinstance(i, Redemption) else i for i in rewards
        ] if isinstance(rewards, list) else MISSING
        data = await self._state.http.get_custom_rewards(broadcaster_id=self._state.user.id,
                                                         only_manageable_rewards=only_manageable_rewards,
                                                         reward_ids=reward_ids)
        return [Reward(data=reward) for reward in data]

    async def create(self, title: str, cost: int, enable: bool = True,
                     background_color: str = MISSING,
                     prompt: str = MISSING,
                     is_user_input_required: bool = False,
                     max_per_stream: int = MISSING,
                     max_per_user_per_stream: int = MISSING,
                     global_cooldown_seconds: int = MISSING,
                     should_redemptions_skip_request_queue: bool = False) -> Reward:
        """
        Creates a new custom reward for the broadcaster's channel.

        | Scopes                       | Description            |
        | ---------------------------- | ---------------------- |
        | `channel:manage:redemptions` | Create Custom Rewards. |

        Parameters
        ----------
        title: str
            The title of the custom reward.
        cost: int
            The cost of the custom reward in Channel Points.
        enable: bool
            Whether the custom reward is enabled.
        background_color: str
            The background color of the custom reward.
        prompt: str
            The user prompt for the custom reward.
        is_user_input_required: bool
            Whether user input is required when redeeming the reward.
        max_per_stream: int
            The maximum number of times the reward can be redeemed per stream.
        max_per_user_per_stream: int
            The maximum number of times a user can redeem the reward per stream.
        global_cooldown_seconds: int
            The global cooldown period for the reward in seconds.
        should_redemptions_skip_request_queue: bool
            Whether redemptions should skip the request queue.

        Raises
        ------
        ValueError
            * The title may contain a maximum of 45 characters.
            * The cost of the reward, in Channel Points. The minimum is 1 point.
            * The prompt may contain a maximum of 200 characters.
            * The minimum value of max_per_stream is 1.
            * The minimum value of max_per_user_per_stream is 1.
            * The minimum value of global_cooldown_seconds is 1 and the maximum is 604800.
        BadRequest
            * The request exceeds the maximum number of rewards allowed per channel.
            * The title must be unique amongst all the broadcaster's custom rewards.
        Unauthorized
            * The user access token is missing the channel:manage:redemptions scope.
        Forbidden
            * The broadcaster is not a partner or affiliate.

        Returns
        -------
        Reward
            A Reward object representing the created custom reward.
        """
        data = await self._state.http.create_custom_rewards(
            broadcaster_id=self._state.user.id,
            title=title,
            cost=cost,
            is_enabled=enable,
            background_color=background_color,
            prompt=prompt,
            is_user_input_required=is_user_input_required,
            max_per_stream=max_per_stream,
            max_per_user_per_stream=max_per_user_per_stream,
            should_redemptions_skip_request_queue=should_redemptions_skip_request_queue,
            global_cooldown_seconds=global_cooldown_seconds)
        return Reward(data=data)

    async def create_copy(self, title: str, reward: Reward) -> Reward:
        """
        Creates a copy of an existing custom reward.

        | Scopes                       | Description            |
        | ---------------------------- | ---------------------- |
        | `channel:manage:redemptions` | Create Custom Rewards. |

        Parameters
        ----------
        title: str
            The new title of the custom reward (must be unique).
        reward: Reward
            The Reward object to copy settings from.

        Raises
        ------
        ValueError
            * The title may contain a maximum of 45 characters.
        BadRequest
            * The request exceeds the maximum number of rewards allowed per channel.
            * The title must be unique amongst all the broadcaster's custom rewards.
        Unauthorized
            * The user access token is missing the channel:manage:redemptions scope.
        Forbidden
            * The broadcaster is not a partner or affiliate.

        Returns
        -------
        Reward
            A Reward object representing the created custom reward.
        """
        settings = reward.to_json()
        # Reward title must be unique.
        settings['title'] = title
        data = await self._state.http.create_custom_rewards(broadcaster_id=self._state.user.id, **settings)
        return Reward(data=data)

    async def update(self, reward: Reward,
                     title: str = MISSING,
                     cost: int = MISSING,
                     enable: bool = MISSING,
                     pause: bool = MISSING,
                     background_color: str = MISSING,
                     prompt: str = MISSING,
                     is_user_input_required: bool = MISSING,
                     max_per_stream: Optional[int] = MISSING,
                     max_per_user_per_stream: Optional[int] = MISSING,
                     global_cooldown_seconds: Optional[int] = MISSING,
                     should_redemptions_skip_request_queue: bool = MISSING) -> Reward:
        """
        Updates an existing custom reward.

        | Scopes                       | Description           |
        | ---------------------------- | --------------------- |
        | `channel:manage:redemptions` | Update Custom Reward. |

        Parameters
        ----------
        reward: Reward
            The Reward object representing the custom reward to be updated.
        title: str
            The new title for the custom reward.
        cost: int
            The new cost for the custom reward.
        enable: bool
            Whether the custom reward is enabled.
        pause: bool
            Whether the custom reward is paused.
        background_color: str
            The new background color for the custom reward.
        prompt: str
            The new user prompt for the custom reward.
        is_user_input_required: bool
            Whether user input is required when redeeming the reward.
        max_per_stream: int
            The new maximum redemption limit per stream.
        max_per_user_per_stream: int
            The new maximum redemption limit per user per stream.
        global_cooldown_seconds: int
            The new global cooldown period for the reward in seconds.
        should_redemptions_skip_request_queue: bool
            Whether redemptions should skip the request queue.

        Raises
        ------
        ValueError
            * The title may contain a maximum of 45 characters.
            * The cost of the reward, in Channel Points. The minimum is 1 point.
            * The prompt may contain a maximum of 200 characters.
        BadRequest
            * The minimum value for max_per_stream is 1.
            * The minimum value for max_per_user_per_stream is 1.
            * The minimum value for global_cooldown_seconds is 1 and the maximum is 604800.
            * The title must be unique amongst all the broadcaster's custom rewards.
        Unauthorized
            * The user access token is missing the channel:manage:redemptions scope.
        Forbidden
            * The ID in the Client-Id header must match the client ID used to create the custom reward.
            * The broadcaster is not a partner or affiliate.
        NotFound
            * The custom reward specified in the id query parameter was not found.

        Returns
        -------
        Reward
            A Reward object representing the updated custom reward.
        """
        data = await self._state.http.update_custom_rewards(
            broadcaster_id=self._state.user.id,
            reward_id=reward.id,
            title=title,
            cost=cost,
            is_enabled=enable,
            is_paused=pause,
            background_color=background_color,
            prompt=prompt,
            is_user_input_required=is_user_input_required,
            max_per_stream=max_per_stream,
            max_per_user_per_stream=max_per_user_per_stream,
            should_redemptions_skip_request_queue=should_redemptions_skip_request_queue,
            global_cooldown_seconds=global_cooldown_seconds)
        return Reward(data=data)

    async def delete(self, reward: Reward):
        """
        Deletes a custom reward.

        | Scopes                       | Description           |
        | ---------------------------- | --------------------- |
        | `channel:manage:redemptions` | Delete Custom Reward. |

        Raises
        ------
        Unauthorized
            * The user access token is missing the channel:manage:redemptions scope.
        Forbidden
            * The ID in the Client-Id header must match the client ID used to create the custom reward.
            * The broadcaster is not a partner or affiliate.
        NotFound
            * The custom reward specified in the id query parameter was not found.

        Parameters
        ----------
        reward: Reward
            The Reward object representing the custom reward to be deleted.
        """
        await self._state.http.delete_custom_rewards(broadcaster_id=self._state.user.id,
                                                     reward_id=reward.id)


# ------------------------------
#     + Channel Moderators +
# ------------------------------
class ClientModerators:
    """
    Represents a client for managing moderators in a Twitch channel.
    """
    __slots__ = ('_state',)

    def __init__(self, state: ConnectionState) -> None:
        self._state: ConnectionState = state

    async def fetch_all(self, limit: int = 4) -> AsyncGenerator[List[BaseUser]]:
        """
        Fetches all moderators of the channel.

        ???+ Warning
            This method uses [pagination](https://dev.twitch.tv/docs/api/guide/#pagination).
            Set the limit to -1 to retrieve all data, but be cautious of potential performance
            and rate limit impacts.

        | Scopes                                           | Description     |
        | ------------------------------------------------ | --------------- |
        | `moderation:read` or `channel:manage:moderators` | Get Moderators. |

        Parameters
        ----------
        limit: int
            The maximum number of moderators to fetch.

        Raises
        ------
        Unauthorized
            * The user access token must include the moderation:read or channel:manage:moderators scope.

        Yields
        -------
        List[BaseUser]
            A list of BaseUser objects representing the fetched moderators.
        """
        async for users in self._state.http.fetch_moderators(limit=limit,
                                                             broadcaster_id=self._state.user.id):
            yield [BaseUser(user, prefix='user_') for user in users]

    async def get_moderators(self, users: List[Union[str, BaseUser]]) -> List[BaseUser]:
        """
        Fetches specific moderators of the channel.

        | Scopes                                           | Description     |
        | ------------------------------------------------ | --------------- |
        | `moderation:read` or `channel:manage:moderators` | Get Moderators. |

        Parameters
        ----------
        users: List[Union[str, BaseUser]]
            A list of users to fetch as moderators.

        Raises
        ------
        TypeError
            * The maximum number of users you may specify is 100.
        Unauthorized
            * The user access token must include the moderation:read or channel:manage:moderators scope.

        Returns
        -------
        List[BaseUser]
            A list of BaseUser objects representing the fetched moderators.
        """
        user_ids = [user.id for user in (await self._state.get_users(users))]
        async for users in self._state.http.fetch_moderators(limit=1,
                                                             broadcaster_id=self._state.user.id,
                                                             user_ids=user_ids):
            return [BaseUser(user, prefix='user_') for user in users]

    async def add(self, user: Union[str, BaseUser], force: bool = False) -> None:
        """
        Adds a user as a moderator to the channel.

        | Scopes                      | Description            |
        | --------------------------- | ---------------------- |
        | `channel:manage:moderators` | Add Channel Moderator. |

        Parameters
        ----------
        user: Union[str, BaseUser]
            The user to be added as a moderator.
        force: bool
            Whether to force add the user as a moderator and prevent role conflict.

        Raises
        ------
        NotFound
            * Unable to find the requested user.
        BadRequest
            * The user is already a moderator in the broadcaster's chat room.
            * The user cannot become a moderator because they're banned from the channel.
        Unauthorized
            * The user access token must include the channel:manage:moderators scope.
        UserRoleConflict
            * The user is a VIP. To make them a moderator, you must first remove them as a VIP.
        RateLimit
            * The broadcaster has exceeded the number of requests allowed within a 10-second window
        """
        user = await self._state.get_user(user)
        await self._state.http.add_channel_moderator(broadcaster_id=self._state.user.id, user_id=user.id,
                                                     force=force)

    async def remove(self, user: Union[str, BaseUser]) -> None:
        """
        Removes a user as a moderator from the channel.

        | Scopes                      | Description                |
        | --------------------------- | -------------------------- |
        | `channel:manage:moderators` | Remove  Channel Moderator. |

        Parameters
        ----------
        user: Union[str, BaseUser]
            The user to be removed as a moderator.

        Raises
        ------
        NotFound
            * Unable to find the requested user.
        BadRequest
            * The user is not a moderator in the broadcaster's chat room.
            * Cannot remove moderator from a deactivated or suspended user.
        Unauthorized
            * The user access token must include the channel:manage:moderators scope.
        RateLimit
            * The broadcaster has exceeded the number of requests allowed within a 10-second window
        """
        if isinstance(user, BaseUser):
            # Ignoring deactivated/suspended moderator.
            if user.name == 'anonymous':
                raise BadRequest('Cannot remove moderator from a deactivated or suspended user.')
        user = await self._state.get_user(user)
        await self._state.http.remove_channel_moderator(broadcaster_id=self._state.user.id,
                                                        user_id=user.id)


# ------------------------------
#        + Channel Vips +
# ------------------------------
class ClientVips:
    """
    Represents a client for managing VIPs in a Twitch channel.
    """
    __slots__ = ('__state',)

    def __init__(self, state: ConnectionState) -> None:
        self.__state: ConnectionState = state

    async def fetch_all(self, limit: int = 4) -> AsyncGenerator[List[BaseUser]]:
        """
        Fetches all VIPs of the channel.

        ???+ Warning
            This method uses [pagination](https://dev.twitch.tv/docs/api/guide/#pagination).
            Set the limit to -1 to retrieve all data, but be cautious of potential performance
            and rate limit impacts.

        | Scopes                                       | Description |
        | -------------------------------------------- | ------------|
        | `channel:read:vips` or `channel:manage:vips` | Get VIPs.   |

        Parameters
        ----------
        limit: int
            The maximum number of VIPs to fetch.

        Raises
        ------
        Unauthorized
            * The user access token must include the channel:read:vips or channel:manage:vips scope.

        Yields
        -------
        List[BaseUser]
            A list of BaseUser objects representing the fetched VIPs.
        """
        async for users in self.__state.http.fetch_vips(limit=limit, broadcaster_id=self.__state.user.id):
            yield [BaseUser(user, prefix='user_') for user in users]

    async def get_vips(self, users: List[Union[str, BaseUser]]) -> List[BaseUser]:
        """
        Fetches specific VIPs of the channel.

        | Scopes                                       | Description |
        | -------------------------------------------- | ------------|
        | `channel:read:vips` or `channel:manage:vips` | Get VIPs.   |

        Parameters
        ----------
        users: List[Union[str, BaseUser]]
            A list of users to fetch as VIPs.

        Raises
        ------
        TypeError
            * The maximum number of users you may specify is 100.
        Unauthorized
            * The user access token must include the channel:read:vips or channel:manage:vips scope.

        Returns
        -------
        List[BaseUser]
            A list of BaseUser objects representing the fetched VIPs.
        """
        user_ids = [user.id for user in (await self.__state.get_users(users))]
        async for users in self.__state.http.fetch_vips(limit=1, broadcaster_id=self.__state.user.id,
                                                        user_ids=user_ids):
            return [BaseUser(user, prefix='user_') for user in users]

    async def add(self, user: Union[str, BaseUser], force: bool = False) -> None:
        """
        Adds a user as a VIP to the channel.

        | Scopes                | Description      |
        | --------------------- | -----------------|
        | `channel:manage:vips` | Add Channel VIP. |

        Parameters
        ----------
        user: Union[str, BaseUser]
            The user to be added as a VIP.
        force: bool
            Whether to force add the user as a VIP and prevent role conflict.

        Raises
        ------
        NotFound
            * Unable to find the requested user.
        BadRequest
            * The user is blocked from the broadcaster's channel.
            * The broadcaster must complete the Build a Community requirement before they may assign VIPs.
        Unauthorized
            * The user access token must include the channel:manage:vips scope.
        Conflict
            * The broadcaster does not have available VIP slots.
        UserRoleConflict
            * The user is already a VIP.
            * The user is a moderator. To make them a VIP, you must first remove them as a moderator.
        RateLimit
            * The broadcaster exceeded the number of VIP that they may add within a 10-second window.
        """
        user = await self.__state.get_user(user)
        await self.__state.http.add_channel_vip(broadcaster_id=self.__state.user.id, user_id=user.id,
                                                force=force)

    async def remove(self, user: Union[str, BaseUser]) -> None:
        """
        Removes a user as a VIP from the channel.

        | Scopes                | Description         |
        | --------------------- | --------------------|
        | `channel:manage:vips` | Remove Channel VIP. |

        Parameters
        ----------
        user: Union[str, BaseUser]
            The user to be removed as a VIP.

        Raises
        ------
        NotFound
            * Unable to find the requested user.
        BadRequest
            * Cannot remove VIP from a deactivated or suspended user.
        UserRoleConflict
            * The user is not a VIP in the broadcaster's channel.
        Unauthorized
            * The user access token must include the channel:manage:vips scope.
        Forbidden
            * The user in broadcaster_id doesn't have permission to remove the user's VIP status.
        RateLimit
            * The broadcaster exceeded the number of VIPs that they may remove within a 10-second window.
        """
        if isinstance(user, BaseUser):
            # Ignoring deactivated/suspended VIP.
            if user.name == 'anonymous':
                raise BadRequest('Cannot remove VIP from a deactivated or suspended user.')
        user = await self.__state.get_user(user)
        await self.__state.http.remove_channel_vip(broadcaster_id=self.__state.user.id, user_id=user.id)


# -----------------------------
#   + Channel Subscriptions +
# -----------------------------
class ClientSubscriptions:
    """
    Represents a client for managing subscriptions in a Twitch channel.
    """

    def __init__(self, state: ConnectionState) -> None:
        self.__state: ConnectionState = state

    async def get_total(self) -> Tuple[int, int]:
        """
        Get the total number of subscribers to the channel.

        | Scopes                                                       | Description                    |
        | ------------------------------------------------------------ | -------------------------------|
        | `channel:read:subscriptions` or `channel:read:subscriptions` | Get Broadcaster Subscriptions. |

        Raises
        ------
        Unauthorized
            * The user access token must include the channel:read:subscriptions or
             channel:read:subscriptions scope.

        Returns
        -------
        Tuple[int, int]
            A tuple containing the total number of subscriber points and the total number subscribers.
        """
        data = await self.__state.http.get_total_broadcaster_subscriptions(
            broadcaster_id=self.__state.user.id)
        return data

    async def fetch_all(self, limit: int = 4) -> AsyncGenerator[List[Subscription]]:
        """
        Fetch information about all subscribers to the channel.

        ???+ Warning
            This method uses [pagination](https://dev.twitch.tv/docs/api/guide/#pagination).
            Set the limit to -1 to retrieve all data, but be cautious of potential performance
            and rate limit impacts.

        | Scopes                                                       | Description                    |
        | ------------------------------------------------------------ | -------------------------------|
        | `channel:read:subscriptions` or `channel:read:subscriptions` | Get Broadcaster Subscriptions. |

        Parameters
        ----------
        limit: int
            The maximum number of subscribers to fetch.

        Raises
        ------
        Unauthorized
            * The user access token must include the channel:read:subscriptions or
             channel:read:subscriptions scope.

        Yields
        -------
        List[Subscription]
            A list of Subscription objects representing the fetched subscribers.
        """
        async for users in self.__state.http.fetch_broadcaster_subscriptions(
                limit=limit, broadcaster_id=self.__state.user.id):
            yield [Subscription(data=user) for user in users]

    async def get_subscriptions(self, users: List[Union[str, BaseUser]]) -> List[Subscription]:
        """
        Get subscription information for specific users.

        | Scopes                                                       | Description                    |
        | ------------------------------------------------------------ | -------------------------------|
        | `channel:read:subscriptions` or `channel:read:subscriptions` | Get Broadcaster Subscriptions. |

        Parameters
        ----------
        users: List[Union[str, BaseUser]]
            A list of users for which to retrieve subscription information.

        Raises
        ------
        TypeError
            * The maximum number of users you may specify is 100.
        Unauthorized
            * The user access token must include the channel:read:subscriptions or
             channel:read:subscriptions scope.

        Returns
        -------
        List[Subscription]
            A list of Subscription objects representing the subscription information for the specified users.
        """
        user_ids = [user.id for user in (await self.__state.get_users(users))]
        async for users in self.__state.http.fetch_broadcaster_subscriptions(
                limit=1, broadcaster_id=self.__state.user.id, user_ids=user_ids):
            return [Subscription(data=user) for user in users]


# ------------------------------
#     + Channel Extensions +
# ------------------------------
class ClientExtensions(ChannelExtensions):
    """
    Represents a client for managing extensions in a Twitch channel.
    """
    __slots__ = ()

    def __init__(self, state: ConnectionState) -> None:
        super().__init__(state=state, broadcaster_id=state.user.id)

    async def get_all(self) -> List[Extension]:
        """
        Get information about all extensions in the channel.

        | Scopes                | Description                   |
        | --------------------- | ------------------------------|
        | `user:read:broadcast` | Get User Active Extensions.   |
        | `user:edit:broadcast` | Get User Inactive Extensions. |

        Raises
        ------
        Unauthorized
            * The user access token must include the user:read:broadcast or user:edit:broadcast scope.

        Returns
        -------
        List[Extension]
            A list of Extension objects representing the available extensions in the channel.
        """
        data = await self.__state.http.get_user_extensions()
        return [Extension(data=ex) for ex in data]

    async def update_panel(self, slot: Literal['1', '2', '3'], extension_id: str,
                           extension_version: str, activate: bool):
        """
        Update an extension panel in the channel.

        | Scopes                | Description             |
        | --------------------- | ------------------------|
        | `user:edit:broadcast` | Update User Extensions. |

        Parameters
        ----------
        slot: Literal['1', '2', '3']
            The slot number of the extension panel to update.
        extension_id: str
            The ID of the extension to update.
        extension_version: str
            The version of the extension to activate.
        activate: bool
            A boolean value indicating whether to activate or deactivate the extension panel.

        Raises
        ------
        Unauthorized
            * The user access token must include the user:edit:broadcast scope.
        NotFound
            * An extension with the specified id and version values was not found.

        Returns
        -------
        Extensions
            An Extensions object representing the updated extension panel.

        """
        data = await self.__state.http.update_user_extensions(section='component', slot=slot,
                                                              extension_id=extension_id,
                                                              extension_version=extension_version,
                                                              activate=activate)
        return Extensions(data=data)

    async def update_overlay(self, extension_id: str, extension_version: str, activate: bool):
        """
        Update the channel's overlay with an extension.

        | Scopes                | Description             |
        | --------------------- | ------------------------|
        | `user:edit:broadcast` | Update User Extensions. |

        Parameters
        ----------
        extension_id: str
            The ID of the extension to update.
        extension_version: str
            The version of the extension to activate.
        activate: bool
            A boolean value indicating whether to activate or deactivate the overlay extension.

        Raises
        ------
        Unauthorized
            * The user access token must include the user:edit:broadcast scope.
        NotFound
            * An extension with the specified id and version values was not found.

        Returns
        -------
        Extensions
            An Extensions object representing the updated overlay extension.
        """
        data = await self.__state.http.update_user_extensions(section='overlay', slot='1',
                                                              extension_id=extension_id,
                                                              extension_version=extension_version,
                                                              activate=activate)
        return Extensions(data=data)

    async def update_component(self, slot: Literal['1', '2'], extension_id: str, extension_version: str,
                               x: int, y: int, activate: bool):
        """
        Update a component extension in the channel.

        | Scopes                | Description             |
        | --------------------- | ------------------------|
        | `user:edit:broadcast` | Update User Extensions. |

        Parameters
        ----------
        slot: Literal['1', '2']
            The slot number of the component extension to update.
        extension_id: str
            The ID of the extension to update.
        extension_version: str
            The version of the extension to activate.
        x: int
            The x-coordinate position of the component extension on the screen.
        y: int
            The y-coordinate position of the component extension on the screen.
        activate: bool
            A boolean value indicating whether to activate or deactivate the component extension.

        Raises
        ------
        Unauthorized
            * The user access token must include the user:edit:broadcast scope.
        NotFound
            * An extension with the specified id and version values was not found.

        Returns
        -------
        Extensions
            An Extensions object representing the updated component extension.

        """
        data = await self.__state.http.update_user_extensions(section='component', slot=slot,
                                                              extension_id=extension_id,
                                                              extension_version=extension_version,
                                                              x=x, y=y,
                                                              activate=activate)
        return Extensions(data=data)


# ------------------------------
#      + Channel Schedule +
# ------------------------------
class ClientSchedule(ChannelSchedule):
    """
    Represents a client for managing the stream schedule of a Twitch channel.
    """
    __slots__ = ()

    def __init__(self, state: ConnectionState) -> None:
        super().__init__(state=state, broadcaster_id=state.user.id)

    async def create(self,
                     timezone: str,
                     duration: int,
                     is_recurring: bool = MISSING,
                     start_time: datetime = MISSING,
                     category: Union[str, Category] = MISSING,
                     title: str = MISSING) -> Schedule:
        """
        Create a new stream schedule segment.

        ???+ Warning
            The broadcaster must be a partner or affiliate.

        ???+ Note
            Specify the time zone using [IANA](https://nodatime.org/TimeZones) time zone format.

        | Scopes                    | Description                             |
        | ------------------------- | ----------------------------------------|
        | `channel:manage:schedule` | Create Channel Stream Schedule Segment. |

        Parameters
        ----------
        timezone: str
            The timezone for the schedule segment.
        duration: int
            The duration of the schedule segment in minutes.
        is_recurring: bool
            Indicates whether the schedule segment is recurring.
        start_time: datetime
            The start time of the schedule segment.
        category: Union[str, Category]
            The category (game) for the schedule segment.
        title: str
            The title of the schedule segment.

        Raises
        ------
        NotFound
            * Unable to find the requested category.
        BadRequest
            * The value in the timezone field is not valid.
            * The value in the duration field is not valid.
            * The string in the title field is too long.
        Unauthorized
            * The user access token must include the channel:manage:schedule scope.
        Forbidden
            * Only partners and affiliates may add non-recurring broadcast segments.

        Returns
        -------
        Schedule
            A Schedule object representing the newly created schedule segment.
        """
        if category is not MISSING:
            category = (await self.__state.get_category(category=category)).id
        data = await self.__state.http.create_channel_stream_schedule_segment(
            broadcaster_id=self.__state.user.id,
            timezone=timezone,
            duration=duration,
            is_recurring=is_recurring,
            start_time=start_time,
            category_id=category,
            title=title)
        return Schedule(data=data)

    async def delete(self, segment: ScheduleSegment) -> None:
        """
        Delete a stream schedule segment.

        ???+ Warning
            Removing a segment removes all segments in the recurring schedule.

        | Scopes                    | Description                             |
        | ------------------------- | ----------------------------------------|
        | `channel:manage:schedule` | Delete Channel Stream Schedule Segment. |

        Parameters
        ----------
        segment: ScheduleSegment
            The ScheduleSegment object representing the segment to be deleted.

        Raises
        ------
        BadRequest
            * The specified broadcast segment was not found.
        Unauthorized
            * The user access token must include the channel:manage:schedule scope.
        """
        await self.__state.http.delete_channel_stream_schedule_segment(broadcaster_id=self.__state.user.id,
                                                                       segment_id=segment.id)

    @overload
    async def update_settings(self,
                              vacation: Literal[True],
                              timezone: str,
                              end_time: datetime,
                              start_time: datetime = MISSING):
        ...

    @overload
    async def update_settings(self, vacation: Literal[False]):
        ...

    async def update_settings(self,
                              vacation: bool,
                              start_time: datetime = MISSING,
                              end_time: datetime = MISSING,
                              timezone: str = MISSING):
        """
        Update the stream schedule settings.

        ???+ Note
           Specify the time zone using [IANA](https://nodatime.org/TimeZones) time zone format.

        | Scopes                    | Description                     |
        | ------------------------- | --------------------------------|
        | `channel:manage:schedule` | Update Channel Stream Schedule. |

        Parameters
        ----------
        vacation: bool
            A boolean value indicating whether the broadcaster is on vacation mode.
        start_time: datetime
            The start time for the stream schedule.
        end_time: datetime
            The end time for the stream schedule.
        timezone: str
            The timezone for the stream schedule.

        Raises
        ------
        BadRequest
            * The vacation end time must be later than the date in vacation start time.
        Unauthorized
            * The user access token must include the channel:manage:schedule scope.
        NotFound
            * The broadcaster's schedule was not found.
        """
        await self.__state.http.update_channel_schedule_settings(broadcaster_id=self.__state.user.id,
                                                                 vacation=vacation,
                                                                 start_time=start_time,
                                                                 end_time=end_time,
                                                                 timezone=timezone)

    async def update_segment(self,
                             segment: ScheduleSegment,
                             start_time: datetime = MISSING,
                             duration: int = MISSING,
                             category: Union[str, Category] = MISSING,
                             title: str = MISSING,
                             timezone: str = MISSING,
                             is_canceled: bool = MISSING) -> ScheduleSegment:
        """
        Update a stream schedule segment.

        ???+ Note
            Specify the time zone using [IANA](https://nodatime.org/TimeZones) time zone format.

        | Scopes                    | Description                            |
        | ------------------------- | ---------------------------------------|
        | `channel:manage:schedule` | Update Channel Stream Schedule Segment |

        Parameters
        ----------
        segment: ScheduleSegment
            The ScheduleSegment object representing the segment to be updated.
        start_time: datetime
            The new start time for the segment.
        duration: int
            The new duration for the segment in minutes.
        category: Union[str, Category]
            The new category (game) for the segment.
        title: str
            The new title for the segment.
        timezone: str
            The new timezone for the segment.
        is_canceled: bool
            A boolean value indicating whether the segment should be canceled.

        Raises
        ------
        NotFound
            * Unable to find the requested category.
            * The specified broadcast segment was not found.
        BadRequest
            * The value in the timezone field is not valid.
            * The value in the duration field is not valid.
            * The string in the title field is too long.
        Unauthorized
            * The user access token must include the channel:manage:schedule scope.

        Returns
        -------
        ScheduleSegment
            A ScheduleSegment object representing the updated schedule segment.
        """
        if category is not MISSING:
            category = (await self.__state.get_category(category=category)).id
        data = await self.__state.http.update_channel_stream_schedule_segment(
            broadcaster_id=self.__state.user.id,
            segment_id=segment.id,
            start_time=start_time,
            duration=duration,
            category_id=category,
            title=title,
            timezone=timezone,
            is_canceled=is_canceled)
        return ScheduleSegment(data=data)


# ------------------------------
#    + Channel Chat AutoMod +
# ------------------------------
class ClientAutoMod(ChannelAutoMod):
    """
    Represents the AutoMod settings and actions for a channel.
    """

    __slots__ = ()

    def __init__(self, state: ConnectionState) -> None:
        super().__init__(state=state, broadcaster_id=state.user.id, moderator_id=state.user.id)

    async def check_messages(self, messages: Union[str, List[str]]) -> Union[bool, List[bool]]:
        """
        Check the AutoMod status for messages.

        | Scopes           | Description           |
        | ----------------- | ---------------------|
        | `moderation:read` | Check AutoMod Status |

        ??? Warning
            Rates are limited per channel based on the account type rather than per access token.

            | Account type | Limit per minute | Limit per hour |
            |--------------|------------------|----------------|
            | Normal       | 5                | 50             |
            | Affiliate    | 10               | 100            |
            | Partner      | 30               | 300            |

        Parameters
        ----------
        messages: Union[str, List[str]]
            The message(s) to check for AutoMod status. It can be a single message or a list of messages.

        Raises
        ------
        Unauthorized
            * The user access token must include the moderation:read scope.
        RateLimit
            * The broadcaster exceeded the number of chat message checks that they may make.

        Returns
        -------
        Union[bool, List[bool]]
            If a single message is provided,
                * returns a boolean indicating whether it's allowed by AutoMod.
            If a list of messages is provided
                * returns a list of booleans indicating the AutoMod status for each message.
        """
        if isinstance(messages, str):
            messages = [messages]
        data = await self.__state.http.check_automod_status(broadcaster_id=self.__state.user.id,
                                                            messages=messages)
        return data[0] if len(data) == 1 else data

    async def held_message(self, msg_id: str, allow: bool) -> None:
        """
        Manage held AutoMod messages.

        | Scopes                     | Description                   |
        | -------------------------- | ------------------------------|
        | `moderator:manage:automod` | Manage Held AutoMod Messages. |

        Parameters
        ----------
        msg_id: str
            The ID of the held AutoMod message to manage.
        allow: bool
            A boolean indicating whether to allow or deny the held AutoMod message.

        Raises
        ------
        NotFound
            * The message specified in the msg_id field was not found.
        Unauthorized
            * The user access token must include the moderator:manage:automod scope.
        """
        await self.__state.http.manage_held_automod_messages(user_id=self.__state.user.id,
                                                             msg_id=msg_id, allow=allow)


# ------------------------------
#    + Channel Client Chat  +
# ------------------------------
class ClientChat(ChannelChat):
    """
    Represents chat-related functionalities for a channel.
    """
    __slots__ = ()

    def __init__(self, state: ConnectionState) -> None:
        super().__init__(state, broadcaster_id=state.user.id, moderator_id=state.user.id)

    @property
    def automod(self) -> ClientAutoMod:
        """
        Access AutoMod-related functionalities for the channel.

        ClientAutoMod
            An instance of the ClientAutoMod class for managing AutoMod.
        """
        return ClientAutoMod(state=self._state)


# -----------------------------
#       + Client Stream +
# -----------------------------
class ClientStream(ChannelStream):
    __slots__ = ('_commercial_retry_in',)

    def __init__(self, state: ConnectionState) -> None:
        super().__init__(state, broadcaster_id=state.user.id, moderator_id=state.user.id)
        self._commercial_retry_in: int = 0

    async def start_commercial(self, length: int) -> int:
        data = await self.__state.http.start_commercial(broadcaster_id=self.__state.user.id, length=length)
        self._commercial_retry_in = time() + data['retry_after']
        return data['length']

    @property
    def is_commercial_cooldown(self) -> bool:
        if time() >= self._commercial_retry_in:
            return True
        return False

    async def start_raid(self, user: Union[str, BaseUser]) -> None:
        user = await self.__state.get_user(user)
        await self.__state.http.start_raid(broadcaster_id=self.__state.user.id, user_id=user.id)

    async def cancel_raid(self) -> None:
        await self.__state.http.cancel_raid(broadcaster_id=self.__state.user.id)


# ------------------------------
#       + Client Channel +
# ------------------------------
class ClientChannel(UserChannel):
    """
    Represents channel-related functionalities for a client.

    !!! Danger
        The attributes are read-only.

        These attributes are automatically updated via EventSub whenever channel information changes.

        Additional requests are unnecessary to fetch basic user information.

        To obtain additional information, such as `delay`, `tags`, and `is_branded_content`, use the
        `get_info()` method.

    Attributes
    ----------
    ccls: List[str]
        Content classification labels associated with the channel.
    title: str
        The title of the channel.
    language: str
        The language of the channel.
    category: Optional[Category]
        The category (game) associated with the channel, if available.
    """

    __slots__ = ('ccls', 'title', 'language', 'category')

    def __init__(self, state: ConnectionState, data: ChannelTypes.Channel) -> None:
        super().__init__(state=state, broadcaster_id=state.user.id)
        self.ccls: List[str] = data['content_classification_labels']
        self.title: str = data['title']
        self.language: str = data['broadcaster_language']
        self.category: Optional[Category] = Category(data=data) if data['game_id'] else None

    @property
    def chat(self) -> Optional[ClientChat]:
        """
        Access chat-related functionalities for the channel.

        Returns
        -------
        Optional[ClientChat]
            An instance of the ClientChat class for managing chat-related features.
        """
        return self._state.chat

    @property
    def stream(self) -> Optional[ClientStream]:
        """
        Access stream-related functionalities for the channel.

        Returns
        -------
        Optional[ClientStream]
            An instance of the ClientStream class for managing stream-related features.
        """
        return self._state.stream

    @property
    def extensions(self) -> ClientExtensions:
        """
        Access extension-related functionalities for the channel.

        Returns
        -------
        ClientExtensions
            An instance of the ClientExtensions class for managing channel extensions.
        """
        return ClientExtensions(state=self._state)

    @property
    def schedule(self) -> ClientSchedule:
        """
        Access stream schedule-related functionalities for the channel.

        Returns
        -------
        ClientSchedule
            An instance of the ClientSchedule class for managing the stream schedule.
        """
        return ClientSchedule(state=self._state)

    @property
    def reward(self) -> ClientReward:
        """
        Access reward-related functionalities for the channel.

        Returns
        -------
        ClientReward
            An instance of the ClientReward class for managing channel rewards.
        """
        return ClientReward(state=self._state)

    @property
    def prediction(self) -> ClientPrediction:
        """
        Access prediction-related functionalities for the channel.

        Returns
        -------
        ClientPrediction
            An instance of the ClientPrediction class for managing channel predictions.
        """
        return ClientPrediction(state=self._state)

    @property
    def poll(self) -> ClientPoll:
        """
        Access poll-related functionalities for the channel.

        Returns
        -------
        ClientPoll
            An instance of the ClientPoll class for managing channel polls.
        """
        return ClientPoll(state=self._state)

    @property
    def moderators(self) -> ClientModerators:
        """
        Access moderator-related functionalities for the channel.

        Returns
        -------
        ClientModerators
            An instance of the ClientModerators class for managing channel moderators.
        """
        return ClientModerators(state=self._state)

    @property
    def vips(self) -> ClientVips:
        """
        Access VIP-related functionalities for the channel.

        Returns
        -------
        ClientVips
            An instance of the ClientVips class for managing channel VIPs.

        """
        return ClientVips(state=self._state)

    @property
    def subscriptions(self) -> ClientSubscriptions:
        """
        Access subscription-related functionalities for the channel.

        Returns
        -------
        ClientSubscriptions
            An instance of the ClientSubscriptions class for managing channel subscriptions.
        """
        return ClientSubscriptions(state=self._state)

    @property
    def charity(self) -> ClientCharity:
        """
        Access charity-related functionalities for the channel.

        Returns
        -------
        ClientCharity
            An instance of the ClientCharity class for managing channel charity events.
        """
        return ClientCharity(state=self._state)

    async def update_ccls(self, ccls: List[ChannelTypes.CCLs], enable: bool) -> None:
        """
        Update content classification labels (CCLs) for the channel.

        | Scopes                     | Description                 |
        | -------------------------- | ----------------------------|
        | `channel:manage:broadcast` | Modify channel information. |

        Parameters
        ----------
        ccls: Literal[ChannelTypes.CCLs]
            A list of content classification labels to set for the channel.

            Can include one or more of the following values:

            * DrugsIntoxication
            * SexualThemes
            * ViolentGraphic
            * Gambling
            * ProfanityVulgarity

        enable: bool
            A boolean indicating whether to enable or disable the specified CCLs.

        Raises
        ------
        Unauthorized
            * User requests CCL for a channel they don’t own.
            * The OAuth token must include the channel:manage:broadcast scope.
        Forbidden
            * User requested gaming CCLs to be added to their channel.
            * Un-allowed CCLs declared for underage authorized user in a restricted country.
        RateLimit
            * User set the Branded Content flag too frequently.
        """
        await self._state.http.modify_channel_information(broadcaster_id=self._state.user.id,
                                                          ccls=ccls, ccls_enable=enable)

    async def update(self,
                     title: str = MISSING,
                     category: Optional[Union[str, Category]] = MISSING,
                     language: str = MISSING,
                     delay: int = MISSING,
                     tags: Optional[List[str]] = MISSING,
                     branded_content: bool = MISSING) -> None:
        """
        Update channel information.

        | Scopes                     | Description                 |
        | -------------------------- | ----------------------------|
        | `channel:manage:broadcast` | Modify channel information. |

        Parameters
        ----------
        title: str
            The new title for the channel.
        category: Optional[Union[str, Category]]
            The new category (game) for the channel.
        language: str
            The new language for the channel.
        delay: int
            The stream delay for the channel.
        tags: Optional[List[str]]
            A list of new tags for the channel.
        branded_content: bool
            A boolean indicating whether branded content is enabled for the channel.

        Raises
        ------
        NotFound
            * Unable to find the requested category.
        ValueError
            * Delay must be integer and maximum of 900 seconds.
        BadRequest
            * The title field may not contain an empty string.
            * The list in the tag's field exceeds the maximum number of tags allowed.
            * A tag in the tag's field exceeds the maximum length allowed.
            * A tag in the tag's field contains special characters or spaces.
            * One or more tags in the tag's field failed AutoMod review.
            * Game restricted for user's age and region
        Unauthorized
            * The OAuth token must include the channel:manage:broadcast scope.
        RateLimit
            * User set the Branded Content flag too frequently.
        """
        if category is not MISSING:
            category = (await self._state.get_category(category)).id
        await self._state.http.modify_channel_information(broadcaster_id=self._state.user.id,
                                                          category_id=category,
                                                          language=language,
                                                          title=title,
                                                          delay=delay,
                                                          tags=tags,
                                                          branded_content=branded_content)

    async def fetch_banned_users(self, limit: int = 4) -> AsyncGenerator[List[BannedUser]]:
        """
        Fetch banned users from the channel.

        ???+ Warning
            This method uses [pagination](https://dev.twitch.tv/docs/api/guide/#pagination).
            Set the limit to -1 to retrieve all data, but be cautious of potential performance
            and rate limit impacts.

        | Scopes                                                | Description       |
        | ------------------------------------------------------| ------------------|
        | `moderation:read` or `moderator:manage:banned_users`  | Get Banned Users. |

        Parameters
        ----------
        limit: int
            The maximum number of banned users to fetch.

        Raises
        ------
        Unauthorized
            * The user access token must include the moderation:read or moderator:manage:banned_users scope.

        Yields
        ------
        AsyncGenerator[List[BannedUser]]
            An asynchronous generator that yields a list of BannedUser objects representing banned users.
        """

        async for banned_users in self._state.http.fetch_banned_users(limit=limit,
                                                                      broadcaster_id=self._state.user.id):
            yield [BannedUser(data=user) for user in banned_users]

    async def get_banned_users(self, users: List[Union[str, BaseUser]]) -> List[BannedUser]:
        """
        Get information about banned users in the channel.

        | Scopes                                                | Description       |
        | ------------------------------------------------------| ------------------|
        | `moderation:read` or `moderator:manage:banned_users`  | Get Banned Users. |

        Parameters
        ----------
        users: List[Union[str, BaseUser]]
            A list of users for which to fetch ban information.

        Raises
        ------
        Unauthorized
            * The user access token must include the moderation:read or moderator:manage:banned_users scope.

        Returns
        -------
        List[BannedUser]
            A list of BannedUser objects representing banned users in the channel.
        """
        user_ids = [user.id for user in (await self._state.get_users(users))]
        async for banned_users in self._state.http.fetch_banned_users(limit=1,
                                                                      broadcaster_id=self._state.user.id,
                                                                      user_ids=user_ids):
            return [BannedUser(data=user) for user in banned_users]

    async def get_editors(self) -> List[Editor]:
        """
        Get the editors for the channel.

        | Scopes                  | Description          |
        | ----------------------- | ---------------------|
        | `channel:read:editors`  | Get Channel Editors. |


        Raises
        ------
        Unauthorized
            * The OAuth token must include the channel:read:editors scope.

        Returns
        -------
        List[Editor]
            A list of Editor objects representing the channel's editors.
        """
        editors = await self._state.http.get_channel_editors(broadcaster_id=self._state.user.id)
        return [Editor(data=editor) for editor in editors]

    async def delete_videos(self, videos: List[Union[Clip, Video]]) -> List[str]:
        """
        Delete videos from the channel.

        ???+ Warning
            After deleting videos, they will be removed from your channel.
            Keep in mind that while the videos are gone, it might take a few minutes for them to fully
            disappear from Twitch's backend systems.

        | Scopes                  | Description       |
        | ----------------------- | ----------------- |
        | `channel:manage:videos` | Delete Videos.    |

        Parameters
        ----------
        videos: List[Union[Clip, Video]]
            A list of Clip or Video objects representing the videos to be deleted.

        Raises
        ------
        Unauthorized
            * The caller is not authorized to delete the specified video.
            * The user access token must include the channel:manage:videos scope.

        Returns
        -------
        List[str]
            A list of video IDs that were successfully deleted.
        """
        video_ids = [
            i.id if isinstance(i, Video) else
            i.video_id if isinstance(i, Clip) else i for i in videos
        ]
        # You can delete a maximum of 5 videos per request.
        for i in range(0, len(video_ids), 5):
            batch = video_ids[i:i + 5]  # Get the next batch of 5 elements
            data = await self._state.http.delete_videos(video_ids=batch)
            return data
        return []

    async def get_goals(self) -> List[Goal]:
        """
        Get the goals associated with the channel.

        | Scopes               | Description        |
        | -------------------- | -------------------|
        | `channel:read:goals` | Get Creator Goals. |

        Raises
        ------
        Unauthorized
            * The user access token must include the channel:read:goals scope.

        Returns
        -------
        List[Goal]
            A list of Goal objects representing the channel's goals.
        """
        data = await self._state.http.get_goals(broadcaster_id=self._b_id)
        return [Goal(data=goal) for goal in data]

    async def get_bits_leaderboard(self,
                                   count: int = 10,
                                   period: Literal['day', 'week', 'month', 'year', 'all'] = 'all',
                                   started_at: datetime = MISSING,
                                   user: BaseUser = MISSING) -> List[BitsLeaderboard]:
        """
        Get the bit's leaderboard for the channel.

        | Scopes                 | Description           |
        | ---------------------- | --------------------- |
        | `bits:read`            | Get Bits Leaderboard. |

        Parameters
        ----------
        count: int
            The number of users to retrieve in the leaderboard.
        period: Literal['day', 'week', 'month', 'year', 'all']
            The time period for the leaderboard.
        started_at: datetime
            The start date and time for the leaderboard.
        user: BaseUser
            The user object for which to retrieve the leaderboard.

        Raises
        -----
        NotFound
            * Unable to find the requested user.
        Unauthorized
            * The user access token must include the bits:read scope.

        Returns
        -------
        List[BitsLeaderboard]
            A list of BitsLeaderboard objects representing the bit's leaderboard.
        """
        if user is not MISSING:
            user = (await self._state.get_user(user)).id
        users = await self._state.http.get_bits_leaderboard(count=count, period=period,
                                                            started_at=started_at, user_id=user)
        return [BitsLeaderboard(data=user) for user in users]

    async def fetch_hype_trains(self, limit: int = 4) -> AsyncGenerator[List[HypeTrain]]:
        """
        Fetch Hype Trains from the channel.

        ???+ Warning
            This method uses [pagination](https://dev.twitch.tv/docs/api/guide/#pagination).
            Set the limit to -1 to retrieve all data, but be cautious of potential performance
            and rate limit impacts.

        | Scopes                     | Description            |
        | ---------------------------| -----------------------|
        | `channel:read:hype_train`  | Get Hype Train Events. |

        Parameters
        ----------
        limit: int
            The maximum number of Hype Trains to fetch.

        Raises
        ------
        Unauthorized
            * The user access token must include the channel:read:hype_train scope.

        Yields
        ------
        AsyncGenerator[List[HypeTrain]]
            An asynchronous generator that yields a list of HypeTrain objects representing Hype Trains.
        """
        async for data in self._state.http.fetch_hype_trains(limit=limit,
                                                             broadcaster_id=self._state.user.id):
            yield [HypeTrain(data=data) for data in data]

    async def get_stream_key(self) -> str:
        """
        Get the stream key for the channel.

        | Scopes                      | Description            |
        | ----------------------------| -----------------------|
        | ` channel:read:stream_key`  | Get Hype Train Events. |

        Raises
        ------
        Unauthorized
            * The user access token must include the channel:read:stream_key scope.

        Returns
        -------
        str
            The stream key for the channel.
        """
        data = await self._state.http.get_channel_stream_key(broadcaster_id=self._state.user.id)
        return data
