#include "Rig.h"
RigControl rig; //= RigControl(); // Use pin 13 for the LED

void setup() {
  Serial.begin(921600);
  Serial.print("Loaded Rig...");
  Serial.println("Scanning I2C bus...");
  Wire.begin();  // Start I2C communication
  // Scan for all I2C devices
  for (byte i = 8; i < 120; i++) {
    Wire.beginTransmission(i);
    byte error = Wire.endTransmission();
    
    if (error == 0) {
      Serial.print("Found device at address 0x");
      Serial.println(i, HEX);
    }
  }

  pinMode(LED_BUILTIN, OUTPUT);
  //rig=RigControl(); 
  rig.init();

}

void loop() {
  
    String command = "";
    char incomingChar = "";
    while (incomingChar != '\n') {
        if (Serial.available() > 0) {   // Ensure there is data to read
            incomingChar = Serial.read();
            // Only add valid ASCII characters (printable range: 32-126)
            if (incomingChar >= 32 && incomingChar <= 126) {
                command += incomingChar;
            }
        }
    }
    command.trim();
    if (incomingChar == '\n') {
      Serial.println("Command recieved");
      ProcessCommand(command);
      flash();
    }
}

void flash() {
  digitalWrite(LED_BUILTIN, HIGH);  // turn the LED on (HIGH is the voltage level)
  delay(100);                      // wait for a second
  digitalWrite(LED_BUILTIN, LOW);   // turn the LED off by making the voltage LOW
  delay(100);  
}
void ProcessCommand(String command) {
  Serial.println(command);
  if (command.startsWith("CALIB")) {
      Serial.println("Calibration");
      rig.calibrate();
      Serial.println("done");
  } else if (command == "ZERO") {
      Serial.println("Zeroing device");
      rig.zero();
      delay(10);
      Serial.println("done");
  } else if (command.startsWith("MOVE,")) {
      Serial.println("Moving rig...");
      int x, y, z;
      sscanf(command.c_str(), "MOVE,%d,%d,%d", &x, &y, &z);
      rig.move(x, y, z);
      Serial.println("done");
  } else if (command=="RESET") {
      Serial.println("Resetting...");
      rig.reset();
      Serial.println("done");  
  }else if (command=="SHOW") {
      int* states = rig.readButtons();
      Serial.print(states[0]);Serial.print(states[1]);Serial.println(states[2]);
      Serial.println("done");
  }else {
      Serial.println("Unknown command");
      Serial.println("done");
  }
}