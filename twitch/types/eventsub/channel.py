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

from ..user import (SpecificBroadcaster, SpecificUser, SpecificAnonymous,
                    ToSpecificBroadcaster, FromSpecificBroadcaster)
from ..message import Message
from typing import Optional


class Update(SpecificBroadcaster):
    """
    Type: Channel Update
    Name: `channel.update`
    Version: 1
    """
    title: str
    language: str
    category_id: str
    category_name: str
    is_mature: bool


class Follow(SpecificBroadcaster, SpecificUser):
    """
    Type: Channel Follow
    Name: `channel.follow`
    Version: 2
    """
    followed_at: str


class Subscribe(SpecificBroadcaster, SpecificUser):
    """
    Type: Channel Subscribe
    Name: `channel.subscribe`
    Version: 1
    """
    tier: str
    is_gift: bool


class SubscriptionEnd(Subscribe):
    """
    Type: Channel Subscription End
    Name: `channel.subscription.end`
    Version: 1
    """
    pass


class SubscriptionGift(SpecificBroadcaster, SpecificAnonymous):
    """
    Type: Channel Subscription Gift
    Name: `channel.subscription.gift`
    Version: 1
    """
    tier: str
    total: int
    cumulative_total: Optional[int]
    is_anonymous: bool


class SubscriptionMessage(SpecificBroadcaster, SpecificUser):
    """
    Type: Channel Subscription Message
    Name: `channel.subscription.message`
    Version: 1
    """
    tier: str
    message: Message
    cumulative_months: int
    streak_months: Optional[int]
    duration_months: int


class Cheer(SpecificBroadcaster, SpecificAnonymous):
    """
    Type: Channel Cheer
    Name: `channel.cheer`
    Version: 1
    """
    bits: int
    message: str
    is_anonymous: bool


class Raid(FromSpecificBroadcaster, ToSpecificBroadcaster):
    """
    Type: Channel Raid
    Name: `channel.raid`
    Version: 1
    """
    viewers: int
