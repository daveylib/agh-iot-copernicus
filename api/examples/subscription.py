from api.utils.copernicus_observer import CopernicusObserver
from api.api_copernicus import APICopernicus
from api.utils.event_type import EventType
from time import sleep


class App(CopernicusObserver):
    def __init__(self):
        self.api = APICopernicus("/dev/tty.usbmodem143401")

        self.api.subscribe([EventType.BUTTON1], self)

    def update(self, event_type: EventType, event_value: int) -> None:
        print(f"Getting event type {event_type} with value {event_value} directly in the app")


app = App()

led_state = True

while True:
    print(f"Setting LED1 state to {led_state}")
    app.api.set_led1_state(led_state)

    sleep(0.5)
    led_state = not led_state
