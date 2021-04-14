#include <OneWire.h>
#include <DallasTemperature.h>
#define ONE_WIRE_BUS A0
#include <math.h>

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);
double r = 0.005; //wire dia in m
const double Mu = 0.000001257;
double a0;
double a1;
double a2;
double a3;
double v0;
double v1;
double v2;
double v3;
double g0;
double g1;
double g2;
double g3;
double c0;
double c1;
double c2;
double c3;
double ave0;
double ave1;
double ave2;
double ave3;
double cout0;
double cout1;
double cout2;
double cout3;
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
        a0 = analogRead(A3)*1000;
        a1 = analogRead(A4)*1000;
        a2 = analogRead(A6)*1000;
        a3 = analogRead(A7)*1000;
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

    float mt1 = t1 * 1000;
    float mt2 = t1 * 1000;

    long lt1 = (long)t1;
    long lt2 = (long)t2;
    
    long trunc0 = trunc(0);
    long trunc1 = trunc(1);
    long trunc2 = trunc(2);
    long trunc3 = trunc(3);
    

    
    //Serial.println((String)t1 + "," + (String)t2 + "," + (String)cout0 + "," + (String)cout1 + "," + (String)cout2 + "," + (String)cout3);
    double sendArray [6] = {abs(t1)/1000.0, abs(t2)/1000.0, abs(cout0)/1000.0, abs(cout1)/1000.0, abs(cout2)/1000.0, abs(cout3)/1000.0};
    for(int i = 0; i < 6; i++){
      Serial.println(sendArray[i]);
      delay(10);
    }

    delay(10000);
    
}
