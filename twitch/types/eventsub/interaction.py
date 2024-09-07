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

from .users import SpecificBroadcaster, SpecificUser
from typing import TYPE_CHECKING, TypedDict
from .chat import TextEmoteMessage

if TYPE_CHECKING:
    from typing import Optional, List, Literal


# Reward
class Emote(TypedDict):
    """
    Represents an emote with its ID and availability times.

    Attributes
    ----------
    id: str
        The ID of the emote.
    begin: int
        The start time of the emotes availability, in Unix timestamp format.
    end: int
        The end time of the emotes availability, in Unix timestamp format.
    """
    id: str
    begin: int
    end: int


class UnlockedEmote(TypedDict):
    """
    Represents an emote that has been unlocked.

    Attributes
    ----------
    id: str
        The ID of the unlocked emote.
    name: str
        The name of the unlocked emote.
    """
    id: str
    name: str


class AutomaticReward(TypedDict):
    """
    Represents an automatic reward with its type and details.

    Attributes
    ----------
    type: str
        The type of event. Possible values include:

        - single_message_bypass_sub_mode
        - send_highlighted_message
        - random_sub_emote_unlock
        - chosen_sub_emote_unlock
        - chosen_modified_sub_emote_unlock
        - message_effect
        - gigantify_an_emote
        - celebration
    cost: int
        The cost of the reward in channel points or other currency.
    unlocked_emote: Optional[UnlockedEmote]
        Details of an emote unlocked by the reward, if applicable.
    """
    type: Literal['single_message_bypass_sub_mode',
                  'send_highlighted_message',
                  'random_sub_emote_unlock',
                  'chosen_sub_emote_unlock',
                  'chosen_modified_sub_emote_unlock',
                  'message_effect',
                  'gigantify_an_emote',
                  'celebration']
    cost: int
    unlocked_emote: Optional[UnlockedEmote]


class AutomaticRewardRedemptionAddEvent(SpecificBroadcaster, SpecificUser):
    """
    Represents an event where an automatic reward is redeemed.

    Attributes
    ----------
    id: str
        The ID of the reward redemption event.
    reward: AutomaticReward
        The details of the automatic reward redeemed.
    message: TextEmoteMessage
        The message associated with the reward redemption.
    user_input: Optional[str]
        Additional user input, if any, provided during the redemption.
    redeemed_at: str
        The timestamp when the reward was redeemed, in ISO 8601 format.
    """
    id: str
    reward: AutomaticReward
    message: TextEmoteMessage
    user_input: Optional[str]
    redeemed_at: str


class Image(TypedDict):
    """
    Represents an image with multiple resolution options.

    Attributes
    ----------
    url_1x: Optional[str]
        URL of the image at 1x resolution.
    url_2x: Optional[str]
        URL of the image at 2x resolution.
    url_4x: Optional[str]
        URL of the image at 4x resolution.
    """
    url_1x: Optional[str]
    url_2x: Optional[str]
    url_4x: Optional[str]


class PointRewardEvent(SpecificBroadcaster):
    """
    Represents custom point reward event.

    Attributes
    ----------
    id: str
        The ID of the reward.
    is_enabled: bool
        Whether the reward is currently enabled.
    is_paused: bool
        Whether the reward is currently paused.
    is_in_stock: bool
        Whether the reward is in stock.
    title: str
        The title of the reward.
    cost: int
        The cost of the reward in channel points or other currency.
    prompt: str
        The prompt or description for the reward.
    is_user_input_required: bool
        Whether user input is required to redeem the reward.
    should_redemptions_skip_request_queue: bool
        Whether redemptions should skip the request queue.
    max_per_stream: Optional[int]
        The maximum number of redemptions allowed per stream, if applicable.
    max_per_user_per_stream: Optional[int]
        The maximum number of redemptions allowed per user per stream, if applicable.
    background_color: Optional[str]
        The background color of the reward's display.
    image: Optional[Image]
        The image associated with the reward.
    default_image: Optional[Image]
        The default image to display for the reward.
    global_cooldown: Optional[int]
        The global cooldown for the reward, in seconds.
    cooldown_expires_at: Optional[str]
        The timestamp when the cooldown expires, in ISO 8601 format.
    redemptions_redeemed_current_stream: Optional[int]
        The number of redemptions redeemed in the current stream.
    """
    id: str
    is_enabled: bool
    is_paused: bool
    is_in_stock: bool
    title: str
    cost: int
    prompt: str
    is_user_input_required: bool
    should_redemptions_skip_request_queue: bool
    max_per_stream: Optional[int]
    max_per_user_per_stream: Optional[int]
    background_color: Optional[str]
    image: Optional[Image]
    default_image: Optional[Image]
    global_cooldown: Optional[int]
    cooldown_expires_at: Optional[str]
    redemptions_redeemed_current_stream: Optional[int]


class RewardInfo(TypedDict):
    """
    Represents basic information about a reward.

    Attributes
    ----------
    id: str
        The ID of the reward.
    title: str
        The title of the reward.
    cost: int
        The cost of the reward in channel points or other currency.
    """
    id: str
    title: str
    cost: int


class RewardRedemptionEvent(SpecificBroadcaster, SpecificUser):
    """
    Represents an event where a reward redemption occurs.

    Attributes
    ----------
    id: str
        The ID of the reward redemption event.
    user_input: str
        The user input provided during the reward redemption.
    status: Literal['unknown', 'unfulfilled', 'fulfilled', 'canceled']
        The current status of the reward redemption.
    reward: RewardInfo
        Basic information about the reward redeemed.
    redeemed_at: str
        The timestamp when the reward was redeemed, in ISO 8601 format.
    """
    id: str
    user_input: str
    status: Literal['unknown', 'unfulfilled', 'fulfilled', 'canceled']
    reward: RewardInfo
    redeemed_at: str


# Poll
class Choice(TypedDict):
    """
    Represents a choice in a poll.

    Attributes
    ----------
    id: str
        The ID of the choice.
    title: str
        The title of the choice.
    bits_votes: int
        The number of votes cast with bits for this choice.
    channel_points_votes: int
        The number of votes cast with channel points for this choice.
    """
    id: str
    title: str
    bits_votes: int
    channel_points_votes: int


class Voting(TypedDict):
    """
    Represents the voting configuration for a poll.

    Attributes
    ----------
    is_enabled: bool
        Whether voting is enabled for the poll.
    amount_per_vote: int
        The amount of currency required per vote.
    """
    is_enabled: bool
    amount_per_vote: int


class PollBase(SpecificBroadcaster):
    """
    Represents the base attributes for a poll.

    Attributes
    ----------
    id: str
        The ID of the poll.
    title: str
        The title of the poll.
    choices: List[Choice]
        A list of choices available in the poll.
    bits_voting: Voting
        The voting configuration for bits.
    channel_points_voting: Voting
        The voting configuration for channel points.
    started_at: str
        The timestamp when the poll started, in ISO 8601 format.
    """
    id: str
    title: str
    choices: List[Choice]
    bits_voting: Voting
    channel_points_voting: Voting
    started_at: str


class PollBeginEvent(PollBase):
    """
    Represents an event where a poll begins.

    Attributes
    ----------
    ends_at: str
        The timestamp when the poll ends, in ISO 8601 format.
    """
    ends_at: str


class PollProgressEvent(PollBase):
    """
    Represents an event where a poll is in progress.

    Attributes
    ----------
    ends_at: str
        The timestamp when the poll ends, in ISO 8601 format.
    """
    ends_at: str


class PollEndEvent(PollBase):
    """
    Represents an event where a poll ends.

    Attributes
    ----------
    status: Literal['completed', 'archived', 'terminated']
        The status of the poll at the end.
    ended_at: str
        The timestamp when the poll ended, in ISO 8601 format.
    """
    status: Literal['completed', 'archived', 'terminated']
    ended_at: str


# Prediction
class TopPredictor(SpecificUser):
    """
    Represents a top predictor in a prediction.

    Attributes
    ----------
    channel_points_used: int
        The amount of channel points used by the top predictor.
    channel_points_won: Optional[int]
        The amount of channel points won by the top predictor, if applicable.
    """
    channel_points_used: int
    channel_points_won: Optional[int]


class Outcome(TypedDict):
    """
    Represents an outcome in a prediction.

    Attributes
    ----------
    id: str
        The ID of the outcome.
    title: str
        The title of the outcome.
    color: Literal['BLUE', 'PINK']
        The color associated with the outcome.
    users: int
        The number of users who predicted this outcome.
    channel_points: int
        The total channel points associated with this outcome.
    top_predictors: Optional[List[TopPredictor]]
        A list of top predictors for this outcome, if applicable.
    """
    id: str
    title: str
    color: Literal['BLUE', 'PINK']
    users: int
    channel_points: int
    top_predictors: Optional[List[TopPredictor]]


class PredictionBase(SpecificBroadcaster):
    """
    Represents the base attributes for a prediction.

    Attributes
    ----------
    id: str
        The ID of the prediction.
    title: str
        The title of the prediction.
    outcomes: List[Outcome]
        A list of outcomes for the prediction.
    started_at: str
        The timestamp when the prediction started, in ISO 8601 format.
    """
    id: str
    title: str
    outcomes: List[Outcome]
    started_at: str


class PredictionBeginEvent(PredictionBase):
    """
    Represents an event where a prediction begins.

    Attributes
    ----------
    locks_at: str
        The timestamp when the prediction locks, in ISO 8601 format.
    """
    locks_at: str


class PredictionProgressEvent(PredictionBase):
    """
    Represents an event where a prediction is in progress.

    Attributes
    ----------
    locks_at: str
        The timestamp when the prediction locks, in ISO 8601 format.
    """
    locks_at: str


class PredictionLockEvent(PredictionBase):
    """
    Represents an event where a prediction locks.

    Attributes
    ----------
    locked_at: str
        The timestamp when the prediction was locked, in ISO 8601 format.
    """
    locked_at: str


class PredictionEndEvent(PredictionBase):
    """
    Represents an event where a prediction ends.

    Attributes
    ----------
    winning_outcome_id: str
        The ID of the winning outcome.
    status: Literal['resolved', 'canceled']
        The status of the prediction at the end.
    ended_at: str
        The timestamp when the prediction ended, in ISO 8601 format.
    """
    winning_outcome_id: str
    status: Literal['resolved', 'canceled']
    ended_at: str


# HypeTrain
class Contribution(SpecificUser):
    """
    Represents a contribution to a Hype Train.

    Attributes
    ----------
    type: Literal['bits', 'subscription']
        The type of contribution.
    total: int
        The total amount of the contribution.
    """
    type: Literal['bits', 'subscription']
    total: int


class HypeTrainEvent(SpecificBroadcaster):
    """
    Represents a Hype Train event.

    Attributes
    ----------
    id: str
        The ID of the Hype Train event.
    total: int
        The total amount of contributions to the Hype Train.
    progress: int
        The current progress of the Hype Train.
    goal: int
        The goal amount for the Hype Train.
    top_contributions: List[Contribution]
        A list of top contributions to the Hype Train.
    last_contribution: Contribution
        The most recent contribution to the Hype Train.
    started_at: str
        The timestamp when the Hype Train started, in ISO 8601 format.
    expires_at: str
        The timestamp when the Hype Train expires, in ISO 8601 format.
    """
    id: str
    total: int
    progress: int
    goal: int
    top_contributions: List[Contribution]
    last_contribution: Contribution
    started_at: str
    expires_at: str


class HypeTrainEndEvent(SpecificBroadcaster):
    """
    Represents an event where a Hype Train ends.

    Attributes
    ----------
    id: str
        The ID of the Hype Train event.
    level: int
        The level reached by the Hype Train.
    total: int
        The total amount of contributions to the Hype Train.
    top_contributions: List[Contribution]
        A list of top contributions to the Hype Train.
    started_at: str
        The timestamp when the Hype Train started, in ISO 8601 format.
    ended_at: str
        The timestamp when the Hype Train ended, in ISO 8601 format.
    cooldown_ends_at: str
        The timestamp when the cooldown period ends, in ISO 8601 format.
    """
    id: str
    level: int
    total: int
    top_contributions: List[Contribution]
    started_at: str
    ended_at: str
    cooldown_ends_at: str
