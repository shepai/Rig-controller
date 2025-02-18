#include "Rig.h"

LEDControl led(13); // Use pin 13 for the LED

void setup() {
  led.on(); // Turn on the LED
  delay(1000);
  led.off(); // Turn off the LED
}

void loop() {
  led.toggle(); // Toggle LED state
  delay(500);
}
