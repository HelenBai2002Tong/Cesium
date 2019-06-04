int led = 11;
void setup() 

{

pinMode(led,OUTPUT);

}

void loop()

{

  int val = analogRead(0);

  val = map(val, 0, 1023, 0, 255);

  analogWrite(10, val);

}
