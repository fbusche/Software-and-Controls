//This one works
#include <OneWire.h>
#include <DallasTemperature.h>
#include <Wire.h>
#define ONE_WIRE_BUS A0
#define address 5
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);
float r = 0.005; //wire dia in m
const float Mu = 0.000001257;
float a0;
float a1;
float a2;
float a3;
float v0;
float v1;
float v2;
float v3;
float g0;
float g1;
float g2;
float g3;
float c0;
float c1;
float c2;
float c3;
float ave0;
float ave1;
float ave2;
float ave3;
float cout0;
float cout1;
float cout2;
float cout3;
String data = "";
int flag = 0;
float t1 = 0;
float t2 = 0;
void setup() {
    Serial.begin(9600);
    pinMode(A2, INPUT);
    pinMode(A3, INPUT);
    pinMode(A6, INPUT);
    pinMode(A7, INPUT);
    int deviceCount = sensors.getDeviceCount();
    Wire.begin(address);
    Wire.onReceive(receiveEvent);
    Wire.onRequest(requestEvent);
}
void loop() {
    sensors.requestTemperatures();
    t1 = sensors.getTempCByIndex(0);
    t2 = sensors.getTempCByIndex(1);
    for (int i = 0; i < 200; i++) {
        a0 = analogRead(A2);
        a1 = analogRead(A3);
        a2 = analogRead(A6);
        a3 = analogRead(A7);
        v0 = (a0 * 5 / 1023);
        v1 = (a1 * 5 / 1023);
        v2 = (a2 * 5 / 1023);
        v3 = (a3 * 5 / 1023);
        g0 = ((v0 - 2.5) * (200) - 11);
        g1 = ((v1 - 2.5) * (200) - 11);
        g2 = ((v2 - 2.5) * (200) - 11);
        g3 = ((v3 - 2.5) * (200) - 11);
        c0 = ((g0 / 10000) * 2 * PI * r) / Mu;
        c1 = ((g1 / 10000) * 2 * PI * r) / Mu;
        c2 = ((g2 / 10000) * 2 * PI * r) / Mu;
        c3 = ((g3 / 10000) * 2 * PI * r) / Mu;
        ave0 = ave0 + c0;
        ave1 = ave1 + c1;
        ave2 = ave2 + c2;
        ave3 = ave3 + c3;
    }
    cout0 = ave0 / 200 +0.25;
    cout1 = ave1 / 100 + 0.25;
    cout2 = ave2 / 100 + 0.25;
    cout3 = ave3 / 100 + 0.25;

    c0=0;
    c1=0;
    c2=0;
    c3=0;
    ave0=0;
    ave1=0;
    ave2=0;
    ave3=0;
}

void receiveEvent(int howMany) {
  while (1 < Wire.available()) {
    char c = Wire.read();
    Serial.print(c);
  }
  int x = Wire.read();
  flag = x;  
}

void requestEvent() {
  int t1_int = abs(((int)t1)+1);
  int t2_int = abs(((int)t2)+1);
  int cout0_int = abs(((int)cout0)+1);
  int cout1_int = abs(((int)cout1)+1);
  int cout2_int = abs(((int)cout2)+1);
  int cout3_int = abs(((int)cout3)+1);


  data = (String)t1_int + "," + (String)t2_int + "," + (String)cout0_int + "," + (String)cout1_int + "," + (String)cout2_int + "," + (String)cout3_int;
  
  int Size = data.length();
  byte arrayByte[Size];
  for(int i=0; i < Size; i++){
    arrayByte[i] = byte(data[i]);
  }

  if(flag == 1){
    Wire.write(Size);
  }
  if(flag == 2){
    Wire.write(arrayByte, Size);
  }
}
