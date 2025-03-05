// rig controller lib
#include <Wire.h>
#include <Adafruit_MotorShield.h>

// Positions and speeds
int positions[3] = {0, 0, 0};  // class member, initialize outside constructor
int set_value[3] = {-3400, -6000, 600};  // class member

int sumArray(int arr[], int size) {
  int sum = 0;
  
  for (int i = 0; i < size; i++) {
    sum += arr[i];
  }
  
  return sum;
}

class RigControl {
  private:
    int buttonY = 7;    // pushbutton connected to digital pin 
    int buttonX = 6;    // pushbutton connected to digital pin
    int buttonZ = 9;    // pushbutton connected to digital pin
  Adafruit_MotorShield kit1; 
  Adafruit_MotorShield kit2;
  Adafruit_StepperMotor *myMotorA;
  Adafruit_StepperMotor *myMotorB;
  Adafruit_StepperMotor *myMotorC;
  int step=30;
  public:
    // Constructor
    RigControl() {
      pinMode(buttonX, INPUT);
      pinMode(buttonY, INPUT);
      pinMode(buttonZ, INPUT);
      //setSpeeds(0, 0, 0);
      
    }

    void init() { 
      kit1 = Adafruit_MotorShield(0x61); 
      kit2 = Adafruit_MotorShield(0x60); 
      delay(100);
      kit1.begin();
      delay(100);
      kit2.begin();
      delay(100);
      myMotorA = kit2.getStepper(180, 2);
      myMotorB = kit2.getStepper(180, 1);
      myMotorC = kit1.getStepper(200, 1);
      setSpeeds(100, 100, 100); // Initial speeds set here
    }

    void setSpeeds(int rpm1, int rpm2, int rpm3) { 
      myMotorA->setSpeed(rpm1);
      myMotorB->setSpeed(rpm2);
      myMotorC->setSpeed(rpm3);
    }
    void setStep(int st){
      step=st;
    }
    void move(int x, int y, int z) {
      int* states = readButtons();
      // Store directions and total steps
      int steps[3] = {abs(x), abs(y), abs(z)};
      int dir[3] = {x > 0 ? FORWARD : BACKWARD, y > 0 ? FORWARD : BACKWARD, z > 0 ? FORWARD : BACKWARD};
      // Move each motor one at a time
      while (sumArray(steps,3) > 0) {
        int remainingSteps=0;
        for (int j = 0; j < 3; j++) {
          remainingSteps = steps[j];
          // Move one step for each motor
          if (remainingSteps > 0) {
            if (j == 0) {myMotorA->step(step, dir[0], DOUBLE);positions[0] += step;}
            else if (j == 1) {myMotorB->step(step, dir[1], DOUBLE);positions[1] += step;}
            else if (j == 2) {myMotorC->step(step, dir[2], DOUBLE);positions[2] += step;}
            steps[j]=remainingSteps-step;
          }
          states = readButtons();
          if (states[j]==1 && dir[j]==FORWARD && j<2){steps[j] = 0;}
          else if (states[j]==1 && dir[j]==BACKWARD && j==2){steps[j] = 0;}
        }
      }
    }

    void reset() {
      int movearray[3] = {0, 0, 0};
      int* states = readButtons();
      while (true) {
        states = readButtons();
        if (states[0] == 1 && states[1] == 1 && states[2] == 1){
          break;
        }
        movearray[0] = 0; movearray[1] = 0; movearray[2] = 0;
        if (states[0] == 0) {
          movearray[0] = 30;
        }
        if (states[1] == 0) {
          movearray[1] = 30;
        }
        if (states[2] == 0) {
          movearray[2] = -30;
        }
        
        move(movearray[0], movearray[1], movearray[2]);
      }
    }

    void centre() { 
      positions[0] = 0; positions[1] = 0; positions[2] = 0;
    }

    int* readButtons() {
      static int buttonStates[3];  // Static array to keep data after function exits
      delay(10);
      buttonStates[0] = digitalRead(buttonX);
      buttonStates[1] = digitalRead(buttonY);
      buttonStates[2] = digitalRead(buttonZ); 
      return buttonStates;
    }
    void zero() {
      move(positions[0]*-1,positions[1]*-1,positions[2]*-1);
    }
    void calibrate() {
      move(set_value[0], set_value[1], set_value[2]);
      centre();
    }
};

