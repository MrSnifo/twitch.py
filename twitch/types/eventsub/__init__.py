"""
twitch.types.eventsub

Typing for Twitch.

:copyright: (c) 2024-present Snifo
:license: MIT, see LICENSE for more details.
"""

from __future__ import annotations

from . import activity, bits, channels, chat, interaction, moderation, streams, users
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from typing import TypeVar, Dict, Any
    T = TypeVar('T')


class Subscription(TypedDict):
    id: str
    type: str
    version: str
    status: str
    cost: int
    condition: Dict[str, Any]
    created_at: str


class Data(TypedDict):
    subscription: Subscription
    event: T
