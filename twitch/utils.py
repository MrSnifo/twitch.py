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
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
import datetime
import logging
import json
import time

if TYPE_CHECKING:
    from typing import Any, Union, Dict, Optional
    import aiohttp

__all__ = ('setup_logging', 'json_or_text', 'convert_rfc3339', 'datetime_to_str', 'ExponentialBackoff')


def setup_logging(*,
                  handler: Optional[logging.Handler] = None,
                  level: Optional[int] = None,
                  root: bool = True) -> None:
    """
    Setup logging configuration.
    """
    if level is None:
        level = logging.INFO

    if handler is None:
        handler = logging.StreamHandler()

    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname}] {name}: {message}', dt_fmt, style='{')

    if root:
        logger = logging.getLogger()
    else:
        library, _, _ = __name__.partition('.')
        logger = logging.getLogger(library)

    handler.setFormatter(formatter)
    logger.setLevel(level)
    logger.addHandler(handler)


async def json_or_text(response: aiohttp.ClientResponse) -> Union[Dict[str, Any], str]:
    """Read response from aiohttp.ClientResponse, parse as JSON if content-type is 'application/json',
    otherwise return response text."""
    text = await response.text(encoding='utf-8')
    try:
        if 'application/json' in response.headers['content-type']:
            return json.loads(text)
    except KeyError:
        pass
    return text


def convert_rfc3339(timestamp: Optional[str]) -> Optional[datetime]:
    """
    Convert RFC3339 timestamp string to a datetime object (UTC +0).
    """
    if timestamp.endswith('Z'):
        timestamp = timestamp[:-1] + '+00:00'
    return None if (not timestamp) else datetime.datetime.fromisoformat(timestamp)


def datetime_to_str(__time: Optional[datetime], /) -> Optional[str]:
    """
    Convert local datetime object to UTC formatted RFC3339 timestamp string.
    """
    return None if time is None else __time.astimezone(datetime.timezone.utc).isoformat()


class ExponentialBackoff:
    """
    Handles retry intervals with exponential backoff.

    Parameters
    ----------
    base_delay: int
        The initial delay in seconds. The delay starts at this value and increases
        exponentially with each retry.
    max_delay: int
        The maximum delay between retries. The exponential increase is capped
        at this value.
    reset_interval: int
        The period in seconds after which the retry count is reset if no errors occur.
    """

    __slots__ = ('base_delay', 'max_delay', 'reset_interval', 'retry_count', 'last_failure_time')

    def __init__(self, base_delay: int = 1, max_delay: int = 180, reset_interval: int = 300) -> None:
        self.base_delay: int = base_delay
        self.max_delay: int = max_delay
        self.reset_interval: int = reset_interval
        self.retry_count: int = 0
        self.last_failure_time: float = time.monotonic()

    def get_delay(self) -> int:
        """

        Determine the delay before the next retry attempt.

        Returns
        -------
        int
            The delay in seconds before the next retry attempt.
        """
        current_time = time.monotonic()
        elapsed_time = current_time - self.last_failure_time

        if elapsed_time > self.reset_interval:
            self.retry_count = 0

        delay = min(self.base_delay * 2 ** self.retry_count, self.max_delay)
        self.retry_count += 1
        self.last_failure_time = current_time
        return delay
