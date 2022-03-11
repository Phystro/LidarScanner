/*
 * Lidar Scanner
 * 
 * Description: Performs Lidar scan of a geological mines, creating a cylindrical set of codes, 
 *              that we later convert into rectangular set of coordinates.
 * 
 * Stepper Motor:
 *           Using 28BYJ-48 Stepper Motor with ULN2003 Driver and Arduino. The 28BYJ-48 is a 5-wire unipolar stepper motor.
 *           There are 2037.8864 ~ 2038 steps per revolution.
 * 
 * NB: for better control, keep the speed high and only go a few steps each call to step() of the motor.
 */

#include <Stepper.h>
#include <LIDARLite.h>

#define REDPIN 2
#define GREENPIN 3
#define OKBTNPIN 4
#define RIGHTBTNPIN 5
// stepper motor driver control inputs
#define IN1 8
#define IN2 9
#define IN3 10
#define IN4 11

// constants and variables
const int STEPS = 2038;  // steps per revolution/ we have a 2038 step motor @ step is 0.1767 degrees
const int RPMSPEED = 1;  // speed of rotation in RPM

double dist_r = 0.0;
int intervals_z = 0;
double theta = 0.0;
double angle_interval = 360.0 / STEPS; // 0.1767 degress per step.
int steps_interval = 1;

bool scanning = false;
bool canMove = true;

// Object devices instances
Stepper stepperMotor(STEPS, IN1, IN2, IN3, IN4);
LIDARLite lidar;

void setup() {
  Serial.begin(115200);

  // set stepper motor speed in RPM.
//  stepperMotor.setSpeed(RPMSPEED); // sets the delay between steps
  lidar.begin(0, true);
  lidar.configure(0);

  pinMode(REDPIN, OUTPUT);
  pinMode(GREENPIN, OUTPUT);
  pinMode(OKBTNPIN, INPUT);
  pinMode(RIGHTBTNPIN, INPUT);

  angle_interval = angle_interval * steps_interval;
}

void loop() {

  if (digitalRead(OKBTNPIN)) {
    scanning = true;
    canMove = false;
  }

   if (digitalRead(RIGHTBTNPIN)) {
    if (canMove){
      stepperMotor.step(steps_interval);
      delay(20);
    }
   }

  if (canMove) {
    adjustmentMode();
  }
  
  if (scanning) {
    lidarScan();
  }

}

void lidarScan() {
  redON();
  greenOFF();
  
  dist_r = lidar.distance(false);
  stepperMotor.step(steps_interval); // turns motor n steps at N RPM.

  Serial.print(theta);
  Serial.print(",");
  Serial.print(dist_r);
  Serial.print(",");
  Serial.print(intervals_z);
  Serial.print("\n");
  delay(20);
  theta += angle_interval;

  if (theta >= 360) {
    theta = 0.0;
    increment_z_intervals();
    scanning = false;
    canMove = true;
  }
  
}

void adjustmentMode() {
  redOFF();
  greenON();
}

void increment_z_intervals() {
  delay(500);
  intervals_z += 1;
}

void redON() {
  digitalWrite(REDPIN, HIGH);
}

void redOFF() {
  digitalWrite(REDPIN, LOW);
}

void greenON() {
  digitalWrite(GREENPIN, HIGH);
}

void greenOFF() {
  digitalWrite(GREENPIN, LOW);
}
