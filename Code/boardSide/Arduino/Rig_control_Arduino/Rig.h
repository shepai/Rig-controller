// rig controller lib
#include <Adafruit_MotorShield.h>
#include "Adafruit_PWMServoDriver.h"

#ifndef LEDCONTROL_H
#define LEDCONTROL_H

Adafruit_MotorShield kit1 = Adafruit_MotorShield(0x61); 
Adafruit_MotorShield kit2 = Adafruit_MotorShield(0x70);
Adafruit_StepperMotor *myMotorA = kit2.getStepper(180, 2);
Adafruit_StepperMotor *myMotorB = kit2.getStepper(180, 1);
Adafruit_StepperMotor *myMotorC = kit1.getStepper(200, 1);
// Positions and speeds
int positions[3] = {0, 0, 0};  // class member, initialize outside constructor
int set_value[3] = {10, 10, 10};  // class member

class RigControl {
  private:
    int buttonY = 7;    // pushbutton connected to digital pin 
    int buttonX = 8;    // pushbutton connected to digital pin
    int buttonZ = 9;    // pushbutton connected to digital pin
  public:
    // Constructor
    RigControl() {
      pinMode(buttonX, INPUT);
      pinMode(buttonY, INPUT);
      pinMode(buttonZ, INPUT);
      setSpeeds(0, 0, 0);
      
    }

    void init() { 
      kit2.begin();
      delay(100);
      kit1.begin();
      delay(100);
      setSpeeds(100, 100, 100); // Initial speeds set here
    }

    void setSpeeds(int rpm1, int rpm2, int rpm3) { 
      myMotorA->setSpeed(rpm1);
      myMotorB->setSpeed(rpm2);
      myMotorC->setSpeed(rpm3);
    }


    void move(int x, int y, int z) {
      int* states = readButtons();
      // Store directions and total steps
      int steps[3] = {abs(x), abs(y), abs(z)};
      int dir[3] = {x > 0 ? FORWARD : BACKWARD, y > 0 ? FORWARD : BACKWARD, z > 0 ? FORWARD : BACKWARD};
      // Move each motor one at a time
      
      for (int j = 0; j < 3; j++) {
        int remainingSteps = steps[j];
        while (remainingSteps > 0) {
          // Move one step for each motor
          if (remainingSteps > 0) {
            if (j == 0) {myMotorA->step(1, dir[0], DOUBLE);}
            else if (j == 1) {setSpeeds(100, 100, 0);myMotorB->step(1, dir[1], DOUBLE);setSpeeds(100, 100, 100);}
            else if (j == 2) {
              setSpeeds(100, 0, 100);
              myMotorC->step(1, dir[2], DOUBLE);setSpeeds(100, 100, 100);}
            remainingSteps--;
          }

          // Update button states and prevent movement if blocked
          states = readButtons();
          for (int i = 0; i < 3; i++) {
            if (states[i] != 0 && ((dir[i] == FORWARD && i < 2) || (dir[i] == BACKWARD && i == 2))) {
              remainingSteps = 0;  // Stop movement if blocked
            }
          }
        }
      }
      // Update memory of position
      positions[0] += x;
      positions[1] += y;
      positions[2] += z;
    }

    void zero() { 
      int moveX = positions[0] * -1;
      int moveY = positions[1] * -1;
      int moveZ = positions[2] * -1;
      move(moveX, moveY, moveZ);
      memset(positions, 0, sizeof(positions));  // Set all values to 0
    }

    void reset() {
      int movearray[3] = {0, 0, 0};
      int* states = readButtons();
      while (!(states[0] == 1 && states[1] == 1 && states[2] == 1)) {
        states = readButtons();
        movearray[0] = 0; movearray[1] = 0; movearray[2] = 0;
        if (states[0] == 0) {
          movearray[0] = 10;
        }
        if (states[1] == 0) {
          movearray[1] = 10;
        }
        if (states[2] == 0) {
          movearray[2] = 10;
        }
        move(movearray[0], movearray[1], movearray[2]);
      }
    }

    void centre(int x, int y, int z) { 
      move(x, y, z);
      positions[0] = 0; positions[1] = 0; positions[2] = 0;
    }

    int* readButtons() {
      static int buttonStates[3];  // Static array to keep data after function exits
      buttonStates[0] = digitalRead(buttonX);
      buttonStates[1] = digitalRead(buttonY);
      buttonStates[2] = digitalRead(buttonZ); 
      return buttonStates;
    }

    void recalibrate() {
      move(set_value[0], set_value[1], set_value[2]);
    }
};

#endif
