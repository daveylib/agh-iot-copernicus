from api.utils.copernicus_observer import CopernicusObserver
from api.utils.event_type import EventType
from typing import List, Union
from serial import Serial
import threading


class APICopernicus:
    """High-level Python API to the AGH Copernicus board"""
    def __init__(self, serial_port: str, serial_timeout = 3):
        """Initialize Serial communication to the Arduino board"""
        self.serial = Serial(serial_port, 115200, timeout=serial_timeout)

        self.__running_subscription: threading.Thread = None
        self.__subscribed_events: List[EventType] = []
        self.__observer: CopernicusObserver = None

    def __send_command(self, cmd: int) -> bool:
        """
        Send command to the Arduino board

        Return True if operation was successful, False otherwise
        """
        self.serial.write(chr(cmd).encode())

        return True

    def __get_response(self) -> int:
        """Wait for response from the Arduino board and return it"""
        response = self.serial.read(1)

        if len(response) == 0:
            raise Exception("Response was not received from the Arduino board")

        return ord(response)

    def __subscription_handler(self):
        """Wait for update and parse it"""
        cmd = 128

        cmd += 32 if EventType.LIGHT in self.__subscribed_events else 0
        cmd += 16 if EventType.BUTTON1 in self.__subscribed_events else 0
        cmd += 8 if EventType.BUTTON2 in self.__subscribed_events else 0
        cmd += 4 if EventType.KNOB in self.__subscribed_events else 0
        cmd += 2 if EventType.TEMPERATURE in self.__subscribed_events else 0
        cmd += 1 if EventType.MOTION in self.__subscribed_events else 0

        self.__send_command(cmd)

        while self.__observer:
            update = self.serial.read(1)

            if len(update) == 0:
                continue

            update = ord(update)
            event_type = APICopernicus.__get_event_type(update)

            if event_type not in self.__subscribed_events:
                continue

            event_value = APICopernicus.__get_event_value(event_type, update)

            self.__observer.update(event_type, event_value)

    def subscribe(self, events: List[EventType], observer: CopernicusObserver):
        """Subscribe to specific events performed on the AGH Copernicus board"""
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

        cmd = angle

        return self.__send_command(cmd)

    def set_led1_state(self, state: bool) -> bool:
        """
        Set state of the LED1

        Return True if operation was successful, False otherwise
        """
        cmd = 32 + int(state)

        return self.__send_command(cmd)

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

        cmd = 64

        cmd |= red << 4
        cmd |= green << 2
        cmd |= blue

        return self.__send_command(cmd)

    def get_ambient_light(self) -> int:
        """Return value of ambient light in range from 0 to 63"""
        cmd = 128 + 64 + 32
        self.__send_command(cmd)

        response = self.__get_response()

        return APICopernicus.__get_event_value(EventType.LIGHT, response)

    def get_knob_position(self) -> int:
        """Return value of the knob position in range from 0 to 63"""
        cmd = 128 + 64 + 4
        self.__send_command(cmd)

        response = self.__get_response()

        return APICopernicus.__get_event_value(EventType.KNOB, response)

    def get_temperature(self) -> float:
        """Return temperature measured in Celsius in range from 10 to 41.5"""
        cmd = 128 + 64 + 2
        self.__send_command(cmd)

        response = self.__get_response()

        return APICopernicus.__get_event_value(EventType.TEMPERATURE, response)

    def get_motion_state(self) -> bool:
        """Return True if motion is detected"""
        cmd = 128 + 64 + 1
        self.__send_command(cmd)

        response = self.__get_response()

        return APICopernicus.__get_event_value(EventType.MOTION, response)

    def get_button1_state(self) -> bool:
        """Return True if the Button 1 is pressed, False otherwise"""
        cmd = 128 + 64 + 16
        self.__send_command(cmd)

        response = self.__get_response()

        return APICopernicus.__get_event_value(EventType.BUTTON1, response)

    def get_button2_state(self) -> bool:
        """Return True if the Button 2 is pressed, False otherwise"""
        cmd = 128 + 64 + 8
        self.__send_command(cmd)

        response = self.__get_response()

        return APICopernicus.__get_event_value(EventType.BUTTON2, response)

    @staticmethod
    def __get_event_value(event_type: EventType, response: int) -> Union[float, int, bool]:
        """Return value from the response based on the specific event type"""
        if event_type in [EventType.LIGHT, EventType.KNOB, EventType.TEMPERATURE]:
            event_value = response & 63

            if event_type == EventType.TEMPERATURE:
                event_value = event_value / 2 + 10
        else:
            event_value = bool(response & 1)

        return event_value

    @staticmethod
    def __get_event_type(response: int) -> EventType:
        """Return type of event based on the response from the Arduino board"""
        if APICopernicus.__check_bit(response, 7, False):
            if APICopernicus.__check_bit(response, 6, False):
                return EventType.LIGHT
            else:
                return EventType.KNOB
        else:
            if APICopernicus.__check_bit(response, 6, False):
                return EventType.TEMPERATURE
            else:
                if APICopernicus.__check_bit(response, 2, False):
                    if APICopernicus.__check_bit(response, 1, False):
                        return EventType.MOTION
                    else:
                        return EventType.BUTTON1
                else:
                    return EventType.BUTTON2

    @staticmethod
    def __check_bit(response: int, bit: int, expected: bool) -> bool:
        """Return True if a specific bit in the response equals to expected, False otherwise"""
        return bool((response >> bit) & 1) == expected
