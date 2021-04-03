#include <OneWire.h>
#include <DallasTemperature.h>
#define ONE_WIRE_BUS 2
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);
void setup(void) {
  Serial.begin(115200);
  int deviceCount = sensors.getDeviceCount();
}
void loop(void) {
 sensors.requestTemperatures();
 float t1 = sensors.getTempCByIndex(0);
 float t2 = sensors.getTempCByIndex(1);
 Serial.println("[" + (String)t1 + "," + (String)t2 + "," + "]");
}
