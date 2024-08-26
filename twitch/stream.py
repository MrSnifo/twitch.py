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

from typing import TYPE_CHECKING, overload
from .utils import datetime_to_str
import datetime

if TYPE_CHECKING:
    from typing import Optional, List, AsyncGenerator, Dict, Any, Literal
    from .types import Data, PData, channels, streams
    from .state import ConnectionState
    from .user import User

__all__ = ('Stream', 'BroadcasterStream')


class Stream:
    """
    Represents a channel stream.
    """

    __slots__ = ('_state', '_user_id', '_auth_user_id')

    def __init__(self, user_id: str, auth_user_id: str, *, state: ConnectionState) -> None:
        self._state: ConnectionState = state
        self._user_id: str = user_id
        self._auth_user_id: str = auth_user_id

    @overload
    async def get_live(self) -> streams.StreamInfo:
        ...

    @overload
    async def get_live(self) -> None:
        ...

    async def get_live(self) -> Optional[streams.StreamInfo]:
        """
        Retrieve the live stream information for the broadcaster.

        Returns
        -------
        Optional[streams.StreamInfo]
            A dictionary representing the live stream information if the broadcaster is live; otherwise, None.
        """
        data: PData[List[streams.StreamInfo]] = await self._state.http.get_streams(self._auth_user_id,
                                                                                   user_ids=[self._user_id])
        return data['data'][0] if len(data['data']) != 0 else None

    async def create_marker(self, description: Optional[str] = None) -> streams.StreamMarkerInfo:
        """
        Create a stream marker for the broadcaster.

        | Scopes                     | Description                                 |
        | -------------------------- | --------------------------------------------|
        | `channel:manage:broadcast` | Manage a channel’s broadcast configuration. |

        Parameters
        ----------
        description: Optional[str]
            A description for the marker.

        Returns
        -------
        streams.StreamMarkerInfo
            A dictionary representing the stream marker information.
        """
        data: Data[List[streams.StreamMarkerInfo]] = await self._state.http.create_stream_marker(self._auth_user_id,
                                                                                                 self._user_id,
                                                                                                 description)
        return data['data'][0] if len(data['data']) != 0 else None

    async def send_shoutout(self, user: User) -> None:
        """
        Send a shoutout to another broadcaster.

        | Scopes                       | Description                       |
        | ---------------------------- | ----------------------------------|
        | `moderator:manage:shoutouts` | Manage a broadcaster’s shoutouts. |

        Parameters
        ----------
        user: User
            The user to whom the shoutout will be sent.
        """
        await self._state.http.send_a_shoutout(self._user_id,
                                               self._auth_user_id,
                                               to_broadcaster_id=user.id)

    async def create_clip(self, has_delay: bool = False) -> channels.ClipEdit:
        """
        Create a clip of the broadcaster's stream.

        | Scopes       | Description                 |
        | ------------ | ----------------------------|
        | `clips:edit` | Manage Clips for a channel. |

        Parameters
        ----------
        has_delay: bool
            Whether to create the clip with a delay.

        Returns
        -------
        channels.ClipEdit
            A dictionary representing the clip edit information.
        """
        data: Data[List[channels.ClipEdit]] = await self._state.http.create_clip(self._auth_user_id,
                                                                                 self._user_id,
                                                                                 has_delay=has_delay)
        return data['data'][0]

    async def fetch_schedule(self,
                             segment_ids: Optional[List[str]] = None,
                             start_time: Optional[datetime.datetime] = None,
                             *,
                             first: int = 25) -> AsyncGenerator[streams.Schedule, None]:
        """
        Fetch the broadcaster's stream schedule.

        Parameters
        ----------
        segment_ids: Optional[List[str]]
            A list of segment IDs to filter the schedule.
        start_time: Optional[datetime.datetime]
            The start time to filter the schedule.
        first: int
            The number of items to return per request.

        Yields
        ------
        AsyncGenerator[streams.Schedule, None]
            A dictionary representing a schedule segment.
        """
        kwargs: Dict[str, Any] = {
            'segment_ids': segment_ids,
            'start_time': datetime_to_str(start_time),
            'broadcaster_id': self._user_id,
            'first': first
        }
        while True:
            data: PData[List[streams.Schedule]] = await self._state.http.get_channel_stream_schedule(
                self._auth_user_id,
                **kwargs)
            yield data['data']
            kwargs['after'] = data['pagination'].get('cursor')
            if not kwargs['after']:
                break

    async def get_channel_icalendar(self) -> str:
        """
        Retrieve the iCalendar link for the broadcaster's stream schedule.

        Returns
        -------
        str
            A string representing the iCalendar link for the broadcaster's stream schedule.
        """
        data: str = await self._state.http.get_channel_icalendar(self._auth_user_id, self._user_id)
        return data


class BroadcasterStream(Stream):
    """
    Represents a Broadcaster channel stream.
    """

    __slots__ = ()

    def __init__(self, user_id: str, *, state: ConnectionState) -> None:
        super().__init__(user_id, user_id, state=state)

    async def get_key(self) -> str:
        """
        Retrieve the stream key for the broadcaster.

        | Scopes                    | Description                           |
        | ------------------------- | --------------------------------------|
        | `channel:read:stream_key` | View an authorized user’s stream key. |

        Returns
        -------
        str
            A string representing the stream key.
        """
        data: Data[List[streams.StreamKey]] = await self._state.http.get_stream_key(self._user_id)
        return data['data'][0]['stream_key']

    async def start_commercial(self, length: int = 180) -> streams.CommercialStatus:
        """
        Start a commercial break on the broadcaster's stream.

        | Scopes                    | Description                   |
        | ------------------------- | ------------------------------|
        | `channel:edit:commercial` | Run commercials on a channel. |

        Parameters
        ----------
        length: int
            The duration of the commercial in seconds.

        Returns
        -------
        streams.CommercialStatus
            A dictionary representing the status of the commercial break.
        """
        data: Data[List[streams.CommercialStatus]] = await self._state.http.start_commercial(self._user_id, length)
        return data['data'][0]

    async def start_raid(self, user: User) -> streams.RaidInfo:
        """
        Start a raid to another broadcaster's channel.

        | Scopes                 | Description                               |
        | ---------------------- | ------------------------------------------|
        | `channel:manage:raids` | Manage a channel raiding another channel. |

        Parameters
        ----------
        user: User
            The user to whom the raid will be directed.

        Returns
        -------
        streams.RaidInfo
            A dictionary representing the raid information.
        """
        data: Data[List[streams.RaidInfo]] = await self._state.http.start_raid(self._user_id, user.id)
        return data['data'][0]

    async def cancel_raid(self) -> None:
        """
        Cancel an ongoing raid.

        | Scopes                 | Description                               |
        | ---------------------- | ------------------------------------------|
        | `channel:manage:raids` | Manage a channel raiding another channel. |
        """
        await self._state.http.cancel_raid(self._user_id)

    async def get_ad_schedule(self) -> streams.AdSchedule:
        """
        Retrieve the advertisement schedule for the broadcaster.

        | Scopes             | Description                                        |
        | ------------------ | ---------------------------------------------------|
        | `channel:read:ads` | Read the ads schedule and details on your channel. |
        | `channel:manage:ads` | Manage ads schedule on a channel.                |

        Returns
        -------
        streams.AdSchedule
            A dictionary representing the advertisement schedule.
        """
        data: Data[List[streams.AdSchedule]] = await self._state.http.get_ad_schedule(self._user_id)
        return data['data'][0]

    async def snooze_next_ad(self) -> streams.AdSnooze:
        """
        Snooze the next scheduled advertisement.

        | Scopes               | Description                       |
        | -------------------- | ----------------------------------|
        | `channel:manage:ads` | Manage ads schedule on a channel. |

        Returns
        -------
        streams.AdSnooze
            A dictionary representing the snooze status of the next ad.
        """
        data: Data[List[streams.AdSnooze]] = await self._state.http.snooze_next_ad(self._user_id)
        return data['data'][0]

    @overload
    async def update_schedule_vacation(self,
                                       enable: Literal[False],
                                       vacation_start_time: None = None,
                                       vacation_end_time: None = None,
                                       timezone: None = None) -> None: ...

    @overload
    async def update_schedule_vacation(self,
                                       enable: Literal[True],
                                       vacation_start_time: datetime.datetime,
                                       vacation_end_time: datetime.datetime,
                                       timezone: str) -> None: ...

    async def update_schedule_vacation(self,
                                       enable: bool,
                                       vacation_start_time: Optional[datetime.datetime] = None,
                                       vacation_end_time: Optional[datetime.datetime] = None,
                                       timezone: Optional[str] = None) -> None:
        """
        Update the vacation settings for the broadcast schedule.

        | Scopes                    | Description                         |
        | ------------------------- | ------------------------------------|
        | `channel:manage:schedule` | Manage a channel’s stream schedule. |

        Parameters
        ----------
        enable: bool
            Whether to enable or disable vacation mode.
        vacation_start_time: Optional[datetime.datetime]
            The start time of the vacation.
        vacation_end_time: Optional[datetime.datetime]
            The end time of the vacation.
        timezone: Optional[str]
            The [timezone](https://nodatime.org/TimeZones) of the vacation times.
        """
        await self._state.http.update_channel_stream_schedule(self._user_id, enable,
                                                              datetime_to_str(vacation_start_time),
                                                              datetime_to_str(vacation_end_time),
                                                              timezone)

    async def create_schedule_segment(self,
                                      start_time: datetime.datetime,
                                      timezone: str,
                                      duration: int,
                                      is_recurring: Optional[bool] = None,
                                      category_id: Optional[str] = None,
                                      title: Optional[str] = None) -> streams.Schedule:
        """
        Create a new schedule segment for the broadcaster's stream.

        | Scopes                    | Description                         |
        | ------------------------- | ------------------------------------|
        | `channel:manage:schedule` | Manage a channel’s stream schedule. |

        Parameters
        ----------
        start_time: datetime.datetime
            The start time of the schedule segment.
        timezone: str
            The [timezone](https://nodatime.org/TimeZones) of the start time.
        duration: int
            The duration of the schedule segment in minutes.
        is_recurring: Optional[bool]
            Whether the segment is recurring.
        category_id: Optional[str]
            The category ID of the segment.
        title: Optional[str]
            The title of the segment.

        Returns
        -------
        streams.Schedule
            A dictionary representing the created schedule segment.
        """
        data: Data[List[streams.Schedule]] = await self._state.http.create_channel_schedule_segment(
            self._user_id,
            datetime_to_str(start_time),
            timezone,
            duration,
            is_recurring,
            category_id,
            title)
        return data['data'][0]

    async def update_schedule_segment(self,
                                      segment_id: str,
                                      start_time: Optional[datetime.datetime] = None,
                                      duration: Optional[int] = None,
                                      category_id: Optional[str] = None,
                                      title: Optional[str] = None,
                                      is_canceled: Optional[bool] = None,
                                      timezone: Optional[str] = None) -> streams.Schedule:
        """
        Update an existing schedule segment for the broadcaster's stream.

        | Scopes                    | Description                         |
        | ------------------------- | ------------------------------------|
        | `channel:manage:schedule` | Manage a channel’s stream schedule. |

        Parameters
        ----------
        segment_id: str
            The ID of the segment to update.
        start_time: Optional[datetime.datetime]
            The new start time of the segment.
        duration: Optional[int]
            The new duration of the segment in minutes.
        category_id: Optional[str]
            The new category ID of the segment.
        title: Optional[str]
            The new title of the segment.
        is_canceled: Optional[bool]
            Whether the segment is canceled.
        timezone: Optional[str]
            The [timezone](https://nodatime.org/TimeZones) of the segment times.

        Returns
        -------
        streams.Schedule
            A dictionary representing the updated schedule segment.
        """
        data: Data[List[streams.Schedule]] = await self._state.http.update_channel_schedule_segment(
            self._user_id,
            segment_id,
            start_time,
            duration,
            category_id,
            title,
            is_canceled,
            timezone
        )
        return data['data'][0]

    async def delete_schedule_segment(self, segment_id: str) -> None:
        """
        Delete an existing schedule segment from the broadcaster's stream schedule.

        | Scopes                    | Description                         |
        | ------------------------- | ------------------------------------|
        | `channel:manage:schedule` | Manage a channel’s stream schedule. |

        Parameters
        ----------
        segment_id: str
            The ID of the segment to delete.
        """
        await self._state.http.delete_channel_schedule_segment(self._user_id, segment_id)
