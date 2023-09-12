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

from .user import SpecificBroadcaster, SpecificUser
from typing import TypedDict, Literal, List


# -----------------------------------
#            + Category +
# -----------------------------------
class Category(TypedDict):
    id: str
    name: str


class SpecificCategory(TypedDict):
    category_id: str
    category_name: str


class SpecificGame(TypedDict):
    game_id: str
    game_name: str


class GetGame(Category):
    igdb_id: str


# ----------------------------------
#            + Stream +
# ----------------------------------
class Online(SpecificBroadcaster):
    id: str
    type: Literal['live', 'playlist', 'watch_party', 'premiere', 'rerun']
    started_at: str


class Stream(SpecificUser, SpecificGame):
    id: str
    tags: List[str]
    type: Literal['live', '']
    title: str
    language: str
    is_mature: bool
    started_at: str
    viewer_count: int
    thumbnail_url: str


class StreamMarker(TypedDict):
    id: str
    url: str  # May sometimes be unavailable.
    created_at: str
    description: str
    position_seconds: int


class StartCommercial(TypedDict):
    length: int
    message: str
    retry_after: int


class CreateClip(TypedDict):
    id: str
    edit_url: str


class StartRaid(TypedDict):
    is_mature: bool
    created_at: str
