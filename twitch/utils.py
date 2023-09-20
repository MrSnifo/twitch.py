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
from __future__ import annotations

from datetime import datetime, timezone, timedelta
from collections import Counter
import logging
import string
import random
import re

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, Any, List, Dict, Union
    from .types.chat import (Images as ImagesType, ChatMessage as ChatMessageType)
    from .types import http

__all__ = (
    'Subscriptions',
    'Scopes',
    'Value',
    'Images',
    'generate_random_text',
    'get_subscriptions',
    'MISSING', 'EXCLUSIVE',
    'convert_rfc3339',
    'convert_to_pst_rfc3339',
    'ircv3_to_json',
    'setup_logging',
)

# -------------------------------------------
#     Documentation Changelog last check
#     Date: 2023‑09‑12
# -------------------------------------------
Subscriptions: Dict[str, http.SubscriptionInfo] = {
    'user_update':
        {'name': 'user.update', 'version': '1', 'scope': None},
    'channel_update':
        {'name': 'channel.update', 'version': '2', 'scope': None},
    'follow':
        {'name': 'channel.follow', 'version': '2', 'scope': 'moderator:read:followers'},
    'subscribe':
        {'name': 'channel.subscribe', 'version': '1', 'scope': 'channel:read:subscriptions'},
    'subscription_end':
        {'name': 'channel.subscription.end', 'version': '1', 'scope': 'channel:read:subscriptions'},
    'subscription_gift':
        {'name': 'channel.subscription.gift', 'version': '1', 'scope': 'channel:read:subscriptions'},
    'resubscribe':
        {'name': 'channel.subscription.message', 'version': '1', 'scope': 'channel:read:subscriptions'},
    'cheer':
        {'name': 'channel.cheer', 'version': '1', 'scope': 'bits:read'},
    'raid':
        {'name': 'channel.raid', 'version': '1', 'scope': None},
    'ban':
        {'name': 'channel.ban', 'version': '1', 'scope': 'channel:moderate'},
    'unban':
        {'name': 'channel.unban', 'version': '1', 'scope': 'channel:moderate'},
    'moderator_add':
        {'name': 'channel.moderator.add', 'version': '1', 'scope': 'moderation:read'},
    'moderator_remove':
        {'name': 'channel.moderator.remove', 'version': '1', 'scope': 'moderation:read'},
    'points_reward_add':
        {'name': 'channel.channel_points_custom_reward.add', 'version': '1',
         'scope': 'channel:read:redemptions'},
    'points_reward_update':
        {'name': 'channel.channel_points_custom_reward.update', 'version': '1',
         'scope': 'channel:read:redemptions'},
    'points_reward_remove':
        {'name': 'channel.channel_points_custom_reward.remove', 'version': '1',
         'scope': 'channel:read:redemptions'},
    'points_reward_redemption':
        {'name': 'channel.channel_points_custom_reward_redemption.add', 'version': '1',
         'scope': 'channel:read:redemptions'},
    'points_reward_redemption_update':
        {'name': 'channel.channel_points_custom_reward_redemption.update', 'version': '1',
         'scope': 'channel:read:redemptions'},
    'poll_begin':
        {'name': 'channel.poll.begin', 'version': '1', 'scope': 'channel:read:polls'},
    'poll_progress':
        {'name': 'channel.poll.progress', 'version': '1', 'scope': 'channel:read:polls'},
    'poll_end':
        {'name': 'channel.poll.end', 'version': '1', 'scope': 'channel:read:polls'},
    'prediction_begin':
        {'name': 'channel.prediction.begin', 'version': '1', 'scope': 'channel:read:predictions'},
    'prediction_progress':
        {'name': 'channel.prediction.progress', 'version': '1', 'scope': 'channel:read:predictions'},
    'prediction_lock':
        {'name': 'channel.prediction.lock', 'version': '1', 'scope': 'channel:read:predictions'},
    'prediction_end':
        {'name': 'channel.prediction.end', 'version': '1', 'scope': 'channel:read:predictions'},
    'charity_campaign_donate':
        {'name': 'channel.charity_campaign.donate', 'version': '1', 'scope': 'channel:read:charity'},
    'charity_campaign_start':
        {'name': 'channel.charity_campaign.start', 'version': '1', 'scope': 'channel:read:charity'},
    'charity_campaign_progress':
        {'name': 'channel.charity_campaign.progress', 'version': '1', 'scope': 'channel:read:charity'},
    'charity_campaign_stop':
        {'name': 'channel.charity_campaign.stop', 'version': '1', 'scope': 'channel:read:charity'},
    'goal_begin':
        {'name': 'channel.goal.begin', 'version': '1', 'scope': 'channel:read:goals'},
    'goal_progress':
        {'name': 'channel.goal.progress', 'version': '1', 'scope': 'channel:read:goals'},
    'goal_end':
        {'name': 'channel.goal.end', 'version': '1', 'scope': 'channel:read:goals'},
    'hype_train_begin':
        {'name': 'channel.hype_train.begin', 'version': '1', 'scope': 'channel:read:hype_train'},
    'hype_train_progress':
        {'name': 'channel.hype_train.progress', 'version': '1', 'scope': 'channel:read:hype_train'},
    'hype_train_end':
        {'name': 'channel.hype_train.end', 'version': '1', 'scope': 'channel:read:hype_train'},
    'shield_mode_begin':
        {'name': 'channel.shield_mode.begin', 'version': '1', 'scope': 'moderator:read:shield_mode'},
    'shield_mode_end':
        {'name': 'channel.shield_mode.end', 'version': '1', 'scope': 'moderator:read:shield_mode'},
    'shoutout_create':
        {'name': 'channel.shoutout.create', 'version': '1', 'scope': 'moderator:read:shoutouts'},
    'shoutout_receive':
        {'name': 'channel.shoutout.receive', 'version': '1', 'scope': 'moderator:read:shoutouts'},
    'stream_online':
        {'name': 'stream.online', 'version': '1', 'scope': None},
    'stream_offline':
        {'name': 'stream.offline', 'version': '1', 'scope': None}
}

Scopes: http.Scopes = [
    'analytics:read:extensions',
    'analytics:read:games',
    'bits:read',
    'channel:edit:commercial',
    'channel:manage:broadcast',
    'channel:manage:extensions',
    'channel:manage:guest_star',
    'channel:manage:moderators',
    'channel:manage:polls',
    'channel:manage:predictions',
    'channel:manage:raids',
    'channel:manage:redemptions',
    'channel:manage:schedule',
    'channel:manage:videos',
    'channel:manage:vips',
    'channel:moderate',
    'channel:read:charity',
    'channel:read:editors',
    'channel:read:goals',
    'channel:read:guest_star',
    'channel:read:hype_train',
    'channel:read:polls',
    'channel:read:predictions',
    'channel:read:redemptions',
    'channel:read:stream_key',
    'channel:read:subscriptions',
    'channel:read:vips',
    'chat:edit',
    'chat:read',
    'clips:edit',
    'moderation:read',
    'moderator:manage:announcements',
    'moderator:manage:automod',
    'moderator:manage:automod_settings',
    'moderator:manage:banned_users',
    'moderator:manage:blocked_terms',
    'moderator:manage:chat_messages',
    'moderator:manage:chat_settings',
    'moderator:manage:shield_mode',
    'moderator:manage:shoutouts',
    'moderator:read:automod_settings',
    'moderator:read:blocked_terms',
    'moderator:read:chat_settings',
    'moderator:read:chatters',
    'moderator:read:followers',
    'moderator:read:guest_star',
    'moderator:read:shield_mode',
    'moderator:read:shoutouts',
    'user:edit',
    'user:edit:broadcast',
    'user:edit:follows',
    'user:manage:blocked_users',
    'user:manage:chat_color',
    'user:manage:whispers',
    'user:read:blocked_users',
    'user:read:broadcast',
    'user:read:email',
    'user:read:follows',
    'user:read:subscriptions',
    'whispers:edit',
    'whispers:read']


class Value:
    """
    Represents a value with an associated boolean flag.

    Attributes
    ----------
    is_enabled: bool
        A boolean flag indicating whether the value is enabled or disabled.
    value: int
        The integer value associated with the flag.

    Methods
    -------
    __bool__() -> bool
        Returns the boolean value of the is_enabled attribute.
    __int__() -> int
        Returns the integer value of the value attribute.
    """
    __slots__ = ('is_enabled', 'value')

    def __init__(self, data: Dict[str, Union[str, bool]]) -> None:
        value1 = list(data.items())[0][-1]
        value2 = list(data.items())[1][-1]
        self.is_enabled: bool = value1 if isinstance(value1, bool) else value2
        self.value: int = value2 if isinstance(value1, bool) else value1

    def __bool__(self) -> bool:
        return self.is_enabled

    def __int__(self) -> int:
        return int(self.value)

    def __repr__(self):
        return f'<Value is_enabled={self.is_enabled} value={self.value}>'


class Images:
    """
    Represents image URLs in different resolutions.

    Attributes
    ----------
    url_1x: str
        URL for the 1x resolution image.
    url_2x: str
        URL for the 2x resolution image.
    url_4x: str
        URL for the 4x resolution image.
    """
    __slots__ = ('url_1x', 'url_2x', 'url_4x')

    def __init__(self, data: ImagesType) -> None:
        self.url_1x: str = data['url_1x']
        self.url_2x: str = data['url_2x']
        self.url_4x: str = data['url_4x']

    def __repr__(self):
        return f'<Images url_1x={self.url_1x} url_2x={self.url_2x} url_4x={self.url_4x}>'


def generate_random_text(length=28) -> str:
    """
    Generate a random text of the specified length.
    """
    characters = string.ascii_letters + string.digits

    # Generate a random text of the specified length
    random_text = ''.join(random.choice(characters) for _ in range(length))
    return random_text


def get_subscriptions(events: List[str]) -> List[http.SubscriptionInfo]:
    """
    Retrieve a list of subscriptions that needed for subscribing to event.
    """
    counter = Counter(events)
    default_subscriptions: List[str] = ['channel_update', 'user_update', 'stream_online', 'stream_offline']
    counter.update(default_subscriptions)
    return [Subscriptions[sub] for sub in list(counter.keys()) if Subscriptions.get(sub) is not None]


class _Missing:
    """
    Placeholder class to represent missing values.
    """
    __slots__ = ()

    def __eq__(self, other) -> bool:
        return False

    def __bool__(self) -> bool:
        return False


# Constant representing a missing value. This can be used to indicate that a value is missing or unavailable.
MISSING: Any = _Missing()

# Constant representing a exclusive value.
EXCLUSIVE: Any = _Missing


def convert_rfc3339(timestamp: Optional[str]) -> Optional[datetime]:
    """
    Converts an RFC3339 timestamp string to a datetime object.
    """
    if timestamp is None:
        return None
    return datetime.fromisoformat(timestamp)


def convert_to_pst_rfc3339(date_time: datetime) -> str:
    """
    Convert a provided datetime to PST in RFC3339 format.
    """
    # Convert user-provided datetime to UTC
    utc_datetime = date_time.replace(tzinfo=timezone.utc)
    # Convert to PST by subtracting 8 hours
    pst_datetime = utc_datetime - timedelta(hours=8)
    # Format PST datetime in RFC3339 format
    formatted_pst_rfc3339 = pst_datetime.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    # Manually adjust the UTC offset format
    formatted_pst_rfc3339 = formatted_pst_rfc3339.replace("+0000", "Z")
    return formatted_pst_rfc3339


class ColoredFormatter(logging.Formatter):
    """
    Chat formatter for logger.
    """
    COLORS = {
        'DEBUG': '\033[37m',
        'INFO': '\033[97m',
        'WARNING': '\033[33m',
        'ERROR': '\033[31m',
        'CRITICAL': '\033[91m'
    }
    RESET_COLOR = '\033[0m'  # Reset to default color

    def __init__(self, colors: bool):
        super().__init__()
        self.colors = colors

    @staticmethod
    def hide_values_between_single_quotes(data: str):
        return re.sub(r"'(\w+_?(token|secret)\w*?)': '.*?'", lambda m: f"'{m.group(1)}': '//HIDDEN//'", data)

    def format(self, record):
        level_name = record.levelname
        formatted_record = self.hide_values_between_single_quotes(super().format(record))
        if self.colors and level_name in self.COLORS:
            return f"{self.COLORS[level_name]}{formatted_record}{self.RESET_COLOR}"
        return formatted_record


def ircv3_to_json(message: str) -> ChatMessageType:
    """
    Convert ircv3 to json.
    """
    parsed = {'command': {'command': '', 'channel': '', 'content': ''},
              'source': {'nick': '', 'host': ''},
              'tags': None,
              'parameters': ''}
    # Indicate that the message includes tags.
    if message.startswith('@'):
        _slice = message.split(' ', 1)
        parsed['tags'] = {
            k: v for k, v in (pair.split('=') for pair in _slice[0][12::].split(';') if '=' in pair)
        }
        message = _slice[-1]
    _slice = message.split(' ', 2)
    if '!' in _slice[0]:
        _source = _slice[0][1::].split('!')
        parsed['source'].update({'nick': _source[0], 'host': _source[1]})
    else:
        parsed['source'].update({'nick': '', 'host': _slice[0][1::]})
    parsed['command'].update({'command': _slice[1]})
    if _slice[-1].startswith('#'):
        _command = _slice[-1].split(' ', 1)
        parsed['command'].update({'channel': _command[0][1::],
                                  'content': None if len(_command) == 1 else _command[-1][1::]})
    parsed['parameters'] = _slice[-1]
    return parsed


def setup_logging(level: int = logging.DEBUG, colors: bool = False) -> logging.getLogger:
    """
    Setup logger.
    """
    handler = logging.StreamHandler()
    formatter = ColoredFormatter(colors=colors)
    handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(level=level)
    return logger
