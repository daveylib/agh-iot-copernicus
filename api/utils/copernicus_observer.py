from utils.event_type import EventType
from abc import ABC, abstractmethod


class CopernicusObserver(ABC):
    """CopernicusObserver interface used by APICopernicus"""
    @abstractmethod
    def update(self, event_type: EventType, event_value: int) -> None:
        """Receive updates from APICopernicus about subscribed events"""
        pass
