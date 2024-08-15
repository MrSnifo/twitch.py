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
OR IMPLIED, INCLUDING BUT NOT firstED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from __future__ import annotations

from .users import SpecificUser, Broadcaster
from typing import TypedDict, TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List, Literal, NotRequired, Optional


# HypeTrain
class HypeTrainContributor(TypedDict):
    """
    Represents a contributor to a Hype Train event.

    Attributes
    ----------
    type: Literal['bits', 'subscription', 'other']
        The type of contribution (e.g., bits, subscription).
    user: str
        The user who made the contribution.
    total: int
        The total amount contributed by the user.
    """
    type: Literal['bits', 'subscription', 'other']
    user: str
    total: int


class HypeTrain(TypedDict):
    """
    Represents a Hype Train event.

    Attributes
    ----------
    id: str
        The unique identifier for the Hype Train.
    total: int
        The total amount of contributions.
    level: int
        The level achieved in the Hype Train.
    started_at: str
        The timestamp when the Hype Train started.
    goal: str
        The goal required to reach the next level.
    expires_at: str
        The timestamp when the Hype Train expires.
    broadcaster_id: str
        The ID of the broadcaster during the Hype Train.
    cooldown_end_time: str
        The timestamp when the cooldown period ends.
    last_contribution: HypeTrainContributor
        The last contribution made during the Hype Train.
    top_contributions: List[HypeTrainContributor]
        A list of the top contributions made during the Hype Train.
    """
    id: str
    total: int
    level: int
    started_at: str
    goal: str
    expires_at: str
    broadcaster_id: str
    cooldown_end_time: str
    last_contribution: HypeTrainContributor
    top_contributions: List[HypeTrainContributor]


# Polls
PollStatus = Literal['ACTIVE', 'COMPLETED', 'TERMINATED', 'ARCHIVED', 'MODERATED', 'INVALID']


class PollChoice(TypedDict, total=False):
    """
    Represents a choice in a poll.

    Attributes
    ----------
    id: str
        The unique identifier for the poll choice.
    title: str
        The title of the poll choice.
    votes: int
        The number of votes this choice received.
    bits_votes: int
        The number of bits votes this choice received.
    channel_points_votes: int
        The number of channel points votes this choice received.
    """
    id: str
    title: str
    votes: NotRequired[int]
    bits_votes: NotRequired[int]
    channel_points_votes: NotRequired[int]
    

class Poll(Broadcaster):
    """
    Represents a poll.

    Attributes
    ----------
    id: str
        The unique identifier for the poll.
    title: str
        The title of the poll.
    choices: List[PollChoice]
        A list of choices available in the poll.
    started_at: str
        The timestamp when the poll started.
    status: PollStatus
        The current status of the poll.
    duration: int
        The duration of the poll in seconds.
    ended_at: Optional[str]
        The timestamp when the poll ended, if applicable.
    bits_per_vote: int
        The cost of a vote in bits, if bits voting is enabled.
    bits_voting_enabled: bool
        Indicates if bits voting is enabled.
    channel_points_per_vote: int
        The cost of a vote in channel points, if channel points voting is enabled.
    channel_points_voting_enabled: bool
        Indicates if channel points voting is enabled.
    """
    id: str
    title: str
    choices: List[PollChoice]
    started_at: str
    status: PollStatus
    duration: int
    ended_at: Optional[str]
    bits_per_vote: int
    bits_voting_enabled: bool
    channel_points_per_vote: int
    channel_points_voting_enabled: bool


# Prediction
class Predictor(SpecificUser):
    """
    Represents a predictor in a channel prediction.

    Attributes
    ----------
    channel_points_won: Optional[int]
        The number of channel points won by the predictor.
    channel_points_used: int
        The number of channel points used by the predictor.
    """
    channel_points_won: Optional[int]
    channel_points_used: int


class Outcome(TypedDict, total=False):
    """
    Represents an outcome in a channel prediction.

    Attributes
    ----------
    id: str
        The unique identifier for the outcome.
    color: str
        The color associated with the outcome.
    title: str
        The title of the outcome.
    users: int
        The number of users who predicted this outcome.
    channel_points: int
        The total number of channel points used for this outcome.
    top_predictors: List[Predictor]
        A list of the top predictors for this outcome.
    """
    id: str
    color: str
    title: str
    users: NotRequired[int]
    channel_points: NotRequired[int]
    top_predictors: NotRequired[List[Predictor]]


class Prediction(TypedDict):
    """
    Represents a channel prediction.

    Attributes
    ----------
    id: str
        The unique identifier for the prediction.
    title: str
        The title of the prediction.
    outcomes: List[Outcome]
        A list of possible outcomes for the prediction.
    status: Literal['ACTIVE', 'CANCELED', 'LOCKED', 'RESOLVED']
        The current status of the prediction.
    ended_at: Optional[str]
        The timestamp when the prediction ended, if applicable.
    locked_at: Optional[str]
        The timestamp when the prediction was locked, if applicable.
    created_at: str
        The timestamp when the prediction was created.
    prediction_window: int
        The time window in seconds during which users can participate in the prediction.
    winning_outcome_id: Optional[str]
        The ID of the winning outcome, if the prediction has been resolved.
    """
    id: str
    title: str
    outcomes: List[Outcome]
    status: Literal['ACTIVE', 'CANCELED', 'LOCKED', 'RESOLVED']
    ended_at: Optional[str]
    locked_at: Optional[str]
    created_at: str
    prediction_window: int
    winning_outcome_id: Optional[str]


# Reward
class RewardImages(TypedDict):
    """
    Represents images for a channel reward.

    Attributes
    ----------
    url_1x: str
        The URL for the 1x resolution image.
    url_2x: str
        The URL for the 2x resolution image.
    url_4x: str
        The URL for the 4x resolution image.
    """
    url_1x: str
    url_2x: str
    url_4x: str


class BaseReward(TypedDict):
    """
    A base class used to Represents common attributes of a channel reward.

    Attributes
    ----------
    id: str
        The unique identifier for the reward.
    cost: int
        The cost of the reward in channel points.
    title: str
        The title of the reward.
    prompt: str
        The prompt or description of the reward.
    """
    id: str
    cost: int
    title: str
    prompt: str


class MaxPerStreamSetting(TypedDict):
    """
    Represents settings for the maximum number of times a reward can be redeemed per stream.

    Attributes
    ----------
    is_enabled: bool
        Indicates if the setting is enabled.
    max_per_stream: int
        The maximum number of times the reward can be redeemed per stream.
    """
    is_enabled: bool
    max_per_stream: int


class MaxPerUserPerStreamSetting(TypedDict):
    """
    Represents settings for the maximum number of times a reward can be redeemed per user per stream.

    Attributes
    ----------
    is_enabled: bool
        Indicates if the setting is enabled.
    max_per_user_per_stream: int
        The maximum number of times the reward can be redeemed per user per stream.
    """
    is_enabled: bool
    max_per_user_per_stream: int


class GlobalCooldownSetting(TypedDict):
    """
    Represents settings for the global cooldown of a reward.

    Attributes
    ----------
    is_enabled: bool
        Indicates if the global cooldown is enabled.
    global_cooldown_seconds: int
        The number of seconds for the global cooldown.
    """
    is_enabled: bool
    global_cooldown_seconds: int


class Reward(Broadcaster, BaseReward):
    """
    Represents a channel reward.

    Attributes
    ----------
    image: Optional[RewardImages]
        The custom image for the reward, if applicable.
    is_paused: bool
        Indicates if the reward is paused.
    is_enabled: bool
        Indicates if the reward is enabled.
    is_in_stock: bool
        Indicates if the reward is in stock.
    default_image: RewardImages
        The default image for the reward.
    background_color: str
        The background color for the reward.
    cooldown_expires_at: Optional[str]
        The timestamp when the cooldown for the reward expires, if applicable.
    is_user_input_required: bool
        Indicates if user input is required to redeem the reward.
    max_per_stream_setting: MaxPerStreamSetting
        The settings for the maximum number of redemptions per stream.
    global_cooldown_setting: GlobalCooldownSetting
        The settings for the global cooldown of the reward.
    max_per_user_per_stream_setting: MaxPerUserPerStreamSetting
        The settings for the maximum number of redemptions per user per stream.
    redemptions_redeemed_current_stream: Optional[int]
        The number of redemptions of the reward during the current stream, if applicable.
    should_redemptions_skip_request_queue: bool
        Indicates if redemptions should skip the request queue.
    """
    image: Optional[RewardImages]
    is_paused: bool
    is_enabled: bool
    is_in_stock: bool
    default_image: RewardImages
    background_color: str
    cooldown_expires_at: Optional[str]
    is_user_input_required: bool
    max_per_stream_setting: MaxPerStreamSetting
    global_cooldown_setting: GlobalCooldownSetting
    max_per_user_per_stream_setting: MaxPerUserPerStreamSetting
    redemptions_redeemed_current_stream: Optional[int]
    should_redemptions_skip_request_queue: bool


class RewardRedemption(Broadcaster, SpecificUser):
    """
    Represents a reward redemption.

    Attributes
    ----------
    id: str
        The unique identifier for the redemption.
    status: Literal['CANCELED', 'FULFILLED', 'UNFULFILLED']
        The current status of the redemption.
    reward: BaseReward
        The reward associated with this redemption.
    user_input: str
        The input provided by the user when redeeming the reward.
    redeemed_at: str
        The timestamp when the reward was redeemed.
    """
    id: str
    status: Literal['CANCELED', 'FULFILLED', 'UNFULFILLED']
    reward: BaseReward
    user_input: str
    redeemed_at: str

