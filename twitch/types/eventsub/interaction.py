"""
The MIT License (MIT)

Copyright (c) 2025-present Snifo

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

from typing import TypedDict, List, Optional, Literal
from .users import SpecificBroadcaster, SpecificUser


# Reward
UnlockedEmoteV1 = TypedDict('UnlockedEmoteV1', {'id': str, 'name': str})
MessageEmoteV1 = TypedDict('MessageEmoteV1', {'id': str, 'begin': int, 'end': int})
MessageV1 = TypedDict('MessageV1', {'text': str, 'emotes': List[MessageEmoteV1]})
RewardV1 = TypedDict('RewardV1', {
    'type': Literal[
        'single_message_bypass_sub_mode',
        'send_highlighted_message',
        'random_sub_emote_unlock',
        'chosen_sub_emote_unlock',
        'chosen_modified_sub_emote_unlock',
        'message_effect',
        'gigantify_an_emote',
        'celebration'
    ],
    'cost': int,
    'unlocked_emote': Optional[UnlockedEmoteV1]
})

class AutomaticRewardRedemptionAddEventV1(TypedDict):
    """
    Twitch EventSub payload for automatic channel point reward redemptions (v1).

    Attributes
    ----------
    id: str
        Unique redemption ID
    broadcaster_user_id: str
        The ID of the channel where the reward was redeemed.
    broadcaster_user_login: str
        The login of the channel where the reward was redeemed.
    broadcaster_user_name: str
        The display name of the channel where the reward was redeemed.
    user_id: str
        The ID of the redeeming user.
    user_login: str
        The login of the redeeming user.
    user_name: str
        The display name of the redeeming user.
    reward: Reward
        Details about the redeemed reward with structure:
        {
            'type': Literal[
                'single_message_bypass_sub_mode',
                'send_highlighted_message',
                'random_sub_emote_unlock',
                'chosen_sub_emote_unlock',
                'chosen_modified_sub_emote_unlock',
                'message_effect',
                'gigantify_an_emote',
                'celebration'
            ],
            'cost': int,
            'unlocked_emote': Optional[{'id': str, 'name': str}]
        }
    message: Message
        Associated chat message data with structure:
        {
            'text': str,
            'emotes': List[{'id': str, 'begin': int, 'end': int}]
        }
    user_input: Optional[str]
        User-provided text input if required
    redeemed_at: str
        UTC timestamp in RFC3339 format
    """
    id: str
    broadcaster_user_id: str
    broadcaster_user_login: str
    broadcaster_user_name: str
    user_id: str
    user_login: str
    user_name: str
    reward: RewardV1
    message: MessageV1
    user_input: Optional[str]
    redeemed_at: str


EmoteV2 = TypedDict('EmoteV2', {'id': str, 'name': str})
MessageFragmentV2 = TypedDict('MessageFragmentV2', {'text': str,
                                                    'type': Literal['text', 'emote'],
                                                    'emote': Optional[EmoteV2]})
MessageV2 = TypedDict('MessageV2', {'text': str, 'fragments': List[MessageFragmentV2]})
RewardV2 = TypedDict('RewardV2', {
    'type': Literal[
        'single_message_bypass_sub_mode',
        'send_highlighted_message',
        'random_sub_emote_unlock',
        'chosen_sub_emote_unlock',
        'chosen_modified_sub_emote_unlock'
    ], 'channel_points': int, 'emote': Optional[EmoteV2]
})

class AutomaticRewardRedemptionAddEventV2(TypedDict):
    """
    Twitch EventSub payload for automatic channel point reward redemptions (v2).

    Attributes
    ----------
    id: str
        Unique redemption ID
    broadcaster_user_id: str
        The ID of the channel where the reward was redeemed.
    broadcaster_user_login: str
        The login of the channel where the reward was redeemed.
    broadcaster_user_name: str
        The display name of the channel where the reward was redeemed.
    user_id: str
        The ID of the redeeming user.
    user_login: str
        The login of the redeeming user.
    user_name: str
        The display name of the redeeming user.

    reward: RewardV2
        Details about the redeemed reward with structure:
        {
            'type': Literal[
                'single_message_bypass_sub_mode',
                'send_highlighted_message',
                'random_sub_emote_unlock',
                'chosen_sub_emote_unlock',
                'chosen_modified_sub_emote_unlock'
            ],
            'channel_points': int,
            'emote': Optional[{'id': str, 'name': str}]
        }
    message: MessageV2
        Associated chat message data with structure:
        {
            'text': str,
            'fragments': List[{
                'text': str,
                'type': Literal['text', 'emote'],
                'emote': Optional[{'id': str, 'name': str}]
            }]
        }
    redeemed_at: str
        UTC timestamp in RFC3339 format
    """
    id: str
    broadcaster_user_id: str
    broadcaster_user_login: str
    broadcaster_user_name: str
    user_id: str
    user_login: str
    user_name: str
    reward: RewardV2
    message: Optional[MessageV2]
    redeemed_at: str


Image = TypedDict('Image', {'url_1x': str, 'url_2x': str, 'url_4x': str})
MaxPerStream = TypedDict('MaxPerStream', {'is_enabled': bool, 'max_per_stream': int})
MaxPerUserPerStream = TypedDict('MaxPerUserPerStream', {'is_enabled': bool, 'max_per_user_per_stream': int})
GlobalCooldown = TypedDict('GlobalCooldown', {'is_enabled': bool, 'global_cooldown_seconds': int})
RewardImage = TypedDict('RewardImage', {'image': Optional[Image], 'default_image': Image})

class PointRewardEvent(TypedDict):
    """
    Twitch EventSub payload for channel points custom reward add events.

    Attributes
    ----------
    id: str
        The reward identifier.
    broadcaster_user_id: str
        The requested broadcaster ID.
    broadcaster_user_login: str
        The requested broadcaster login.
    broadcaster_user_name: str
        The requested broadcaster display name.
    is_enabled: bool
        Is the reward currently enabled. If false, the reward won't show up to viewers.
    is_paused: bool
        Is the reward currently paused. If true, viewers can't redeem.
    is_in_stock: bool
        Is the reward currently in stock. If false, viewers can't redeem.
    title: str
        The reward title.
    cost: int
        The reward cost.
    prompt: str
        The reward description.
    is_user_input_required: bool
        Does the viewer need to enter information when redeeming the reward.
    should_redemptions_skip_request_queue: bool
        Should redemptions be set to fulfilled status immediately when redeemed.
    max_per_stream: {'is_enabled': bool, 'max_per_stream': int}
        Whether a maximum per stream is enabled and what the maximum is.
    max_per_user_per_stream: {'is_enabled': bool, 'max_per_user_per_stream': int}
        Whether a maximum per user per stream is enabled and what the maximum is.
    background_color: str
        Custom background color for the reward (Hex with # prefix).
    image: Optional[{'url_1x': str, 'url_2x': str, 'url_4x': str}]
        Set of custom images for the reward. Can be null if no images uploaded.
    default_image: {'url_1x': str, 'url_2x': str, 'url_4x': str}
        Set of default images for the reward.
    global_cooldown: {'is_enabled': bool, 'global_cooldown_seconds': int}
        Whether a cooldown is enabled and what the cooldown is in seconds.
    cooldown_expires_at: str
        Timestamp of the cooldown expiration. null if the reward isn't on cooldown.
    redemptions_redeemed_current_stream: Optional[int]
        The number of redemptions redeemed during the current live stream.
    """
    id: str
    broadcaster_user_id: str
    broadcaster_user_login: str
    broadcaster_user_name: str
    is_enabled: bool
    is_paused: bool
    is_in_stock: bool
    title: str
    cost: int
    prompt: str
    is_user_input_required: bool
    should_redemptions_skip_request_queue: bool
    max_per_stream: MaxPerStream
    max_per_user_per_stream: MaxPerUserPerStream
    background_color: str
    image: Optional[Image]
    default_image: Image
    global_cooldown: GlobalCooldown
    cooldown_expires_at: Optional[str]
    redemptions_redeemed_current_stream: Optional[int]


RewardInfo = TypedDict('RewardInfo', {'id': str, 'title': str, 'prompt': str, 'cost': int})

class RewardRedemptionEvent(TypedDict):
    """
    Twitch EventSub payload for custom channel point reward redemptions.

    Attributes
    ----------
    id: str
        The redemption identifier.
    broadcaster_user_id: str
        The requested broadcaster ID.
    broadcaster_user_login: str
        The requested broadcaster login.
    broadcaster_user_name: str
        The requested broadcaster display name.
    user_id: str
        User ID of the user that redeemed the reward.
    user_login: str
        Login of the user that redeemed the reward.
    user_name: str
        Display name of the user that redeemed the reward.
    user_input: str
        The user input provided. Empty string if not provided.
    status: Literal['unknown', 'unfulfilled', 'fulfilled', 'canceled']
        Redemption status. Possible values: unknown, unfulfilled, fulfilled, canceled.
    reward: RewardInfo
        Basic information about the reward that was redeemed, with structure:
        {
            'id': str,
            'title': str,
            'prompt': str,
            'cost': int
        }
    redeemed_at: str
        RFC3339 timestamp of when the reward was redeemed.
    """
    id: str
    broadcaster_user_id: str
    broadcaster_user_login: str
    broadcaster_user_name: str
    user_id: str
    user_login: str
    user_name: str
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
    is_golden_kappa_train: bool
        Indicates if the Hype Train is a Golden Kappa Train.
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
    is_golden_kappa_train: bool
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
    is_golden_kappa_train: bool
        Indicates if the Hype Train is a Golden Kappa Train.
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
    is_golden_kappa_train: bool
    started_at: str
    ended_at: str
    cooldown_ends_at: str
