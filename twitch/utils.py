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

# Core
from .types.eventsub.subscriptions import Subscriptions

# Libraries
from datetime import datetime
from functools import wraps
import logging
import json
import time

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .types.eventsub.subscriptions import SubscriptionPayload
    from typing import Optional, List, Callable, Awaitable, Any
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
    else:
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


def get_subscriptions(*, events: List[str]) -> List[SubscriptionPayload]:
    """
    Retrieve a list of subscriptions that needed for subscribing to event.
    """
    return [Subscriptions[sub] for sub in events if Subscriptions.get(sub) is not None]
