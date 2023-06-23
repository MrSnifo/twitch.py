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

from ..user import SpecificBroadcaster, SpecificUser
from typing import TypedDict


class SpecificCharity(TypedDict):
    charity_name: str
    charity_description: str
    charity_logo: str
    charity_website: str


class Amount(TypedDict):
    value: int
    decimal_places: int
    currency: str


class _CharityBase(SpecificBroadcaster, SpecificCharity):
    id: str


class Donation(_CharityBase, SpecificUser):
    """
    Type: Charity Donation
    Name: `channel.charity_campaign.donate`
    Version: 1
    """
    amount: Amount


class Start(_CharityBase):
    """
    Type: Charity Campaign Start
    Name: `channel.charity_campaign.start`
    Version: 1
    """
    current_amount: Amount
    target_amount: Amount
    started_at: str


class Progress(_CharityBase):
    """
    Type: Charity Campaign Progress
    Name: `channel.charity_campaign.progress`
    Version: 1
    """
    current_amount: Amount
    target_amount: Amount


class Stop(_CharityBase):
    """
    Type: Charity Campaign Stop
    Name: `channel.charity_campaign.stop`
    Version: 1
    """
    current_amount: Amount
    target_amount: Amount
    stopped_at: str
