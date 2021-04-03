#include <OneWire.h>
#include <DallasTemperature.h>
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
void setup() {
    Serial.begin(9600);
    pinMode(A3, INPUT);
    pinMode(A4, INPUT);
    pinMode(A6, INPUT);
    pinMode(A7, INPUT);
    int deviceCount = sensors.getDeviceCount();
}
void loop() {
    sensors.requestTemperatures();
    float t1 = sensors.getTempCByIndex(0);
    float t2 = sensors.getTempCByIndex(1);
    for (int i = 0; i < 100; i++) {
        a0 = analogRead(A3);
        a1 = analogRead(A4);
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
    cout0 = ave0 / 200 + 8.75;
    cout1 = ave1 / 200 + 8.75;
    cout2 = ave2 / 200 + 8.75;
    cout3 = ave3 / 200 + 8.75;
    Serial.println((String)t1 + "," + (String)t2 + "," + (String)cout0 + "," + (String)cout1 + "," + (String)cout2 + "," + (String)cout3);
}
