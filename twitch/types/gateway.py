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

from typing import Optional, TypedDict, Dict

__all__ = ('Session', 'Subscription')


class _Metadata(TypedDict):
    """
    Represents the metadata of a server.
    """
    _id: str
    _type: str
    _timestamp: str


class _SubscriptionMetadata(_Metadata):
    """
    Represents the metadata for a Notification.
    """
    subscription_type: str
    subscription_version: str


class Session(TypedDict):
    """
    Represents the connection information.
    """
    id: str
    status: str
    connected_at: str
    keepalive_timeout_seconds: Optional[int]
    reconnect_url: Optional[str]


class _Transport(TypedDict):
    """
    Represents the transport details.
    """
    method: str
    session_id: str


class Subscription(TypedDict):
    """
    Represents the subscription details.
    """
    id: str
    status: str
    type: str
    version: str
    cost: str
    condition: Dict[str, str]
    transport: _Transport
    created_at: str
