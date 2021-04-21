//By Faith
#include <Wire.h>

#define address 0x04

String data = "";
float v1 = 0.0;
float v2 = 0.00;
float v3 = 0.000;
float v4 = 0.0000;
float v5 = 0.00000;
int flag = 1;

void setup() {
  Serial.begin(9600);
  Wire.begin(address);
  Wire.onReceive(receiveEvent);
  Wire.onRequest(requestEvent);

}

void loop() {
  v1 = v1 + 1.0;
  v2 = v2 + 0.1;
  v3 = v3 + 0.01;
  v4 = v4 + 0.001;
  v5 = v5 + 0.0001;
  data = "[" + String(v1) + "," + String(v2) + "," + String(v3) + "," + String(v4) + "," + String(v5) + "]"; //Grant did this
  Serial.println(data);
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
  if(flag == 1) {
    Wire.write(Size);
    Serial.println("Flag: 1");
    Serial.println(Size);
    flag = 2;
  }
  
  if(flag == 2){
    Serial.println("Flag: 2");
    byte dataBytes[Size];
    for(int i=0; i < data.length(); i++){
      dataBytes[i] = (byte)(data[i]);
    }
    if(Size > 32){
      Wire.write(dataBytes, 32);
      byte dataBytes2[Size - 32];
      for(int i=33; i < data.length(); i++){
        dataBytes2[i] = dataBytes[i];
      }
      Wire.write(dataBytes2, (Size - 32));
      flag = 1;
    }
    else {
      flag = 1;
    }
  }
}
