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

from typing import TypedDict, TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List


# Game Search
class Game(TypedDict):
    """
    Represents a game with its details.

    Attributes
    ----------
    id: str
        The unique identifier for the game.
    name: str
        The name of the game.
    box_art_url: str
        The URL of the game's box art.
    igdb_id: str
        The IGDB (Internet Game Database) identifier for the game.
    """
    id: str
    name: str
    box_art_url: str
    igdb_id: str


# Category Search
class CategorySearch(TypedDict):
    """
    Represents a category with its details.

    Attributes
    ----------
    box_art_url: str
        The URL of the category's box art.
    name: str
        The name of the category.
    id: str
        The unique identifier for the category.
    """
    box_art_url: str
    name: str
    id: str


# Channel Search
class ChannelSearch(TypedDict):
    """
    Represents a channel with its details.

    Attributes
    ----------
    broadcaster_language: str
        The language spoken by the broadcaster.
    broadcaster_login: str
        The login name of the broadcaster.
    display_name: str
        The display name of the channel.
    game_id: str
        The unique identifier of the game being played.
    game_name: str
        The name of the game being played.
    id: str
        The unique identifier for the channel.
    is_live: bool
        Indicates whether the channel is currently live.
    tags: List[str]
        A list of tags associated with the channel.
    thumbnail_url: str
        The URL of the channel's thumbnail.
    title: str
        The title of the channel's current broadcast.
    started_at: str
        The start time of the channel's current broadcast in ISO 8601 format.
    """
    broadcaster_language: str
    broadcaster_login: str
    display_name: str
    game_id: str
    game_name: str
    id: str
    is_live: bool
    tags: List[str]
    thumbnail_url: str
    title: str
    started_at: str
