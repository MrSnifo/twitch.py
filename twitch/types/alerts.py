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

from .user import (Broadcaster, SpecificBroadcaster, FromSpecificBroadcaster, ToSpecificBroadcaster,
                   SpecificUser, SpecificAnonymousUser,
                   SpecificModerator)
from typing import Literal, Optional, TypedDict, List
from .chat import SubscriptionMessage


# ------------------------------
#        + Subscription +
# ------------------------------
SubscriptionTier = Literal['1000', '2000', '3000']


class SubscribeEvent(SpecificBroadcaster, SpecificUser):
    tier: SubscriptionTier
    is_gift: bool


class ReSubscribeEvent(SpecificBroadcaster, SpecificUser):
    tier: SubscriptionTier
    message: SubscriptionMessage
    streak_months: Optional[int]
    duration_months: int
    cumulative_months: int


class GiftSubsEvent(SpecificBroadcaster, SpecificAnonymousUser):
    tier: SubscriptionTier
    total: int
    is_anonymous: bool
    cumulative_total: Optional[str]


# -----------------------------
#           + Cheer +
# -----------------------------
class CheerEvent(SpecificBroadcaster, SpecificAnonymousUser):
    bits: int
    message: str
    is_anonymous: bool


# -----------------------------
#       + Channel Raid +
# -----------------------------
class RaidEvent(FromSpecificBroadcaster, ToSpecificBroadcaster):
    viewers: int


# -----------------------------
#    + Channel Moderators +
# -----------------------------
class ModeratorPrivilegesEvent(SpecificBroadcaster, SpecificUser):
    pass


# -------------------------
#      + Channel Goal +
# -------------------------
class BaseGoal(TypedDict):
    id: int
    type: str
    description: str
    target_amount: int
    current_amount: int


class Goal(BaseGoal, Broadcaster):
    created_at: str


# -------------+ EventSub +-------------
class GoalBeginProgressEvent(BaseGoal, SpecificBroadcaster):
    started_at: str


class GoalEndEvent(BaseGoal, SpecificBroadcaster):
    ended_at: str
    started_at: str
    is_achieved: bool


# ---------------------------
#    + Channel HypeTrain +
# ---------------------------
class HypeTrainContributor(TypedDict):
    type: Literal['bits', 'subscription', 'other']
    user: str
    total: int


class BaseHypeTrain(TypedDict):
    id: str
    total: int
    level: int
    started_at: str


class HypeTrain(BaseHypeTrain):
    goal: str
    expires_at: str
    broadcaster_id: str
    cooldown_end_time: str
    last_contribution: HypeTrainContributor
    top_contributions: List[HypeTrainContributor]


# -------------+ EventSub +-------------
class HypeTrainContributorEvent(SpecificUser):
    type: Literal['bits', 'subscription', 'other']
    total: int


class HypeTrainBeginProgressEvent(BaseHypeTrain):
    goal: int
    progress: int
    expires_at: str
    last_contribution: HypeTrainContributorEvent
    top_contributions: List[HypeTrainContributorEvent]


class HypeTrainEndEvent(BaseHypeTrain):
    ended_at: str
    cooldown_ends_at: str
    top_contributions: List[HypeTrainContributorEvent]


# --------------------------
#        + shoutout +
# --------------------------
class ShoutoutCreateEvent(SpecificBroadcaster, SpecificModerator, ToSpecificBroadcaster):
    started_at: str
    viewer_count: int
    cooldown_ends_at: str
    target_cooldown_ends_at: str


class ShoutoutReceiveEvent(SpecificBroadcaster, FromSpecificBroadcaster):
    viewer_count: int
    started_at: str
