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

from .users import Broadcaster, SpecificUser
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from typing import List, Literal, Optional


class Entitlement(TypedDict):
    """
    Represents an entitlement for a user.

    Attributes
    ----------
    id: str
        The unique identifier of the entitlement.
    benefit_id: str
        The ID of the benefit associated with the entitlement.
    timestamp: str
        The timestamp when the entitlement was created.
    user_id: str
        The ID of the user who owns the entitlement.
    game_id: str
        The ID of the game associated with the entitlement.
    fulfillment_status: Literal['CLAIMED', 'FULFILLED']
        The status of the entitlement, indicating whether it has been claimed or fulfilled.
    last_updated: str
        The timestamp when the entitlement was last updated.
    """
    id: str
    benefit_id: str
    timestamp: str
    user_id: str
    game_id: str
    fulfillment_status: Literal['CLAIMED', 'FULFILLED']
    last_updated: str


class EntitlementsUpdate(TypedDict):
    """
    Represents an update to multiple entitlements.

    Attributes
    ----------
    status: str
        The status of the entitlement update process.
    ids: List[str]
        A list of entitlement IDs that have been updated.
    """
    status: str
    ids: List[str]


class CharityAmount(TypedDict):
    """
    Represents an amount in a charity context.

    Attributes
    ----------
    value: int
        The value of the amount.
    decimal_places: int
        The number of decimal places in the value.
    currency: str
        The currency of the amount, e.g., 'USD', 'EUR'.
    """
    value: int
    decimal_places: int
    currency: str


class Charity(Broadcaster):
    """
    Represents a charity campaign.

    Attributes
    ----------
    id: str
        The unique identifier of the charity campaign.
    charity_logo: str
        The URL to the logo of the charity.
    charity_name: str
        The name of the charity.
    target_amount: Optional[CharityAmount]
        The target amount for the charity campaign.
    current_amount: CharityAmount
        The current amount raised by the charity campaign.
    charity_website: str
        The website URL of the charity.
    charity_description: str
        A description of the charity.
    """
    id: str
    charity_logo: str
    charity_name: str
    target_amount: Optional[CharityAmount]
    current_amount: CharityAmount
    charity_website: str
    charity_description: str


class CharityDonation(SpecificUser):
    """
    Represents a donation to a charity campaign.

    Attributes
    ----------
    id: str
        The unique identifier of the donation.
    amount: CharityAmount
        The amount donated.
    campaign_id: str
        The ID of the charity campaign to which the donation was made.
    """
    id: str
    amount: CharityAmount
    campaign_id: str


class Goal(Broadcaster):
    """
    Represents a goal in a Twitch context.

    Attributes
    ----------
    id: int
        The unique identifier of the goal.
    type: str
        The type of the goal, e.g., 'follower', 'subscriber'.
    description: str
        A brief description of the goal.
    target_amount: int
        The target amount to achieve the goal.
    current_amount: int
        The current progress towards the goal.
    created_at: str
        The timestamp when the goal was created.
    """
    id: int
    type: str
    description: str
    target_amount: int
    current_amount: int
    created_at: str
