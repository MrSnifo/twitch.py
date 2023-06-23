from typing import List
from .user import Broadcaster


class Channel(Broadcaster):
    broadcaster_language: str
    game_name: str
    game_id: str
    title: str
    delay: int
    tags: List[str]
