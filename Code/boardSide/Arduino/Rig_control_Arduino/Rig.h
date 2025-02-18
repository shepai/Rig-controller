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
    int positions[];
  public:
    // Constructor
    RigControl() {
      pinMode(buttonX, INPUT);
      pinMode(buttonY, INPUT);
      pinMode(buttonZ, INPUT);
      myMotorA = kit1.getStepper(200, 2);
      myMotorB = kit1.getStepper(200, 1);
      myMotorC = kit2.getStepper(200, 2);
      int positions[] ={0,0,0};
    }
    void setSpeeds(int rpm1, int rpm2, int rpm3) {
      myMotorA->setSpeed(rpm1);
      myMotorB->setSpeed(rpm2);
      myMotorC->setSpeed(rpm3);
    }
    void move(int x, int y, int z) {
      if(x>0){myMotorA->step(abs(x), FORWARD, SINGLE); }
      else{myMotorA->step(abs(x), BACKWARD, SINGLE); }
      if(y>0){myMotorB->step(abs(y), FORWARD, SINGLE); }
      else{myMotorB->step(abs(y), BACKWARD, SINGLE); }
      if(z>0){myMotorC->step(abs(z), FORWARD, SINGLE); }
      else{myMotorC->step(abs(z), BACKWARD, SINGLE); }
    }
    void zero(){

    }
    int * readButtons() {

    }
};

#endif
