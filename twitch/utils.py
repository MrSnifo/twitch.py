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

from datetime import datetime
from functools import wraps
import logging
import json
import time

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .types.eventsub.subscriptions import SubscriptionInfo
    from typing import Optional, List, Callable, Awaitable, Any, Dict
try:
    # noinspection PyPackageRequirements
    import orjson
except ImportError:
    orjson = None


def cache_decorator(expiry_seconds: int) -> Callable:
    """
    Cache decorator that caches the result of a function with a specified expiry time.

    :param expiry_seconds: The number of seconds to cache the result.
    :return: The decorated function.
    """
    cache = {}
    cache_expiry = {}

    def decorator(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
        """
        Decorator function that wraps the original function with caching logic.

        :param func: The original function to be decorated.
        :return: The wrapped function.
        """

        @wraps(func)
        async def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
            """
            Wrapper function that performs the caching logic before calling the original function.

            :param self: The instance object.
            :param args: The positional arguments passed to the function.
            :param kwargs: The keyword arguments passed to the function.
            :return: The result of the original function.
            """
            cache_key = (func.__name__, self, *args, frozenset(kwargs.items()))
            if cache_key in cache and time.time() < cache_expiry[cache_key]:
                return cache[cache_key]
            result = await func(self, *args, **kwargs)
            cache[cache_key] = result
            cache_expiry[cache_key] = time.time() + expiry_seconds
            return result

        return wrapper

    return decorator


def to_json(text: str, encoding='utf-8') -> dict:
    """
    Converts the given text to a JSON object (dict) using the specified encoding.

    :param text:
     The text to convert to JSON.

    :param encoding:
     The encoding to use when decoding the text. Defaults to 'utf-8'.

    :return:
     The JSON object (dict) representing the converted text.

    :raises UnicodeDecodeError: If the text cannot be decoded using the specified encoding.
    :raises json.JSONDecodeError: If the text is not valid JSON.
    """
    if orjson is not None:
        encoded_text = text.encode(encoding)
        return orjson.loads(encoded_text)  # type: ignore
    return json.loads(text)


def format_seconds(seconds: int) -> str:
    """
    Formats the given number of seconds into a string representation of days, hours, minutes,
    and seconds.

    :param seconds:
     The number of seconds.

    :return:
     The formatted time string.
    """
    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    time_components = []
    if days > 0:
        time_components.append(f"{days} day(s)")
    if hours > 0:
        time_components.append(f"{hours} hour(s)")
    if minutes > 0:
        time_components.append(f"{minutes} minute(s)")
    if seconds > 0:
        time_components.append(f"{seconds} second(s)")

    return " ".join(time_components)


def empty_to_none(text: Optional[str]) -> Optional[str]:
    """
    Converts an empty string to None.

    If the input string is empty or consists only of whitespace characters,
    this function returns None. Otherwise, it returns the input string as is.

    :param text:
     The string to be checked.

    :return:
     The input text if it is not empty, or None if it is empty.
    """

    if text and text != '':
        return text
    return None


def parse_rfc3339_timestamp(timestamp: str) -> datetime:
    """
    Parses a string representing a timestamp in RFC3339 format and returns a datetime object.

    :param timestamp:
     The timestamp in RFC3339 format to be parsed.

    :return:
     The parsed timestamp as a datetime object.
    """
    return datetime.fromisoformat(timestamp)


class ColoredFormatter(logging.Formatter):
    """
    Setup chat formatter for logger
    """
    COLORS = {
        'DEBUG': '\033[36m',  # Cyan
        'INFO': '\033[37m',  # White
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',  # Red
        'CRITICAL': '\033[91m'  # Light Red
    }
    RESET_COLOR = '\033[0m'  # Reset to default color

    def format(self, record):
        level_name = record.levelname
        if level_name in self.COLORS:
            record.level_name = f"{self.COLORS[level_name]}{level_name}{self.RESET_COLOR}"
        return super().format(record)


def setup_logging() -> logging.getLogger:
    """
    Setup logger
    """
    formatter = ColoredFormatter('%(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


# -------------------------------------------
#     Documentation Changelog last check
#              Date: 2023‑06‑15
# -------------------------------------------
Subscriptions: Dict[str, SubscriptionInfo] = {
    'channel_update':
        {'name': 'channel.update', 'version': '1'},
    'follow':
        {'name': 'channel.follow', 'version': '2'},
    'subscribe':
        {'name': 'channel.subscribe', 'version': '1'},
    'subscription_end':
        {'name': 'channel.subscription.end', 'version': '1'},
    'subscription_gift':
        {'name': 'channel.subscription.gift', 'version': '1'},
    'subscription_message':
        {'name': 'channel.subscription.message', 'version': '1'},
    'cheer':
        {'name': 'channel.cheer', 'version': '1'},
    'raid':
        {'name': 'channel.raid', 'version': '1'},
    'ban':
        {'name': 'channel.ban', 'version': '1'},
    'unban':
        {'name': 'channel.unban', 'version': '1'},
    'moderator_add':
        {'name': 'channel.moderator.add', 'version': '1'},
    'moderator_remove':
        {'name': 'channel.moderator.remove', 'version': '1'},
    'points_reward_add':
        {'name': 'channel.channel_points_custom_reward.add', 'version': '1'},
    'points_reward_update':
        {'name': 'channel.channel_points_custom_reward.update', 'version': '1'},
    'points_reward_remove':
        {'name': 'channel.channel_points_custom_reward.remove', 'version': '1'},
    'points_reward_redemption':
        {'name': 'channel.channel_points_custom_reward_redemption.add', 'version': '1'},
    'points_reward_redemption_update':
        {'name': 'channel.channel_points_custom_reward_redemption.update', 'version': '1'},
    'poll_begin':
        {'name': 'channel.poll.begin', 'version': '1'},
    'poll_progress':
        {'name': 'channel.poll.progress', 'version': '1'},
    'poll_end':
        {'name': 'channel.poll.end', 'version': '1'},
    'prediction_begin':
        {'name': 'channel.prediction.begin', 'version': '1'},
    'prediction_progress':
        {'name': 'channel.prediction.progress', 'version': '1'},
    'prediction_lock':
        {'name': 'channel.prediction.lock', 'version': '1'},
    'prediction_end':
        {'name': 'channel.prediction.end', 'version': '1'},
    'charity_campaign_donate':
        {'name': 'channel.charity_campaign.donate', 'version': '1'},
    'charity_campaign_start':
        {'name': 'channel.charity_campaign.start', 'version': '1'},
    'charity_campaign_progress':
        {'name': 'channel.charity_campaign.progress', 'version': '1'},
    'charity_campaign_stop':
        {'name': 'channel.charity_campaign.stop', 'version': '1'},
    'goal_begin':
        {'name': 'channel.goal.begin', 'version': '1'},
    'goal_progress':
        {'name': 'channel.goal.progress', 'version': '1'},
    'goal_end':
        {'name': 'channel.goal.end', 'version': '1'},
    'hype_train_begin':
        {'name': 'channel.hype_train.begin', 'version': '1'},
    'hype_train_progress':
        {'name': 'channel.hype_train.progress', 'version': '1'},
    'hype_train_end':
        {'name': 'channel.hype_train.end', 'version': '1'},
    'shield_mode_begin':
        {'name': 'channel.shield_mode.begin', 'version': '1'},
    'shield_mode_end':
        {'name': 'channel.shield_mode.end', 'version': '1'},
    'shoutout_create':
        {'name': 'channel.shoutout.create', 'version': '1'},
    'shoutout_receive':
        {'name': 'channel.shoutout.receive', 'version': '1'},
    'stream_online':
        {'name': 'stream.online', 'version': '1'},
    'stream_offline':
        {'name': 'stream.offline', 'version': '1'}}


def get_subscriptions(*, events: List[str]) -> List[SubscriptionInfo]:
    """
    Retrieve a list of subscriptions that needed for subscribing to event.
    """
    return [Subscriptions[sub] for sub in events if Subscriptions.get(sub) is not None]
