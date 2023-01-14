void setup() {
  // Serial communication to the USB port
  Serial.begin(115200);

  // Serial communication to the AGH Copernicus board
  Serial1.begin(38400);
}

void loop() {
  // Forward requests from Serial to Serial1
  while (Serial.available() > 0) {
    char serial_request = Serial.read();

    Serial1.write(serial_request);
  }

  // Forward responses from Serial1 to Serial
  while (Serial1.available() > 0) {
    char serial_response = Serial1.read();

    Serial.write(serial_response);
  }
}
