#include <Wire.h>

#define address 0x04

String data = "[0.0,0.0,0.0,0.0]";

void setup() {
  Serial.begin(9600);
  Wire.begin(address);
  Wire.onReceive(receiveEvent);
  Wire.onRequest(requestEvent);

}

void loop() {

}

void receiveEvent(int byteCount) {
  while (1 < Wire.available()) {
    char c = Wire.read();
    Serial.print(c);
  }
  int x = Wire.read();
  Serial.println(x);
}

void requestEvent() {
  int Size = data.length();
  byte dataBytes[Size];
  for(int i=0; i < data.length(); i++){
    dataBytes[i] = (byte)(data[i]);
  }
  Wire.write(dataBytes, Size);
}
