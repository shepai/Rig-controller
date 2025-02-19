#include "Rig.h"

RigControl rig = RigControl(); // Use pin 13 for the LED

void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
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
  if (command.startsWith("CALIB-")) {
      int value, lower, val;
      sscanf(command.c_str(), "CALIB-%d,%d,%d", &x, &y, &z);
      rig.move(x, y, z);
      Serial.println("Calibration");
      Serial.println("done");
  } else if (command == "ZERO") {
      rig.zero();
      delay(10);
      Serial.println("done");
  } else if (command.startsWith("MOVE-")) {
      int x, y, z;
      sscanf(command.c_str(), "MOVE-%d,%d,%d", &x, &y, &z);
      rig.move(x, y, z);
      Serial.println("done");
  } else if (command=="RESET") {
      Serial.println("Resetting...");
      rig.reset();
      Serial.println("done");
  }else if () {
    
    
  }else {
      Serial.println("Unknown command");
      Serial.println("done");
  }
}