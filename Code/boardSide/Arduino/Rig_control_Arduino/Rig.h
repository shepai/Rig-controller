// rig controller lib
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_PWMServoDriver.h"

#ifndef LEDCONTROL_H
#define LEDCONTROL_H

Adafruit_MotorShield kit1 = Adafruit_MotorShield AFMStop(0x60); 
Adafruit_MotorShield kit2 = Adafruit_MotorShield AFMStop(0x70); 

class RigControl {
  private:
    Adafruit_StepperMotor *myMotorA = kit1.getStepper(200, 2);
    Adafruit_StepperMotor *myMotorB = kit1.getStepper(200, 2);
    Adafruit_StepperMotor *myMotorC = kit2.getStepper(200, 2);
    int positions[] ={0,0,0};
  public:
    // Constructor
    RigControl() {
      pin = ledPin;
      state = false;
      pinMode(pin, OUTPUT);
    }
    void setSpeeds(int rpm1, int rpm2, int rpm3) {
      myMotorA.setSpeed(rpm1);
      myMotorB.setSpeed(rpm2);
      myMotorC.setSpeed(rpm3);
    }
    void move(int x, int y, int z) {
      if(x>0){myMotorA.step(abs(x), FORWARD, SINGLE); }
      else{myMotorA.step(abs(x), BACKWARD, SINGLE); }
      if(y>0){myMotorB.step(abs(y), FORWARD, SINGLE); }
      else{myMotorB.step(abs(y), BACKWARD, SINGLE); }
      if(z>0){myMotorC.step(abs(z), FORWARD, SINGLE); }
      else{myMotorC.step(abs(z), BACKWARD, SINGLE); }
    }
    void zero(){
      
    }
    // Turn LED on
    void on() {
      digitalWrite(pin, HIGH);
      state = true;
    }

    // Turn LED off
    void off() {
      digitalWrite(pin, LOW);
      state = false;
    }

    // Toggle LED state
    void toggle() {
      state = !state;
      digitalWrite(pin, state ? HIGH : LOW);
    }

    // Get LED state
    bool isOn() {
      return state;
    }
};

#endif
