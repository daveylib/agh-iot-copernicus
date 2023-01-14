from api.utils.event_type import EventType
from abc import ABC, abstractmethod
from typing import Union


class CopernicusObserver(ABC):
    """CopernicusObserver interface used by APICopernicus"""
    @abstractmethod
    def update(self, event_type: EventType, event_value: Union[int, float, bool]) -> None:
        """Receive updates from APICopernicus about subscribed events"""
        pass
