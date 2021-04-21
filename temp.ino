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
  Wire.onRequest(requestEvent);
}

void loop() {
  v1 = v1 + 1.0;
  v2 = v2 + 0.1;
  v3 = v3 + 0.01;
  v4 = v4 + 0.001;
  v5 = v5 + 0.0001;
  data = "[" + String(v1) + "," + String(v2) + "," + String(v3) + "," + String(v4) + "," + String(v5) + "]"; //Grant did this
  //data = "[5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5]";
}

void requestEvent(){
  int dataByteCount = data.length();
  if(flag == 1){
    Wire.write(dataByteCount);
    Serial.println("-------------\nFlag: 1\nSize Sent: " + String(dataByteCount));
    if(dataByteCount < 33){flag = 2;}
    else{flag=3;}
  }

  else if(flag == 2){
    byte dataBytes[dataByteCount];
    for(int i=0; i < dataByteCount; i++){
      dataBytes[i] = (byte)(data[i]);
    }
    Wire.write(dataBytes, dataByteCount);
    Serial.println("-------------\nFlag: 2");
    flag = 1;
  }

  else if(flag == 3){
    byte dataBytes[32];
    for(int i=0; i < 32; i++){
      dataBytes[i] = (byte)(data[i]);
    }
    Wire.write(dataBytes, 32);
    Serial.println("-------------\nFlag: 3");
    flag = 4;
  }

  else if(flag == 4){
    int Size = (dataByteCount - 32);
    byte dataBytes[Size];
    for(int i=0; i < Size; i++){
      dataBytes[i] = (byte)(data[i+32]);
    }
    Wire.write(dataBytes, Size);
    Serial.println("-------------\nFlag: 4");
    flag = 1;
  }
}
