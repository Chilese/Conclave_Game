from typing import Callable, Dict, List
from functools import partial

class GameEventManager:
    _events: Dict[str, List[Callable]] = {}

    @classmethod
    def subscribe(cls, event_name: str, callback: Callable) -> None:
        if event_name not in cls._events:
            cls._events[event_name] = []
        cls._events[event_name].append(callback)

    @classmethod
    def unsubscribe(cls, event_name: str, callback: Callable) -> None:
        if event_name in cls._events:
            cls._events[event_name].remove(callback)

    @classmethod
    def trigger(cls, event_name: str, *args, **kwargs) -> None:
        if event_name in cls._events:
            for callback in cls._events[event_name]:
                callback(*args, **kwargs)
