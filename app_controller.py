from threading import Thread
from api.utils.copernicus_observer import CopernicusObserver
from api.api_copernicus import APICopernicus
from api.utils.event_type import EventType
from time import sleep
import eel

class AppController(CopernicusObserver):
    def __init__(self, serial_port: str):
        eel.init('web')
        self.api = APICopernicus(serial_port)
        self.led1_state = False
        self.led2_color = [0, 0, 0]
        self.button1_state = False
        self.button2_state = False
        self.button1_ui_state = False
        self.button2_ui_state = False
        self.button1_thread = None
        self.button2_thread = None
        self.dashboard_value = 0
        self.api.set_led1_state(self.led1_state)
        self.api.set_led2_color(self.led2_color[0], self.led2_color[1], self.led2_color[2])

        self.forward_update = {
            EventType.BUTTON1: self.__update_button1_state,
            EventType.BUTTON2: self.__update_button2_state,
            EventType.KNOB: self.__update_knob,
            EventType.LIGHT: self.__update_light_sensor,
            EventType.TEMPERATURE: self.__update_temperature
        }

        self.forward_update[EventType.BUTTON1](self.api.get_button1_state())
        self.forward_update[EventType.BUTTON2](self.api.get_button2_state())
        self.forward_update[EventType.KNOB](self.api.get_knob_position())
        self.forward_update[EventType.LIGHT](self.api.get_ambient_light())
        self.forward_update[EventType.TEMPERATURE](self.api.get_temperature())

        self.api.subscribe([EventType.BUTTON1, EventType.BUTTON2, EventType.KNOB, EventType.LIGHT, EventType.TEMPERATURE], self)

    def update(self, event_type: EventType, event_value: int) -> None:
        print(f"Getting event type {event_type} with value {event_value} directly in the app")
        self.forward_update[event_type](event_value)

    def __update_light_sensor(self, value: int) -> None:
        print(f"Setting Light Sensor value to {value}")
        eel.update_light_sensor(value)

    def __update_button1_state(self, state: bool) -> None:
        print(f"Setting Button1 state to {state}")
        self.button1_state = state
        eel.update_button1_state(state)

        if state:
            self.button1_thread = Thread(target=self.__button1_handler)
            self.button1_thread.daemon = True
            self.button1_thread.start()

    def __update_button2_state(self, state: bool) -> None:
        print(f"Setting Button2 state to {state}")
        self.button2_state = state
        eel.update_button2_state(state)

        if state:
            self.button2_thread = Thread(target=self.__button2_handler)
            self.button2_thread.daemon = True
            self.button2_thread.start()

    def __update_knob(self, value: int) -> None:
        print(f"Setting Knob value to {value}")
        eel.update_knob(value)
        self.__knob_handler(value)

    def __update_temperature(self, value: int) -> None:
        print(f"Setting Temperature value to {value}")
        eel.update_temperature(value)


    def toggle_led1(self) -> bool:
        print(f"Setting LED1 state to {not self.led1_state}")
        if self.api.set_led1_state(not self.led1_state):
            self.led1_state = not self.led1_state
        return self.led1_state

    def set_led2_color(self, red: int, green: int, blue: int) -> bool:
        print(f"Setting LED2 color to ({red}, {green}, {blue})")
        if self.api.set_led2_color(red, green, blue):
            self.led2_color = [red, green, blue]
            return True
        return False
    

    def update_dashboard_angle(self, angle: int) -> None:
        print(f"Setting dashboard angle to {angle}")
        self.api.set_dashboard_angle(angle)

    def __knob_handler(self, value: int) -> None:
        self.dashboard_value = value // 2
        self.api.set_dashboard_angle(self.dashboard_value)
        eel.update_dashboard(self.dashboard_value / 31 * 180)
    
    def knob_handler(self, value: int) -> bool:
        print(f"Knob change to {value}")
        self.__knob_handler(value)

    def __signal(self, delay: float) -> None:
        if not self.button1_ui_state and not self.button1_state:
            return
        
        self.api.set_led1_state(True)
        eel.update_led1(True)
        sleep(delay)
        self.api.set_led1_state(False)
        eel.update_led1(False)
        sleep(delay)

    def __button1_handler(self) -> None:
        while True:
            for _ in range(3):
                self.__signal(0.3)
            for _ in range(3):    
                self.__signal(1)
            for _ in range(3):
                self.__signal(0.3)
            if not self.button1_state and not self.button1_ui_state:
                return
            sleep(1)
    
    def button1_handler(self, state: bool) -> bool:
        if self.button1_state:
            return False

        print(f"Button1 state: {state}")
        self.button1_ui_state = state
        if not state:
            self.button1_thread.join()
            return True

        self.button1_thread = Thread(target=self.__button1_handler)
        self.button1_thread.daemon = True
        self.button1_thread.start()
        return True

    def __button2_handler(self) -> bool:
        id = self.led2_color.index(max(self.led2_color))
        while self.button2_state or self.button2_ui_state:
            self.led2_color[id] = 3
            self.api.set_led2_color(self.led2_color[0], self.led2_color[1], self.led2_color[2])
            eel.update_led2(self.led2_color)
            self.led2_color[id] = 0
            id = (id + 1) % 3
            sleep(1)

        self.api.set_led2_color(self.led2_color[0], self.led2_color[1], self.led2_color[2])
        eel.update_led2(self.led2_color)

        return True

    def button2_handler(self, state: bool) -> bool:
        if self.button2_state:
            return False

        print(f"Button2 state: {state}")
        self.button2_ui_state = state
        if not state:
            self.button2_thread.join()
            return True

        self.button2_thread = Thread(target=self.__button2_handler)
        self.button2_thread.daemon = True
        self.button2_thread.start()

        return True