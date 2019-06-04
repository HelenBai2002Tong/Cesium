int val;
int tempPin = 1;

void setup()
{
Serial.begin(9600);
pinMode(5, OUTPUT);
pinMode(3,OUTPUT);
pinMode(2,OUTPUT);
}

float getTemperature() {
  float data = analogRead(tempPin);
  return (5.0 * data * 100.0) / 1024.0;  
}
void loop(){

float a = analogRead(tempPin);
float rtemp= (5.0 * a * 100.0) / 1024.0;
while(1){
digitalWrite(3,LOW);
digitalWrite(2,LOW);
Serial.print("Room Temperature: ");
Serial.println(rtemp);
float c = getTemperature();
Serial.print("C: ");
Serial.println(c);
if (c > (rtemp+2.0))
  {
    digitalWrite(5, LOW); 
    delay(10000);
    if (c > (rtemp+2.0)){
      digitalWrite(3,HIGH);
      digitalWrite(2,HIGH);
    }
  } else {
    digitalWrite(5, HIGH);
    digitalWrite(3,LOW);
    digitalWrite(2,LOW);
  }
 
/*val = analogRead(tempPin);
float mv = ( val/1024.0)*5000; 
float cel = mv/10;


Serial.print("TEMPRATURE = ");
Serial.print(cel);
Serial.print("*C");
Serial.println();
*/
delay(5000);
}
}
/* uncomment this to get temperature in farenhite 
Serial.print("TEMPRATURE = ");
Serial.print(farh);
Serial.print("*F");
Serial.println();


*/
