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

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .types import message as msg
    from typing import List


class Emote:
    """
    Represents a message emote.

    :param emote: A dictionary representing the emote with 'id', 'begin', and 'end' keys.
    """

    __slots__ = ('id', 'begin', 'end')

    def __init__(self, *, emote: msg.Emote) -> None:
        self.id: str = emote['id']
        self.begin: int = emote['begin']
        self.end: int = emote['end']

    def __repr__(self) -> str:
        return f'<Emote id={self.id} begin={self.begin} end={self.end}>'


class Message:
    """
    Represents a chat message.

    :param message: A dictionary representing the message with 'text' and 'emotes' keys.
    """

    __slots__ = ('content', '_emotes')

    def __init__(self, *, message: msg.Message) -> None:
        self.content: str = message['text']
        self._emotes: List[msg.Emote] = message['emotes']

    def __repr__(self) -> str:
        return f'<Message message={self.content}>'

    def __str__(self) -> str:
        return self.content

    @property
    def emotes(self) -> List[Emote]:
        """
        Retrieve the list of emotes in the message, if any.

        :return: List of Emote objects.
        """
        return [Emote(emote=emote) for emote in self._emotes]
