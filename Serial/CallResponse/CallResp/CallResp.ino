int firstSensor = 0;    // first analog sensor
int secondSensor = 0;   // second analog sensor
int thirdSensor = 0;    // digital sensor
int inByte = 0;

void setup() {
  Serial.begin(9600);
  while (!Serial) {
    ; // wait ... Needed for native USB port only
  }

  pinMode(2, INPUT); 
  establishContact();
}

void loop() {
  if (Serial.available() > 0) {
    inByte = Serial.read();
    firstSensor = analogRead(A0) / 4;
    delay(10);
    secondSensor = analogRead(1) / 4;
    thirdSensor = map(digitalRead(2), 0, 1, 0, 255);
    
    Serial.write(firstSensor);
    Serial.write(secondSensor);
    Serial.write(thirdSensor);
  }
}

void establishContact() {
  while (Serial.available() <= 0) {
    Serial.print('A');
    delay(1000);
  }
}
