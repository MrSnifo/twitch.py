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

# Core
from .message import Message
from .user import User

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .types.eventsub import channel as chl
    from typing import Optional


class Category:
    """
    Represents a category for a channel.
    """
    __slots__ = ('id', 'name')

    def __init__(self, channel: chl.Update) -> None:
        self.id: Optional[str] = channel['category_id']
        self.name: Optional[str] = channel['category_name']


class Channel:
    """
    Represents a channel.
    """
    __slots__ = ('title', 'language', '_category', 'is_mature')

    def __init__(self, channel: chl.Update) -> None:
        self.title: str = channel['title']
        self.language: str = channel['language']
        self._category: Category = Category(channel=channel)
        self.is_mature: bool = channel['is_mature']

    def __repr__(self) -> str:
        return f'<Channel title={self.title} language={self.language}>'

    @property
    def category(self) -> Optional[Category]:
        """
        Retrieves the category of the channel.
        """
        if self._category.id:
            return self._category
        else:
            return None


class Subscription:
    """
    Represents a channel subscription.
    """
    __slots__ = ('user', 'tier', 'is_gift')

    def __init__(self, *, channel: chl.Subscribe | chl.SubscriptionEnd) -> None:
        self.user: User = User(user=channel)
        self.tier: str = channel['tier']
        self.is_gift: bool = channel['is_gift']

    def __repr__(self) -> str:
        return f'<Subscription {super().__repr__()} tier={self.tier} is_gift={self.is_gift}>'


class SubscriptionGift:
    """
    Represents a channel subscription gift.
    """
    __slots__ = ('user', 'tier', 'total', 'cumulative_total', 'is_anonymous')

    def __init__(self, channel: chl.SubscriptionGift) -> None:
        self.user: User = User(user=channel)
        self.tier: str = channel['tier']
        self.total: int = channel['total']
        self.cumulative_total: Optional[int] = channel['cumulative_total']
        self.is_anonymous: bool = channel['is_anonymous']

    def __repr__(self) -> str:
        return f'<SubscriptionGift tier={self.tier} total={self.total}>'


class SubscriptionMessage:
    """
    Represents a channel re-subscription.
    """
    __slots__ = ('user', 'tier', 'message', 'cumulative', 'duration', 'streak')

    def __init__(self, channel: chl.SubscriptionMessage) -> None:
        self.user: User = User(user=channel)
        self.tier: str = channel['tier']
        self.message: Message = Message(message=channel['message'])
        self.cumulative: int = channel['cumulative_months']
        self.duration: int = channel['duration_months']
        self.streak: Optional[int] = channel['streak_months']

    def __repr__(self) -> str:
        return f'<SubscriptionMessage tier={self.tier} duration={self.duration} message={self.message.__repr__()}>'


class Cheer:
    """
    Represents a channel cheer.
    """
    __slots__ = ('user', 'bits', 'message', 'is_anonymous')

    def __init__(self, channel: chl.Cheer) -> None:
        self.user: User = User(user=channel)
        self.bits: int = channel['bits']
        self.message: str = channel['message']
        self.is_anonymous: bool = channel['is_anonymous']

    def __repr__(self) -> str:
        return f'<Cheer bits={self.bits} message={self.message} user={self.user.__repr__()}>'


class Raid:
    """
    Represents a channel raid.
    """
    __slots__ = ('from_user', 'to_user', 'viewers')

    def __init__(self, raid: chl.Raid) -> None:
        self.from_user: User = User(user=raid, prefix='from_broadcaster_user')
        self.to_user: User = User(user=raid, prefix='to_broadcaster_user')
        self.viewers: int = raid['viewers']

    def __repr__(self) -> str:
        return f'<Raid from_user={self.from_user.__repr__()} to_user={self.to_user.__repr__()} viewers={self.viewers}>'
