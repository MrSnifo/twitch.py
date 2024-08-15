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

from typing import TypedDict


class DataRange(TypedDict):
    """
    Represents a time range with start and end dates.

    Attributes
    ----------
    started_at: str
        The start date of the range in ISO 8601 format.
    ended_at: str
        The end date of the range in ISO 8601 format.
    """
    started_at: str
    ended_at: str


class Extension(TypedDict):
    """
    Represents an extension with its details.

    Attributes
    ----------
    extension_id: str
        The unique identifier for the extension.
    URL: str
        The URL where the extension is hosted.
    type: str
        The type of the extension.
    date_range: DataRange
        The date range during which the extension data is relevant.
    """
    extension_id: str
    URL: str
    type: str
    date_range: DataRange


class Game(TypedDict):
    """
    Represents a game with its details.

    Attributes
    ----------
    game_id: str
        The unique identifier for the game.
    URL: str
        The URL where the game is hosted or related to.
    type: str
        The type of the game.
    date_range: DataRange
        The date range during which the game data is relevant.
    """
    game_id: str
    URL: str
    type: str
    date_range: DataRange
