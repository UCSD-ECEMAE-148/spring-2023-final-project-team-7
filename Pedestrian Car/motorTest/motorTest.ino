#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"
#include <Servo.h>

Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 

Adafruit_DCMotor *RFMotor = AFMS.getMotor(1);
Adafruit_DCMotor *LFMotor = AFMS.getMotor(4);
Adafruit_DCMotor *RBMotor = AFMS.getMotor(2);
Adafruit_DCMotor *LBMotor = AFMS.getMotor(3);

byte motorSpeed = 70;                             //Max motor speed (do not exceed 70)
byte wait_time = 5000;
byte dist_time = 5000;

void setup() {
  AFMS.begin();
  RFMotor->setSpeed(motorSpeed);                   //Set motor speed
  LFMotor->setSpeed(motorSpeed);
  RBMotor->setSpeed(motorSpeed); 
  LBMotor->setSpeed(motorSpeed);

  RFMotor->run(RELEASE);                            //Release all motors before loop
  LFMotor->run(RELEASE);
  RBMotor->run(RELEASE);
  LBMotor->run(RELEASE);
}

void loop() {
  delay(wait_time);
  RFMotor->run(FORWARD);
  RBMotor->run(FORWARD);
  LFMotor->run(FORWARD);
  LBMotor->run(FORWARD);
  delay(dist_time);
  RFMotor->run(RELEASE);
  RBMotor->run(RELEASE);
  LFMotor->run(RELEASE);
  LBMotor->run(RELEASE);
  delay(wait_time);
  RFMotor->run(BACKWARD);
  RBMotor->run(BACKWARD);
  LFMotor->run(BACKWARD);
  LBMotor->run(BACKWARD);
  delay(dist_time);
  RFMotor->run(RELEASE);
  RBMotor->run(RELEASE);
  LFMotor->run(RELEASE);
  LBMotor->run(RELEASE);
}
