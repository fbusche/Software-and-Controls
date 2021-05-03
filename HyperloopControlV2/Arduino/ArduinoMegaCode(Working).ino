//Faith did this
#include <Servo.h>
#include <Wire.h>
Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;
Servo servo6;
Servo servo7;
Servo servo8;

int Arduino_Address = 7;
static_assert(LOW == 0, "Expecting LOW to be a 0");
void setup() {
  Wire.begin(Arduino_Address); // initiate the wire library
  
  servo1.attach(3); // pins 2-13 are for PWM on Mega, pins 4 and 13 have diff frequency tho so I skipped over 4 to keep them all same
  servo2.attach(5);
  servo3.attach(6);
  servo4.attach(7);
  servo5.attach(8);
  servo6.attach(9);
  servo7.attach(10);
  servo8.attach(11);

  servo1.write(0);
  servo2.write(0);
  servo3.write(0);
  servo4.write(0);
  servo5.write(0);
  servo6.write(0);
  servo7.write(0);
  servo8.write(0);  
  
  Wire.onReceive(receiveEvent); // register event
  
}

void loop() { }

void receiveEvent(int howMany) {
  while (1 < Wire.available()) {
    char c = Wire.read();
  }
  int motor_speed = Wire.read();
  Serial.println("Updating Motor Speed: " + motor_speed);
  servo1.write(motor_speed);
  servo2.write(motor_speed);
  servo3.write(motor_speed);
  servo4.write(motor_speed);
  servo5.write(motor_speed);
  servo6.write(motor_speed);
  servo7.write(motor_speed);
  servo8.write(motor_speed);  
  
}
