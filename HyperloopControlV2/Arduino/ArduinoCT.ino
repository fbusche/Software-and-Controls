//This one works
#include <OneWire.h>
#include <DallasTemperature.h>
#include <Wire.h>
#define ONE_WIRE_BUS A0
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
int flag = 1;
void setup() {
    Serial.begin(9600);
//    pinMode(A2, INPUT);
//    pinMode(A3, INPUT);
//    pinMode(A6, INPUT);
//    pinMode(A7, INPUT);
    int deviceCount = sensors.getDeviceCount();
    Wire.begin(4);
    Wire.onRequest(requestEvent);
}
void loop() {
    sensors.requestTemperatures();
    float t1 = sensors.getTempCByIndex(0);
    float t2 = sensors.getTempCByIndex(1);
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
    Serial.println((String)t1 + "," + (String)t2 + "," + (String)cout0 + "," + (String)cout1 + "," + (String)cout2 + "," + (String)cout3);

    String string_t1 = String(t1,2);
    String string_t2 = String(t2,2);
    String string_cout0 = String(cout0,2);
    String string_cout1 = String(cout1,2);
    String string_cout2 = String(cout2,2);
    String string_cout3 = String(cout3,2);

    
    
    String data= "[" + string_t1 + "," + string_t2 + "," + string_cout0 + "," + string_cout1 + "," + string_cout2 + "," + string_cout3 + "]";
    //FOR DEBUG
    //System.out.println(to_I2C);


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
    Wire.beginTransmission(4);
    Wire.write(dataBytes, Size);
    Wire.endTransmission();
    flag = 1;
  }
}
