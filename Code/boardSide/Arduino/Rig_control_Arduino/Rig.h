// rig controller lib
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "Adafruit_PWMServoDriver.h"

#ifndef LEDCONTROL_H
#define LEDCONTROL_H

Adafruit_MotorShield kit1 = Adafruit_MotorShield(0x60); 
Adafruit_MotorShield kit2 = Adafruit_MotorShield(0x70); 

class RigControl {
  private:
    Adafruit_StepperMotor *myMotorA;
    Adafruit_StepperMotor *myMotorB;
    Adafruit_StepperMotor *myMotorC;
    int buttonX = 7;    // pushbutton connected to digital pin 
    int buttonY = 7;    // pushbutton connected to digital pin
    int buttonZ = 7;    // pushbutton connected to digital pin
    int* positions;
    int * set_value;
  public:
    // Constructor
    RigControl() {
      pinMode(buttonX, INPUT);
      pinMode(buttonY, INPUT);
      pinMode(buttonZ, INPUT);
      myMotorA = kit1.getStepper(200, 2);
      myMotorB = kit1.getStepper(200, 1);
      myMotorC = kit2.getStepper(200, 2);
      int set_value[3] = {10,10,10};
      int positions[3] ={0,0,0};
    }
    void setSpeeds(int rpm1, int rpm2, int rpm3) {
      myMotorA->setSpeed(rpm1);
      myMotorB->setSpeed(rpm2);
      myMotorC->setSpeed(rpm3);
    }
    void move(int x, int y, int z) { // move the steppers based on direction, but not if pushing against wall
      int* states = readButtons();
      if(x>0 && states[0]==0){myMotorA->step(abs(x), FORWARD, SINGLE); }
      else{myMotorA->step(abs(x), BACKWARD, SINGLE); }
      if(y>0 && states[1]==0){myMotorB->step(abs(y), FORWARD, SINGLE); }
      else{myMotorB->step(abs(y), BACKWARD, SINGLE); }
      if(z>0 && states[2]==0){myMotorC->step(abs(z), FORWARD, SINGLE); }
      else{myMotorC->step(abs(z), BACKWARD, SINGLE); }
      //update memory of position
      positions[0]+=x;
      positions[1]+=y;
      positions[2]+=z;
    }
    void zero(){ // return to states
      int moveX=positions[0]*-1;
      int moveY=positions[1]*-1;
      int moveZ=positions[2]*-1;
      move(moveX,moveY,moveZ);
      memset(positions, 0, sizeof(positions));  // Set all values to 0
    }
    int *readButtons() {
      static int buttonStates[3];  // Static array to keep data after function exits
      buttonStates[0] = digitalRead(buttonX);
      buttonStates[1] = digitalRead(buttonY);
      buttonStates[2] = digitalRead(buttonZ);
      return buttonStates;  // Return the array
  }
  void recalibrate() {
    move(set_value[0],set_value[1],set_value[2]);
  }

};

#endif
