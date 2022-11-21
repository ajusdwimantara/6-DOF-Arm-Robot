#if defined(ARDUINO) && ARDUINO >= 100
  #include "Arduino.h"
#else
  #include <WProgram.h>
#endif

#include <Servo.h> 
#include <ros.h>
#include <ros/time.h>
#include <std_msgs/Float32.h>
#include <arm_robot/servo.h>

ros::NodeHandle  nh;
std_msgs::Float32 distance_msg, sensorData, kalmanFilterData;
std_msgs::Float32 Xt, Xt_update, Xt_prev;
std_msgs::Float32 Pt, Pt_update, Pt_prev;
std_msgs::Float32 Kt, R, Q;
ros::Publisher pub_range("/distance", &distance_msg);

Servo servo1, servo2, servo3, servo4, servo5, servo6;
const int echoPin = 2; // attach pin D2 Arduino to pin Echo of HC-SR04
const int trigPin = 3; //attach pin D3 Arduino to pin Trig of HC-SR04

void servo_cb( const arm_robot::servo& cmd_msg){
  servo1.write(cmd_msg.servo0 * 180 / 3.14); //set servo angle, should be from 0-180  
  delay(50);
  servo4.write(cmd_msg.servo3 * 180 / 3.14);
  delay(50);
  servo3.write(cmd_msg.servo2 * 180 / 3.14);
  delay(50);
  servo2.write(cmd_msg.servo1 * 180 / 3.14);
  delay(50);
  servo5.write(cmd_msg.servo4 * 180 / 3.14);
  delay(50);
  servo6.write(cmd_msg.servo5 * 180 / 3.145);
  delay(50);
}


ros::Subscriber<arm_robot::servo> servo_sub("/servo", servo_cb);

void setup(){
//  pinMode(13, OUTPUT);
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an OUTPUT
  pinMode(echoPin, INPUT); // Sets the echoPin as an INPUT
  nh.initNode();
  nh.subscribe(servo_sub);
  nh.advertise(pub_range);
  
  servo1.attach(6); 
  servo2.attach(7); 
  servo3.attach(10); 
  servo4.attach(11); 
  servo5.attach(12); 
  servo6.attach(13);
}

std_msgs::Float32 getRange(int echoPin, int trigPin){
  float duration;
  std_msgs::Float32 distance;
  // Clears the trigPin condition
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin HIGH (ACTIVE) for 10 microseconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  // Calculating the distance
  distance.data = duration * 0.034 / 2; // Speed of sound wave divided by 2 (go and back)

  return distance;
}

void loop(){
  distance_msg = getRange(echoPin, trigPin);

  pub_range.publish(&distance_msg);

  nh.spinOnce();
  delay(1);
}
