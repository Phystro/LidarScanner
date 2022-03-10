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

// constants and variables
const int STEPS = 2038;  // steps per revolution/ we have a 2038 step motor @ step is 0.1767 degrees

double dist_r = 0.0;
int intervals_z = 0;
double theta = 0.0;
double angle_interval = 360.0 / STEPS; // 0.1767 degress per step.
int steps_count = 0;
int steps_interval = 1;

bool scanning = false;
bool canMove = true;

// Object devices instances
Stepper stepperMotor(STEPS, 8, 9, 10, 11);
LIDARLite lidar;

int redPin = 2;
int greenPin = 3;
int btnOKPin = 4;
int btnLeftPin = 6;
int btnRightPin = 5;

void setup() {
  Serial.begin(115200);

  // set stepper motor speed in RPM. 6RPM corresponds to a 64 step complete rotation in 10s
  stepperMotor.setSpeed(100); // sets the delay between steps
  lidar.begin(0, true);
  lidar.configure(0);

  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(btnOKPin, INPUT);
  pinMode(btnLeftPin, INPUT);
  pinMode(btnRightPin, INPUT);

  angle_interval = angle_interval * steps_interval;
}

void loop() {

  if (digitalRead(btnOKPin)) {
    scanning = true;
    canMove = false;
  }

  if (digitalRead(btnLeftPin)) {
    if (canMove) {
//      stepperMotor.setSpeed(64);
      stepperMotor.step(64);
//      Serial.print("LEFT\n");
      delay(20);
    }
   }

   if (digitalRead(btnRightPin)) {
    if (canMove){
//      stepperMotor.setSpeed(64);
      stepperMotor.step(steps_interval);//
//      Serial.print("RIGHT\n");
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
  delay(100);
  
  scanning = true;
  dist_r = lidar.distance(false);
  stepperMotor.step(steps_interval); // turns motor n steps at N RPM.
  Serial.print("Steps: ");
  Serial.print(steps_count);
  Serial.print("\t");
  Serial.print(theta);
  Serial.print(",");
  Serial.print(dist_r);
  Serial.print(",");
  Serial.print(intervals_z);
  Serial.print("\n");
  delay(20);
  theta += angle_interval;
  steps_count++;

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
  delay(1000);
  intervals_z += 1;
}

void redON() {
  digitalWrite(redPin, HIGH);
}

void redOFF() {
  digitalWrite(redPin, LOW);
}

void greenON() {
  digitalWrite(greenPin, HIGH);
}

void greenOFF() {
  digitalWrite(greenPin, LOW);
}
