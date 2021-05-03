#include <Wire.h>

#define hall_pin1    A0
#define hall_pin2    A1

#define address 5

float diameter = 0.07; // meters
float circ = PI*diameter;
int rots1,rots2 = 0;
float d1,d2 = 0; 
float v1,v2 = 0;
unsigned long timer1prev,timer2prev = 0;
bool prev1,prev2 = true;
int flag = 0;
String data = "";

void setup() {
  Serial.begin(9600);
  pinMode(hall_pin1, INPUT);
  pinMode(hall_pin2, INPUT);
  Wire.begin(address);
  Wire.onReceive(receiveEvent);
  Wire.onRequest(requestEvent);
}

void loop() {
  
  while (true) {
    bool cur1 = digitalRead(hall_pin1);
    bool cur2 = digitalRead(hall_pin2);
       
    if (prev1 and !cur1){ 
      unsigned long now = micros();  
      unsigned long int1 = now - timer1prev;
      timer1prev = now;
      d1 += circ;
      rots1++;
      v1 = circ/((float)int1/1000000.0);
      }
      
    if (prev2 and !cur2){ 
      unsigned long now = micros();  
      unsigned long int2 = now - timer2prev;
      timer2prev = now;
      d2 += circ;
      rots2++;
      v2 = circ/((float)int2/1000000.0);
      }
  
    prev1 = cur1;
    prev2 = cur2; 

  }
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
  int d1_int = abs(((int)d1));
  int d2_int = abs(((int)d2));
  int v1_int = abs(((int)v1));
  int v2_int = abs(((int)v2));


  data = (String)d1_int + "," + (String)d2_int + "," + (String)v1_int + "," + (String)v2_int;
  Serial.println(data);
  
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
