"""
twitch.types.eventsub

Typing for Twitch.

:copyright: (c) 2024-present Snifo
:license: MIT, see LICENSE for more details.
"""

from typing import TypedDict, TypeVar, Dict
from . import activity, bits, channels, chat, interaction, moderation, streams, users


T = TypeVar('T')


class Subscription(TypedDict):
    id: str
    type: str
    version: str
    status: str
    cost: int
    condition: Dict[str, str]  # This will be specific to each type of subscription
    created_at: str


class Data(TypedDict):
    subscription: Subscription
    event: T
