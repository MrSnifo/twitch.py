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

from .users import SpecificBroadcaster, SpecificUser
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from typing import Literal, Optional, List, Dict, Any


# Message
class ChatClearEvent(SpecificBroadcaster):
    """
    Represents an event where the chat is cleared.

    Attributes
    ----------
    (Inherits from SpecificBroadcaster)
    """
    pass


class ClearUserMessagesEvent(SpecificBroadcaster):
    """
    Represents an event where a user's messages are cleared.

    Attributes
    ----------
    target_user_id: str
        The ID of the target user whose messages are cleared.
    target_user_name: str
        The name of the target user whose messages are cleared.
    target_user_login: str
        The login name of the target user whose messages are cleared.
    """
    target_user_id: str
    target_user_name: str
    target_user_login: str


class Cheermote(TypedDict):
    """
    Represents a cheermote used in the chat.

    Attributes
    ----------
    prefix: str
        The prefix for the cheermote.
    bits: int
        The number of bits required to use the cheermote.
    tier: int
        The tier of the cheermote.
    """
    prefix: str
    bits: int
    tier: int


class Emote(TypedDict):
    """
    Represents an emote in the chat.

    Attributes
    ----------
    id: str
        The ID of the emote.
    emote_set_id: str
        The ID of the emote set to which this emote belongs.
    owner_id: str
        The ID of the owner of the emote.
    format: List[Literal['animated', 'static']]
        The formats in which the emote is available.
    """
    id: str
    emote_set_id: str
    owner_id: str
    format: List[Literal['animated', 'static']]


class Fragment(TypedDict):
    """
    Represents a fragment of a chat message.

    Attributes
    ----------
    type: Literal['text', 'cheermote', 'emote', 'mention']
        The type of the fragment.
    text: str
        The text content of the fragment.
    cheermote: Optional[Cheermote]
        The cheermote associated with the fragment, if applicable.
    emote: Optional[Emote]
        The emote associated with the fragment, if applicable.
    mention: Optional[SpecificUser]
        The user mentioned in the fragment, if applicable.
    """
    type: Literal['text', 'cheermote', 'emote', 'mention']
    text: str
    cheermote: Optional[Cheermote]
    emote: Optional[Emote]
    mention: Optional[SpecificUser]


class TextEmoteMessage(TypedDict):
    """
    Represents a chat message containing text and emotes.

    Attributes
    ----------
    text: str
        The text of the message.
    emotes: List[str]
        A list of emote IDs present in the message.
    """
    text: str
    emotes: List[str]


class Message(TypedDict):
    """
    Represents a chat message.

    Attributes
    ----------
    text: str
        The text content of the message.
    fragments: List[Fragment]
        A list of fragments that make up the message.
    """
    text: str
    fragments: List[Fragment]


class Badge(TypedDict):
    """
    Represents a badge displayed next to a user's name.

    Attributes
    ----------
    set_id: str
        The ID of the badge set to which this badge belongs.
    id: str
        The ID of the badge.
    info: str
        Additional information about the badge.
    """
    set_id: str
    id: str
    info: str


class Cheer(TypedDict):
    """
    Represents a cheer in the chat.

    Attributes
    ----------
    bits: int
        The number of bits used in the cheer.
    """
    bits: int


class Reply(TypedDict):
    """
    Represents a reply to a chat message.

    Attributes
    ----------
    parent_message_id: str
        The ID of the parent message being replied to.
    parent_message_body: str
        The body of the parent message.
    parent_user_id: str
        The ID of the user who sent the parent message.
    parent_user_name: str
        The name of the user who sent the parent message.
    parent_user_login: str
        The login name of the user who sent the parent message.
    thread_message_id: str
        The ID of the thread message in which the reply was made.
    thread_user_id: str
        The ID of the user who sent the thread message.
    thread_user_name: str
        The name of the user who sent the thread message.
    thread_user_login: str
        The login name of the user who sent the thread message.
    """
    parent_message_id: str
    parent_message_body: str
    parent_user_id: str
    parent_user_name: str
    parent_user_login: str
    thread_message_id: str
    thread_user_id: str
    thread_user_name: str
    thread_user_login: str


class MessageEvent(SpecificBroadcaster):
    """
    Represents a chat message event.

    Attributes
    ----------
    chatter_user_id: str
        The ID of the user who sent the message.
    chatter_user_name: str
        The name of the user who sent the message.
    chatter_user_login: str
        The login name of the user who sent the message.
    message_id: str
        The ID of the message.
    message: Message
        The message content.
    message_type: Literal[
        'text',
        'channel_points_highlighted',
        'channel_points_sub_only',
        'user_intro',
        'power_ups_message_effect',
        'power_ups_gigantified_emote'
    ]
        The type of the message.
    badges: List[Badge]
        A list of badges associated with the user.
    cheer: Optional[Cheer]
        Details of the cheer, if applicable.
    color: Optional[str]
        The color of the user's chat message.
    reply: Optional[Reply]
        Details of the reply to the message, if applicable.
    channel_points_custom_reward_id: Optional[str]
        The ID of the custom reward associated with the message, if applicable.
    channel_points_animation_id: Optional[str]
        The ID of the animation associated with the channel points reward, if applicable.
    """
    chatter_user_id: str
    chatter_user_name: str
    chatter_user_login: str
    message_id: str
    message: Message
    message_type: Literal[
        'text',
        'channel_points_highlighted',
        'channel_points_sub_only',
        'user_intro',
        'power_ups_message_effect',
        'power_ups_gigantified_emote'
    ]
    badges: List[Badge]
    cheer: Optional[Cheer]
    color: Optional[str]
    reply: Optional[Reply]
    channel_points_custom_reward_id: Optional[str]
    channel_points_animation_id: Optional[str]


class MessageDeleteEvent(SpecificBroadcaster):
    """
    Represents an event where a chat message is deleted.

    Attributes
    ----------
    target_user_id: str
        The ID of the user whose message was deleted.
    target_user_name: str
        The name of the user whose message was deleted.
    target_user_login: str
        The login name of the user whose message was deleted.
    message_id: str
        The ID of the deleted message.
    """
    target_user_id: str
    target_user_name: str
    target_user_login: str
    message_id: str


class Sub(TypedDict):
    """
    Represents a subscription.

    Attributes
    ----------
    sub_tier: str
        The tier of the subscription.
    is_prime: bool
        Whether the subscription is a Prime subscription.
    duration_months: int
        The duration of the subscription in months.
    """
    sub_tier: str
    is_prime: bool
    duration_months: int


# Notification
class Resub(TypedDict):
    """
    Represents a resubscription.

    Attributes
    ----------
    cumulative_months: int
        The total number of months the user has subscribed.
    duration_months: int
        The duration of the resubscription in months.
    streak_months: int
        The number of months in the current streak.
    sub_tier: str
        The tier of the resubscription.
    is_prime: Optional[bool]
        Whether the resubscription is a Prime subscription, if applicable.
    is_gift: bool
        Whether the resubscription is a gift.
    gifter_is_anonymous: Optional[bool]
        Whether the gifter is anonymous, if applicable.
    gifter_user_id: Optional[str]
        The ID of the user who gifted the subscription, if applicable.
    gifter_user_name: Optional[str]
        The name of the user who gifted the subscription, if applicable.
    gifter_user_login: Optional[str]
        The login name of the user who gifted the subscription, if applicable.
    """
    cumulative_months: int
    duration_months: int
    streak_months: int
    sub_tier: str
    is_prime: Optional[bool]
    is_gift: bool
    gifter_is_anonymous: Optional[bool]
    gifter_user_id: Optional[str]
    gifter_user_name: Optional[str]
    gifter_user_login: Optional[str]


class SubGift(TypedDict):
    """
    Represents a subscription gift.

    Attributes
    ----------
    duration_months: int
        The duration of the gift subscription in months.
    cumulative_total: Optional[int]
        The total number of gifted subscriptions, if applicable.
    recipient_user_id: str
        The ID of the recipient of the gift subscription.
    recipient_user_name: str
        The name of the recipient of the gift subscription.
    recipient_user_login: str
        The login name of the recipient of the gift subscription.
    sub_tier: str
        The tier of the gift subscription.
    community_gift_id: Optional[str]
        The ID of the community gift, if applicable.
    """
    duration_months: int
    cumulative_total: Optional[int]
    recipient_user_id: str
    recipient_user_name: str
    recipient_user_login: str
    sub_tier: str
    community_gift_id: Optional[str]


class CommunitySubGift(TypedDict):
    """
    Represents a community subscription gift.

    Attributes
    ----------
    id: str
        The ID of the community gift.
    total: int
        The total number of subscriptions gifted to the community.
    sub_tier: str
        The tier of the gift subscriptions.
    cumulative_total: Optional[int]
        The cumulative total number of gifted subscriptions, if applicable.
    """
    id: str
    total: int
    sub_tier: str
    cumulative_total: Optional[int]


class GiftPaidUpgrade(TypedDict):
    """
    Represents a paid upgrade for a gifted subscription.

    Attributes
    ----------
    gifter_is_anonymous: bool
        Whether the gifter is anonymous.
    gifter_user_id: Optional[str]
        The ID of the user who gifted the upgrade, if applicable.
    gifter_user_name: Optional[str]
        The name of the user who gifted the upgrade, if applicable.
    gifter_user_login: Optional[str]
        The login name of the user who gifted the upgrade, if applicable.
    """
    gifter_is_anonymous: bool
    gifter_user_id: Optional[str]
    gifter_user_name: Optional[str]
    gifter_user_login: Optional[str]


class PrimePaidUpgrade(TypedDict):
    """
    Represents a paid upgrade for a Prime subscription.

    Attributes
    ----------
    sub_tier: str
        The tier of the upgraded Prime subscription.
    """
    sub_tier: str


class Raid(TypedDict):
    """
    Represents a raid event.

    Attributes
    ----------
    user_id: str
        The ID of the user who initiated the raid.
    user_name: str
        The name of the user who initiated the raid.
    user_login: str
        The login name of the user who initiated the raid.
    viewer_count: int
        The number of viewers participating in the raid.
    profile_image_url: str
        The URL of the user's profile image.
    """
    user_id: str
    user_name: str
    user_login: str
    viewer_count: int
    profile_image_url: str


class PayItForward(TypedDict):
    """
    Represents a Pay It Forward event.

    Attributes
    ----------
    gifter_is_anonymous: bool
        Whether the gifter is anonymous.
    gifter_user_id: Optional[str]
        The ID of the user who initiated the Pay It Forward, if applicable.
    gifter_user_name: Optional[str]
        The name of the user who initiated the Pay It Forward, if applicable.
    gifter_user_login: Optional[str]
        The login name of the user who initiated the Pay It Forward, if applicable.
    """
    gifter_is_anonymous: bool
    gifter_user_id: Optional[str]
    gifter_user_name: Optional[str]
    gifter_user_login: Optional[str]


class Announcement(TypedDict):
    """
    Represents an announcement event.

    Attributes
    ----------
    color: str
        The color of the announcement.
    """
    color: str


class CharityDonationAmount(TypedDict):
    """
    Represents the amount donated to charity.

    Attributes
    ----------
    value: int
        The donation amount.
    decimal_place: int
        The number of decimal places in the donation amount.
    currency: str
        The currency of the donation.
    """
    value: int
    decimal_place: int
    currency: str


class CharityDonation(TypedDict):
    """
    Represents a charity donation event.

    Attributes
    ----------
    charity_name: str
        The name of the charity receiving the donation.
    amount: CharityDonationAmount
        The amount of the donation.
    """
    charity_name: str
    amount: CharityDonationAmount


class BitsBadgeTier(TypedDict):
    """
    Represents a bits badge tier.

    Attributes
    ----------
    tier: int
        The tier of the bits badge.
    """
    tier: int


class NotificationEvent(TypedDict):
    """
    Represents a notification event.

    Attributes
    ----------
    broadcaster_user_id: str
        The ID of the broadcaster associated with the notification.
    broadcaster_user_name: str
        The name of the broadcaster associated with the notification.
    broadcaster_user_login: str
        The login name of the broadcaster associated with the notification.
    chatter_user_id: str
        The ID of the chatter associated with the notification.
    chatter_user_name: str
        The name of the chatter associated with the notification.
    chatter_user_login: str
        The login name of the chatter associated with the notification.
    chatter_is_anonymous: bool
        Whether the chatter is anonymous.
    color: str
        The color of the notification.
    badges: List[Badge]
        A list of badges associated with the chatter.
    system_message: str
        The system message of the notification.
    message_id: str
        The ID of the message associated with the notification.
    message: Message
        The message content.
    notice_type: str
        The type of notification.
    sub: Optional[Sub]
        Details of the subscription, if applicable.
    resub: Optional[Resub]
        Details of the resubscription, if applicable.
    sub_gift: Optional[SubGift]
        Details of the subscription gift, if applicable.
    community_sub_gift: Optional[CommunitySubGift]
        Details of the community subscription gift, if applicable.
    gift_paid_upgrade: Optional[GiftPaidUpgrade]
        Details of the paid upgrade for a gifted subscription, if applicable.
    prime_paid_upgrade: Optional[PrimePaidUpgrade]
        Details of the paid upgrade for a Prime subscription, if applicable.
    raid: Optional[Raid]
        Details of the raid event, if applicable.
    unraid: Optional[Dict[Any, Any]]
        Details of the unraid event, if applicable.
    pay_it_forward: Optional[PayItForward]
        Details of the Pay It Forward event, if applicable.
    announcement: Optional[Announcement]
        Details of the announcement, if applicable.
    charity_donation: Optional[CharityDonation]
        Details of the charity donation, if applicable.
    bits_badge_tier: Optional[BitsBadgeTier]
        Details of the bits badge tier, if applicable.
    """
    broadcaster_user_id: str
    broadcaster_user_name: str
    broadcaster_user_login: str
    chatter_user_id: str
    chatter_user_name: str
    chatter_user_login: str
    chatter_is_anonymous: bool
    color: str
    badges: List[Badge]
    system_message: str
    message_id: str
    message: Message
    notice_type: str
    sub: Optional[Sub]
    resub: Optional[Resub]
    sub_gift: Optional[SubGift]
    community_sub_gift: Optional[CommunitySubGift]
    gift_paid_upgrade: Optional[GiftPaidUpgrade]
    prime_paid_upgrade: Optional[PrimePaidUpgrade]
    raid: Optional[Raid]
    unraid: Optional[Dict[Any, Any]]
    pay_it_forward: Optional[PayItForward]
    announcement: Optional[Announcement]
    charity_donation: Optional[CharityDonation]
    bits_badge_tier: Optional[BitsBadgeTier]


# Settings
class SettingsUpdateEvent(SpecificBroadcaster):
    """
    Represents an event where chat settings are updated.

    Attributes
    ----------
    emote_mode: bool
        Whether emote mode is enabled.
    follower_mode: bool
        Whether follower mode is enabled.
    follower_mode_duration_minutes: Optional[int]
        The duration of follower mode in minutes, if applicable.
    slow_mode: bool
        Whether slow mode is enabled.
    slow_mode_wait_time_seconds: Optional[int]
        The wait time for slow mode in seconds, if applicable.
    subscriber_mode: bool
        Whether subscriber mode is enabled.
    unique_chat_mode: bool
        Whether unique chat mode is enabled.
    """
    emote_mode: bool
    follower_mode: bool
    follower_mode_duration_minutes: Optional[int]
    slow_mode: bool
    slow_mode_wait_time_seconds: Optional[int]
    subscriber_mode: bool
    unique_chat_mode: bool