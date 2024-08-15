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

from typing import TYPE_CHECKING, TypedDict
from .users import SpecificUser

if TYPE_CHECKING:
    from typing import List, Literal


# Leaderboard
class Leaderboard(SpecificUser):
    """
    Represents a leaderboard entry for a user.

    Attributes
    ----------
    rank: int
        The rank of the user in the leaderboard.
    score: int
        The score of the user in the leaderboard.
    """
    rank: int
    score: int


# Cheermote
CheermoteImages = TypedDict('CheermoteImages', {'1': str, '1.5': str, '2': str, '3': str, '4': str})


class ImagesType(TypedDict):
    """
    Represents different types of cheermote images.

    Attributes
    ----------
    animated: CheermoteImages
        A dictionary containing URLs of cheermote images for different bit amounts in animated form.
    static: CheermoteImages
        A dictionary containing URLs of cheermote images for different bit amounts in static form.

    The `CheermoteImages` dictionary contains keys for various bit amounts, including:
    - '1': URL for 1 bit
    - '1.5': URL for 1.5 bits
    - '2': URL for 2 bits
    - '3': URL for 3 bits
    - '4': URL for 4 bits
    """
    animated: CheermoteImages
    static: CheermoteImages


class TierImages(TypedDict):
    """
    Represents cheermote images categorized by theme mode.

    Attributes
    ----------
    dark: ImagesType
        A dictionary containing URLs of cheermote images categorized by type (animated or static) for dark mode.
    light: ImagesType
        A dictionary containing URLs of cheermote images categorized by type (animated or static) for light mode.
    """
    dark: ImagesType
    light: ImagesType


class CheermoteTier(TypedDict):
    """
    Represents a tier of cheermote with specific attributes.

    Attributes
    ----------
    id: str
        The unique identifier of the cheermote tier.
    min_bits: Literal[1, 100, 500, 1000, 5000, 10000, 100000]
        The minimum number of bits required to unlock this cheermote tier.
    color: str
        The color associated with the cheermote tier.
    images: TierImages
        A dictionary containing cheermote images categorized by theme mode and type.
    can_cheer: bool
        Whether the cheermote tier can be used for cheering.
    show_in_bits_card: bool
        Whether the cheermote tier is shown in the bits card.
    """
    id: str
    min_bits: Literal[1, 100, 500, 1000, 5000, 10000, 100000]
    color: str
    images: TierImages
    can_cheer: bool
    show_in_bits_card: bool


class Cheermote(TypedDict):
    """
    Represents a cheermote with its details and tiers.

    Attributes
    ----------
    prefix: str
        The prefix used to represent the cheermote.
    tiers: List[CheermoteTier]
        A list of cheermote tiers available.
    type: Literal['global_first_party', 'global_third_party', 'channel_custom', 'display_only', 'sponsored']
        The type of cheermote.
    order: int
        The order of the cheermote.
    last_updated: str
        The timestamp when the cheermote was last updated.
    is_charitable: bool
        Whether the cheermote is used for charitable purposes.
    """
    prefix: str
    tiers: List[CheermoteTier]
    type: Literal['global_first_party', 'global_third_party', 'channel_custom', 'display_only', 'sponsored']
    order: int
    last_updated: str
    is_charitable: bool
