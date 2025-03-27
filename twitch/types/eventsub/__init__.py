""" 
twitch.types.eventsub  
Typing for Twitch.  
:copyright: (c) 2025-present Snifo 
:license: MIT, see LICENSE for more details. 
"""

from __future__ import annotations

from . import activity, bits, channels, chat, interaction, moderation, streams, users
from typing import TypedDict, TypeVar, Generic, Dict

T = TypeVar('T')

class Metadata(TypedDict):
    """
    Metadata for the event subscription payload.

    Attributes
    ----------
    message_id: str
        Unique identifier for the message.
    message_type: str
        Type of the message.
    message_timestamp: str
        Timestamp of the message when it was sent.
    subscription_type: str
        Type of the subscription.
    subscription_version: str
        Version of the subscription.
    """
    message_id: str
    message_type: str
    message_timestamp: str
    subscription_type: str
    subscription_version: str

class Transport(TypedDict):
    """
    Transport details for the event subscription.

    Attributes
    ----------
    method: str
        The method used for transport.
    session_id: str
        Session ID for the subscription transport.
    """
    method: str
    session_id: str

class Subscription(TypedDict):
    """
    Subscription details for the event subscription.

    Attributes
    ----------
    id: str
        Unique identifier for the subscription.
    status: str
        Status of the subscription.
    type: str
        Type of the subscription.
    version: str
        Version of the subscription.
    condition: Dict[str, str]
        Condition for triggering the subscription.
    transport: Transport
        Transport details for the subscription.
    created_at: str
        Timestamp when the subscription was created.
    cost: int
        Cost associated with the subscription.
    """
    id: str
    status: str
    type: str
    version: str
    condition: Dict[str, str]
    transport: Transport
    created_at: str
    cost: int

class Payload(TypedDict, Generic[T]):
    """
    Payload for the event subscription.

    Attributes
    ----------
    subscription: Subscription
        The subscription details.
    event: T
        Event associated with the subscription.
    """
    subscription: Subscription
    event: T

class MPData(TypedDict, Generic[T]):
    """
    MPData for the event subscription.

    Attributes
    ----------
    metadata: Metadata
        Metadata for the event subscription.
    payload: Payload[T]
        Payload for the event subscription.
    """
    metadata: Metadata
    payload: Payload[T]
