"""
twitch.types

Typing for Twitch.

:copyright: (c) 2024-present Snifo
:license: MIT, see LICENSE for more details.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from typing import TypeVar
    T = TypeVar('T')


# Most of the data in the Helix API is wrapped with the 'data' keyword.
class Data(TypedDict):
    data: T


pagination = TypedDict('pagination', {'cursor': str})


class PData(Data):
    pagination: pagination


date_range = TypedDict('date_range', {'started_at': str, 'ended_at': str})


class TData(PData):
    total: int


# EventSub Subscription
class TTMData(TData):
    total_cost: int
    max_total_cost: int


# Subscription
class TPData(PData):
    points: int
    total: int


# Chat Emote
class Edata(Data):
    template: str


class PEdata(PData):
    template: str


class DTData(Data):
    date_range: date_range
    total: int
