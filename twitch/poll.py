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

from .utils import convert_rfc3339, Value
from datetime import timedelta

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Optional, Union, List
    from .types import poll as PollTypes
    from datetime import datetime

__all__ = ('Poll', 'PollChoice')


class PollChoice:
    """
    Represents a choice in a poll.

    Attributes
    ----------
    id: str
        The unique ID of the poll choice.
    title: str
        The title or description of the poll choice.
    votes: int
        The number of votes received for this poll choice.
    bits_votes: int
        The number of bits votes received for this poll choice.
    points_votes: int
        The number of channel points votes received for this poll choice.

    Methods
    -------
    __str__() -> str
        Returns the title of the PollChoice.
    __int__() -> int
        Returns the number of votes as an integer.
    __eq__(other: object) -> bool
        Checks if two PollChoice instances are equal based on their IDs.
    __ne__(other: object) -> bool
        Checks if two PollChoice instances are not equal.
    """
    __slots__ = ('id', 'title', 'votes', 'bits_votes', 'points_votes')

    if TYPE_CHECKING:
        id: str
        title: str
        votes: int
        bits_votes: int
        points_votes: int

    def __init__(self, data: PollTypes.PollChoice) -> None:
        self._form_data(data=data)

    def __repr__(self) -> str:
        return f'<PollChoice id={self.id} title={self.title} votes={self.votes}>'

    def __str__(self) -> str:
        return self.title

    def __int__(self) -> int:
        return self.votes

    def __eq__(self, other: object) -> bool:
        if isinstance(other, PollChoice):
            return self.id == other.id
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def _form_data(self, data: PollTypes.PollChoice) -> None:
        self.id = data['id']
        self.title = data['title']
        self.votes = data.get('votes') or 0
        self.points_votes = data.get('channel_points_votes') or 0
        self.bits_votes = data.get('bits_votes') or 0


class Poll:
    """
    Represents a poll on a Twitch channel.

    Attributes
    ----------
    id: str
        The unique ID of the poll.
    title: str
        The title or question of the poll.
    status: str
        The status of the poll (e.g., "ACTIVE", "COMPLETED").
    choices: List[PollChoice]
        The list of poll choices available in the poll.
    duration: int
        The duration of the poll in seconds.
    end_time: datetime
        The date and time when the poll ends.
    started_at: datetime
        The date and time when the poll started.
    bits_voting: Value
        The settings for bits voting in the poll.
    channel_points_voting: Value
        The settings for channel points voting in the poll.

    Methods
    -------
    __str__() -> str
        Returns the title of the Poll.
    __eq__(other: object) -> bool
        Checks if two Poll instances are equal based on their IDs.
    __ne__(other: object) -> bool
        Checks if two Poll instances are not equal.
    """
    __slots__ = ('id', 'title', 'status', 'choices', 'duration', 'end_time', 'started_at',
                 'bits_voting', 'channel_points_voting')

    if TYPE_CHECKING:
        id: str
        title: str
        status: str
        choices: List[PollChoice]
        duration: int
        end_time: datetime
        started_at: datetime
        bits_voting: Value
        channel_points_voting: Value

    def __init__(self, data: Union[PollTypes.Poll, Union[PollTypes.PollBeginAndProgressEvent,
                                                         PollTypes.PollEndEvent]]) -> None:
        # `channel_points_voting` is missing when using helix.
        if data.get('channel_points_voting') is None:
            self._form_data(data=data)
        else:
            self._form_event_data(data=data)

    def __repr__(self) -> str:
        return f'<Poll id={self.id} status={self.id} started_at={self.started_at} end_time={self.end_time}>'

    def __str__(self) -> str:
        return self.title

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Poll):
            return self.id == other.id
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def _form_data(self, data: PollTypes.Poll) -> None:
        self.id = data['id']
        self.title = data['title']
        self.status = data['status']
        self.choices = [PollChoice(data=choice) for choice in data['choices']]
        self.duration = data['duration']
        self.started_at = convert_rfc3339(data['started_at'])
        # If status is ``ACTIVE`` this set to None.
        _ended_at: Optional[str] = data['ended_at']
        if _ended_at:
            self.end_time = convert_rfc3339(_ended_at)
        else:
            self.end_time = self.started_at + timedelta(seconds=self.duration)

        # Response of `Poll End` & `Poll Begin` & `Poll Progress` does not match the helix.
        _bits_voting: PollTypes.AmountPerVote = {
            'is_enabled': data['bits_voting_enabled'],
            'amount_per_vote': data['bits_per_vote']}
        _channel_points_voting: PollTypes.AmountPerVote = {
            'is_enabled': data['channel_points_voting_enabled'],
            'amount_per_vote': data['channel_points_per_vote']}
        self.bits_voting = Value(data=_bits_voting)
        self.channel_points_voting = Value(data=_channel_points_voting)

    def _form_event_data(self, data: Union[PollTypes.PollBeginAndProgressEvent,
                                           PollTypes.PollEndEvent]) -> None:
        self.id = data['id']
        self.title = data['title']
        self.choices = [PollChoice(data=choice) for choice in data['choices']]
        self.started_at = convert_rfc3339(data['started_at'])
        self.bits_voting = Value(data=data['bits_voting'])
        self.channel_points_voting = Value(data=data['channel_points_voting'])

        # Missing on `Poll End` Event.
        _ends_at: Optional[str] = data.get('ends_at')
        # Missing on `Poll Begin` & `Poll Progress` Event.
        _ended_at: Optional[str] = data.get('ended_at')
        self.status = (data.get('status') or 'ACTIVE').upper()

        # Combining both of `_ends_at` and `_ended_at`.
        self.end_time = convert_rfc3339(_ends_at) if _ends_at else convert_rfc3339(_ended_at)

        # Missing on `Poll End` & `Poll Begin` & `Poll Progress` Event.
        self.duration = (self.end_time - self.started_at).seconds

    def to_json(self) -> PollTypes.PollToJson:
        # This is useful when you want to recreate the same poll.
        return ({
            'title': self.title,
            'choices': [{'title': choice.title} for choice in self.choices],
            'duration': self.duration,
            'points_voting_enabled': self.channel_points_voting.is_enabled,
            'points_per_vote': self.channel_points_voting.value,
        })
