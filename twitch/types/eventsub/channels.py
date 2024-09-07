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
from .chat import TextEmoteMessage
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List, Optional


# Update
class ChannelUpdateEvent(SpecificBroadcaster):
    """
    Represents an event where the broadcaster updates their channel information.

    Attributes
    ----------
    title: str
        The title of the stream.
    language: str
        The language of the stream.
    category_id: str
        The ID of the category.
    category_name: str
        The name of the category.
    content_classification_labels: List[str]
        A list of content classification labels associated with the stream.
    """
    title: str
    language: str
    category_id: str
    category_name: str
    content_classification_labels: List[str]


# Follow
class FollowEvent(SpecificBroadcaster, SpecificUser):
    """
    Represents an event where a user follows a broadcaster.

    Attributes
    ----------
    followed_at: str
        The timestamp when the follow occurred.
    """
    followed_at: str


# Subscription
class SubscribeEvent(SpecificBroadcaster, SpecificUser):
    """
    Represents an event where a user subscribes to a broadcaster's channel.

    Attributes
    ----------
    tier: str
        The tier of the subscription (e.g., Tier 1, Tier 2, Tier 3).
    is_gift: bool
        Indicates whether the subscription was gifted.
    """
    tier: str
    is_gift: bool


class SubscriptionEndEvent(SpecificBroadcaster, SpecificUser):
    """
    Represents an event where a user's subscription to a broadcaster's channel ends.

    Attributes
    ----------
    tier: str
        The tier of the subscription that ended.
    is_gift: bool
        Indicates whether the ended subscription was a gift.
    """
    tier: str
    is_gift: bool


class SubscriptionGiftEvent(SpecificBroadcaster):
    """
    Represents an event where a user gifts a subscription to another user.

    Attributes
    ----------
    user_id: Optional[str]
        The ID of the user who gifted the subscription, if available.
    user_login: Optional[str]
        The login name of the user who gifted the subscription, if available.
    user_name: Optional[str]
        The display name of the user who gifted the subscription, if available.
    total: int
        The total number of subscriptions gifted by the user.
    tier: str
        The tier of the gifted subscription (e.g., Tier 1, Tier 2, Tier 3).
    cumulative_total: Optional[int]
        The cumulative total number of subscriptions gifted by the user, if available.
    is_anonymous: bool
        Indicates whether the gift was given anonymously.
    """
    user_id: Optional[str]
    user_login: Optional[str]
    user_name: Optional[str]
    total: int
    tier: str
    cumulative_total: Optional[int]
    is_anonymous: bool


class SubscriptionMessageEvent(SpecificBroadcaster, SpecificUser):
    """
    Represents an event where a user sends a message during their subscription.

    Attributes
    ----------
    tier: str
        The tier of the subscription associated with the message.
    message: TextEmoteMessage
        The message content, which may include text and emotes.
    cumulative_months: int
        The total number of months the user has been subscribed.
    streak_months: Optional[int]
        The number of consecutive months the user has been subscribed, if available.
    duration_months: int
        The duration of the current subscription in months.
    """
    tier: str
    message: TextEmoteMessage
    cumulative_months: int
    streak_months: Optional[int]
    duration_months: int


# VIP Add/Remove
class VIPAddEvent(SpecificBroadcaster, SpecificUser):
    """
    Represents an event where a user is granted VIP status in a broadcaster's channel.
    """
    pass


class VIPRemoveEvent(SpecificBroadcaster, SpecificUser):
    """
    Represents an event where a user is removed from VIP status in a broadcaster's channel.
    """
    pass
