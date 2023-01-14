from api.api_copernicus import APICopernicus

api = APICopernicus()

print("Setting dashboard angle to 30")
api.set_dashboard_angle(30)

print("Turning on LED1")
api.set_led1_state(True)

print("Turning on LED2 with green color")
api.set_led2_color(0, 3, 0)

print(f"Ambient light value: {api.get_ambient_light()}")
print(f"Knob position: {api.get_knob_position()}")
print(f"Temperature: {api.get_temperature()}")
print(f"Motion state: {api.get_motion_state()}")
print(f"Button 1 state: {api.get_button1_state()}")
print(f"Button 2 state: {api.get_button2_state()}")