from utils.copernicus_observer import CopernicusObserver
from utils.event_type import EventType
from random import getrandbits, randint
from typing import List
import threading
from time import sleep



class APICopernicus:
    """High-level Python API to the AGH Copernicus board"""
    def __init__(self):
        self.__running_subscription: threading.Thread = None
        self.__subscribed_events: List[EventType] = []
        self.__observer: CopernicusObserver = None

    def __subscription_handler(self):
        """Wait for update and parse it"""
        while self.__observer:
            x = randint(0, 4)
            if x == 0:
                self.__observer.update(EventType.BUTTON1, self.get_button1_state())
            elif x == 1:
                self.__observer.update(EventType.BUTTON2, self.get_button2_state())
            elif x == 2:
                self.__observer.update(EventType.KNOB, self.get_knob_position())
            elif x == 3:
                self.__observer.update(EventType.TEMPERATURE, self.get_temperature())
            elif x == 4:
                self.__observer.update(EventType.LIGHT, self.get_ambient_light())
            sleep(3)

    def subscribe(self, events: List[EventType], observer: CopernicusObserver):
        """Subscribe to specific events performed on the board"""
        self.stop_subscribing()

        self.__subscribed_events = events
        self.__observer = observer

        self.__running_subscription = threading.Thread(target=self.__subscription_handler)
        self.__running_subscription.daemon = True
        self.__running_subscription.start()

    def stop_subscribing(self):
        """Stop running subscription"""
        if self.__running_subscription and self.__running_subscription.is_alive():
            self.__subscribed_events = []
            self.__observer = None
            self.__running_subscription.join()

    def set_dashboard_angle(self, angle: int) -> bool:
        """
        Set the dashboard angle

        Return True if operation was successful, False otherwise
        """
        if angle < 0 or angle > 31:
            raise Exception("Dashboard angle must be in range from 0 to 31")

        return True

    def set_led1_state(self, state: bool) -> bool:
        """
        Set state of the LED1

        Return True if operation was successful, False otherwise
        """
        return True

    def set_led2_color(self, red: int, green: int, blue: int) -> bool:
        """
        Set color of the LED2

        Return True if operation was successful, False otherwise
        """
        if red < 0 or red > 3:
            raise Exception("Red color must be in range from 0 to 3")

        if green < 0 or green > 3:
            raise Exception("Green color must be in range from 0 to 3")

        if blue < 0 or blue > 3:
            raise Exception("Blue color must be in range from 0 to 3")

        return True

    def get_ambient_light(self) -> int:
        """Return value of ambient light in range from 0 to 63"""
        return getrandbits(6)

    def get_knob_position(self) -> int:
        """Return value of the knob position in range from 0 to 63"""
        return getrandbits(6)

    def get_temperature(self) -> float:
        """Return temperature measured in Celsius in range from 10 to 41.5"""
        return getrandbits(6) / 2 + 10

    def get_motion_state(self) -> bool:
        """Return True if motion is detected"""
        return bool(getrandbits(1))

    def get_button1_state(self) -> bool:
        """Return True if the Button 1 is pressed, False otherwise"""
        return bool(getrandbits(1))

    def get_button2_state(self) -> bool:
        """Return True if the Button 2 is pressed, False otherwise"""
        return bool(getrandbits(1))
