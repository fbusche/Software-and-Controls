#include <Wire.h>

#define address 4

int flag = 0;
String var0 = "Grant ";
String var1 = "Is ";
String var3 = "A ";
String var9 = "Weenie and a Stinky";
String a = "";

void setup() {
  Wire.begin(address);
  Wire.onReceive(receiveEvent);
  Wire.onRequest(requestEvent);
  Serial.begin(9600);
}

void loop() {

}

void receiveEvent(int howMany) {
  while (1 < Wire.available()) {
    char c = Wire.read();
    Serial.print(c);
  }
  int x = Wire.read();
  flag = x;
  Serial.println("Flag Update To: " + (String)flag);
  
}
void requestEvent() {
  int Size = a.length();
  a = (var0 + var1 + var3 + var9);
  byte arrayByte[Size];
  for(int i=0; i < Size; i++){
    arrayByte[i] = byte(a[i]);
  }
  
  if(flag == 1){
    Wire.write(Size);
  }
  if(flag == 2){
    Wire.write(arrayByte, Size);
  }
}
