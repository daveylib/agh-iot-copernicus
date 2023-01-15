# IoT Project: Integration of AGH Copernicus with RaspberryPi 4
The goal of the project was to create a simple app based on integration of AGH Copernicus board with RaspberryPi 4. It 
displays board's current state and allows users to control all of its elements through a user-friendly interface.

![picture of initial state](images/initial_state.jpg)

## Implementation
Project follows the Observer design pattern. To communicate with the Copernicus board we used the `AppController` class 
inheriting from `CopernicusObserver`. It contains function `update()` which receives updates from `APICopernicus` about 
subscribed events and passes them to corresponding handlers in order to display changes in the UI. Analogical 
subscription handlers have been created in `APICopernicus` allowing changes made in UI to be displayed also on the 
actual Copernicus board.

## Usage
App can be launched from `main()` function in file `app.py`. Example usage of the app can be found in `api/examples` 
directory.

In UI it's possible to change angle of Dashboard (using Knob), state of Led1 and Led2 (using respectively Button1 and 
Button2) and color of Led2 (by clicking on it).

`APICopernicus` class contains methods that can be used manually to change or read state of each element of the AGH 
Copernicus board, such as:
- `set_dashboard_angle(self, angle: int)`
- `set_led1_state(self, state: bool)`
- `set_led2_color(self, red: int, green: int, blue: int)`
- `get_ambient_light(self)`
- `get_knob_position(self)`
- `get_temperature(self)`
- `get_motion_state(self)`
- `get_button1_state(self)`
- `get_button2_state(self)`

## Example
|                UI                |                 Copernicus board                 |
|:--------------------------------:|:------------------------------------------------:|
| ![Led2 - UI](images/led2_ui.jpg) | ![Led2 - Copernicus](images/led2_copernicus.jpg) |


