// rig controller lib
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "Adafruit_PWMServoDriver.h"

#ifndef LEDCONTROL_H
#define LEDCONTROL_H

int sumArray(int arr[]) {
    int sum = 0;
    for (int i = 0; i < sizeof(arr); ++i)
        sum += arr[i];
    return sum;
}

class RigControl {
  private:
    Adafruit_StepperMotor *myMotorA;
    Adafruit_StepperMotor *myMotorB;
    Adafruit_StepperMotor *myMotorC;
    int buttonX = 7;    // pushbutton connected to digital pin 
    int buttonY = 8;    // pushbutton connected to digital pin
    int buttonZ = 9;    // pushbutton connected to digital pin
    int* positions;
    int * set_value;
  public:
    // Constructor
    RigControl() {
      pinMode(buttonX, INPUT);
      pinMode(buttonY, INPUT);
      pinMode(buttonZ, INPUT);
      
      int set_value[3] = {10,10,10};
      int positions[3] ={0,0,0};
      Adafruit_MotorShield kit1 = Adafruit_MotorShield(0x60); 
      Adafruit_MotorShield kit2 = Adafruit_MotorShield(0x70); 
      myMotorA = kit2.getStepper(200, 2);
      myMotorB = kit2.getStepper(200, 1);
      myMotorC = kit1.getStepper(200, 2);
      kit1.begin();
      kit2.begin();
      
      setSpeeds(100,100,100);
      
    }
    void setSpeeds(int rpm1, int rpm2, int rpm3) {
      myMotorA->setSpeed(rpm1);
      myMotorB->setSpeed(rpm2);
      myMotorC->setSpeed(rpm3);
    }
    void move(int x, int y, int z) { // move the steppers based on direction, but not if pushing against wall
      int* states = readButtons();
      //Serial.print(states[0]);Serial.print(states[1]);Serial.println(states[2]);
      //Serial.print(x);Serial.print(y);Serial.println(z);
      if(x>0 && states[0]==0){myMotorA->step(abs(x), FORWARD, DOUBLE); }
      else{myMotorA->step(abs(x), BACKWARD, DOUBLE); }
      if(y>0 && states[1]==0){myMotorB->step(abs(y), FORWARD, DOUBLE); }
      else{myMotorB->step(abs(y), BACKWARD, DOUBLE); }
      if(z>0 && states[2]==0){myMotorC->step(abs(z), FORWARD, DOUBLE); }
      else{myMotorC->step(abs(z), BACKWARD, DOUBLE); }
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
    void reset(){ //reset the rig till all buttons are suppressed
      int movearray[3] = {0,0,0};
      int* states = readButtons();
      while(sumArray(states)!=0) { //loop till all rig features are stuck
        states = readButtons();
        movearray[0]=0; movearray[1]=0; movearray[2]=0;
        if(states[0]) {
          movearray[0]=10;
        }if(states[1]) {
          movearray[1]=10;
        }if(states[2]) {
          movearray[2]=10;
        }
      }
    }
    void centre(int x, int y, int z) {
      move(x,y,z);
      positions[0]=0; positions[1]=0; positions[2]=0;
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
