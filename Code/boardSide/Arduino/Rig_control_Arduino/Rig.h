// rig controller lib
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "Adafruit_PWMServoDriver.h"

#ifndef LEDCONTROL_H
#define LEDCONTROL_H
Adafruit_StepperMotor *myMotorA;
Adafruit_StepperMotor *myMotorB;
Adafruit_StepperMotor *myMotorC;
Adafruit_MotorShield kit1;
Adafruit_MotorShield kit2;
int sumArray(int arr[]) {
    int sum = 0;
    for (int i = 0; i < sizeof(arr); ++i)
        sum += arr[i];
    return sum;
}

class RigControl {
  private:
    
    int buttonY = 7;    // pushbutton connected to digital pin 
    int buttonX = 8;    // pushbutton connected to digital pin
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
      kit1 = Adafruit_MotorShield(0x60); 
      kit2 = Adafruit_MotorShield(0x70); 
      myMotorA = kit2.getStepper(200, 2);
      myMotorB = kit2.getStepper(200, 1);
      myMotorC = kit1.getStepper(200, 2);
      setSpeeds(100,100,100);
      
    }
    void init() { //init seperate to main load up to avoid interference with serial communication
      kit1.begin();
      kit2.begin();
    }
    void setSpeeds(int rpm1, int rpm2, int rpm3) { //set the speeds of each motor
      myMotorA->setSpeed(rpm1);
      myMotorB->setSpeed(rpm2);
      myMotorC->setSpeed(rpm3);
    }
    void move(int x, int y, int z) {
      int* states = readButtons();
      // Store directions and total steps
      int steps[3] = {abs(x), abs(y), abs(z)};
      int dir[3] = {x > 0 ? FORWARD : BACKWARD, y > 0 ? FORWARD : BACKWARD, z > 0 ? FORWARD : BACKWARD};
      // Prevent movement if blocked by limits
      for (int i = 0; i < 3; i++) {
        if (states[i] != 0) steps[i] = 0;
      }
      //find the motor with the most steps
      int max_steps = max(steps[0], max(steps[1], steps[2]));
      int accum[3] = {0, 0, 0};
      for (int i = 0; i < max_steps; i++) {
        // Move each motor proportionally
        for (int j = 0; j < 3; j++) {
          if (steps[j] > 0) {
            accum[j] += steps[j];
            if (accum[j] >= max_steps) {
              accum[j] -= max_steps;
              if (j == 0) myMotorA->step(1, dir[0], DOUBLE);
              if (j == 1) myMotorB->step(1, dir[1], DOUBLE);
              if (j == 2) myMotorC->step(1, dir[2], DOUBLE);
            }
          }
        } 
      }
      // Update memory of position
      positions[0] += x;
      positions[1] += y;
      positions[2] += z;
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
    void centre(int x, int y, int z) { //center the rig
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
