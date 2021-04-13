#include <Wire.h>

#define SLAVE_ADDRESS 0x06

void setup() {
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
}

void loop() {
  //delay(100);
}

byte data = 0.0;
String data_from_pi = "";
int flag = 0;

void receiveData(int byteCount){
  char c = Wire.read()
  if(c == '1'){flag = 1;}
  if(c == '2'){flag = 2};
  Serial.print("Data Received: ");
  Serial.println(data_from_pi);
}

void sendData() {
  Wire.write(data);
  data++;
}
