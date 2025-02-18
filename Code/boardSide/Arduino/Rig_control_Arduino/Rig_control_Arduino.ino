#include "Rig.h"

RigControl rig = RigControl(); // Use pin 13 for the LED

void setup() {
  Serial.begin(9600);
}

void loop() {
  int* buttons = rig.readButtons();
  Serial.println(buttons[0]+buttons[1]+buttons[2]);
  delay(500);
}
