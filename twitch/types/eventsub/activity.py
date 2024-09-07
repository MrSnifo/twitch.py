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

from .users import SpecificBroadcaster, Broadcaster, SpecificUser
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from typing import Literal


class DonationAmount(TypedDict):
    """
    Represents the amount of a donation.

    Attributes
    ----------
    value: int
        The value of the donation.
    decimal_places: int
        The number of decimal places in the donation value.
    currency: str
        The currency code (e.g., USD) of the donation.
    """
    value: int
    decimal_places: int
    currency: str


class CharityDonationEvent(SpecificBroadcaster, SpecificUser):
    """
    Represents an event where a donation is made to a charity during a Twitch stream.

    Attributes
    ----------
    id: str
        The unique identifier for the charity donation event.
    campaign_id: str
        The unique identifier for the charity campaign.
    charity_name: str
        The name of the charity.
    charity_description: str
        A description of the charity.
    charity_logo: str
        The URL of the charity's logo.
    charity_website: str
        The URL of the charity's website.
    amount: DonationAmount
        The amount donated to the charity.
    """
    id: str
    campaign_id: str
    charity_name: str
    charity_description: str
    charity_logo: str
    charity_website: str
    amount: DonationAmount


class CharityCampaignStartEvent(Broadcaster):
    """
    Represents the start of a charity campaign during a Twitch stream.

    Attributes
    ----------
    id: str
        The unique identifier for the charity campaign.
    charity_name: str
        The name of the charity.
    charity_description: str
        A description of the charity.
    charity_logo: str
        The URL of the charity's logo.
    charity_website: str
        The URL of the charity's website.
    current_amount: DonationAmount
        The current amount raised during the campaign.
    target_amount: DonationAmount
        The target amount to be raised during the campaign.
    started_at: str
        The timestamp when the charity campaign started.
    """
    id: str
    charity_name: str
    charity_description: str
    charity_logo: str
    charity_website: str
    current_amount: DonationAmount
    target_amount: DonationAmount
    started_at: str


class CharityCampaignProgressEvent(Broadcaster):
    """
    Represents the progress of an ongoing charity campaign during a Twitch stream.

    Attributes
    ----------
    id: str
        The unique identifier for the charity campaign.
    charity_name: str
        The name of the charity.
    charity_description: str
        A description of the charity.
    charity_logo: str
        The URL of the charity's logo.
    charity_website: str
        The URL of the charity's website.
    current_amount: DonationAmount
        The current amount raised during the campaign.
    target_amount: DonationAmount
        The target amount to be raised during the campaign.
    """
    id: str
    charity_name: str
    charity_description: str
    charity_logo: str
    charity_website: str
    current_amount: DonationAmount
    target_amount: DonationAmount


class CharityCampaignStopEvent(Broadcaster):
    """
    Represents the end of a charity campaign during a Twitch stream.

    Attributes
    ----------
    id: str
        The unique identifier for the charity campaign.
    charity_name: str
        The name of the charity.
    charity_description: str
        A description of the charity.
    charity_logo: str
        The URL of the charity's logo.
    charity_website: str
        The URL of the charity's website.
    current_amount: DonationAmount
        The current amount raised during the campaign.
    target_amount: DonationAmount
        The target amount to be raised during the campaign.
    stopped_at: str
        The timestamp when the charity campaign ended.
    """
    id: str
    charity_name: str
    charity_description: str
    charity_logo: str
    charity_website: str
    current_amount: DonationAmount
    target_amount: DonationAmount
    stopped_at: str


class GoalsEvent(SpecificBroadcaster):
    """
    Represents a goal event during a Twitch stream.

    Attributes
    ----------
    id: str
        The unique identifier for the goal event.
    type: str
        The type of goal being tracked. Possible values include:

        - follow
        - subscription
        - subscription_count
        - new_subscription
        - new_subscription_count
        - new_bit
        - new_cheerer
    description: str
        A description of the goal event.
    is_achieved: bool
        Indicates whether the goal has been achieved.
    current_amount: int
        The current progress towards the goal.
    target_amount: int
        The target amount to achieve the goal.
    started_at: str
        The timestamp when the goal event started.
    ended_at: str
        The timestamp when the goal event ended, if applicable.
    """
    id: str
    type: Literal[
        'follow',
        'subscription',
        'subscription_count',
        'new_subscription',
        'new_subscription_count',
        'new_bit',
        'new_cheerer'
    ]
    description: str
    is_achieved: bool
    current_amount: int
    target_amount: int
    started_at: str
    ended_at: str
