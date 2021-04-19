#define hall_pin1    A0
#define hall_pin2    A1

float diameter = 0.07; // meters
float circ = PI*diameter;
int rots1,rots2 = 0;
float d1,d2 = 0; 
float v1,v2 = 0;
unsigned long timer1prev,timer2prev = 0;
bool prev1,prev2 = true;

void setup() {
  Serial.begin(2000000);
  pinMode(hall_pin1, INPUT);
  pinMode(hall_pin2, INPUT);
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

    Serial.print("["+(String)d1+", "+(String)d2+", "+(String)v1+", "+(String)v2+"]");
  }
}
