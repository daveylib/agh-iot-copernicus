import eel
from app_controller import AppController


@eel.expose
def button1_down_handler():
    return app_controller.button1_handler(True)

@eel.expose
def button1_up_handler():
    return app_controller.button1_handler(False)

@eel.expose
def button2_down_handler():
    return app_controller.button2_handler(True)

@eel.expose
def button2_up_handler():
    return app_controller.button2_handler(False)

@eel.expose
def knob_handler(value):
    return app_controller.knob_handler(value)

@eel.expose
def toggle_led1():
    return app_controller.toggle_led1()

@eel.expose
def set_led2_color(color):
    rgb = {color: 3}
    return app_controller.set_led2_color(rgb.get('Red', 0), rgb.get('Green', 0), rgb.get('Blue', 0))

def start_server():
    eel.init('web')
    eel.start('index.html', size=(800, 600), block=True, port=8000, debug=False)


if __name__ == '__main__':
    app_controller = AppController("/dev/tty.usbmodem143401")
    start_server()





