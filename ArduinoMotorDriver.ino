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

int motor_speed = 0;
int Arduino_Address = 0x04;
//int Arduino_Address = 0x05;
//int Arduino_Address = 0x06;
static_assert(LOW == 0, "Expecting LOW to be a 0);

void setup() {
  Wire.begin(Arduino_Address); // initiate the wire library
  
  Serial.begin(9600); //this part might be wrong because serial ports confuse me
  
  servo1.attach(3); // pins 2-13 are for PWM on Mega, pins 4 and 13 have diff frequency tho so I skipped over 4 to keep them all same
  servo2.attach(5);
  servo3.attach(6);
  servo4.attach(7);
  servo5.attach(8);
  servo6.attach(9);
  servo7.attach(10);
  servo8.attach(11);
  
  Wire.onReceive(receiveEvent); // register event
  
  servo1.write(motor_speed); // sets speed of the servo (0-180 in degrees)
  servo2.write(motor_speed);
  servo3.write(motor_speed);
  servo4.write(motor_speed);
  servo5.write(motor_speed);
  servo6.write(motor_speed);
  servo7.write(motor_speed);
  servo8.write(motor_speed);
}

void loop() {
  // put your main code here, to run repeatedly:

}

void receiveEvent(int howMany) {
  while (Wire.available()) {
    motor_speed = Wire.read();
    
    servo1.write(motor_speed);
    servo2.write(motor_speed);
    servo3.write(motor_speed);
    servo4.write(motor_speed);
    servo5.write(motor_speed);
    servo6.write(motor_speed);
    servo7.write(motor_speed);
    servo8.write(motor_speed);  
  }
}
