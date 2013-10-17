int sensorValue;
float voltage1;
float voltage0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  sensorValue = analogRead(A1);
  voltage1 = sensorValue * (5.0 / 1024.0);
  sensorValue = analogRead(A0);
  voltage0 = sensorValue * (5.0 / 1024.0);
  Serial.print(voltage0);Serial.print(", ");Serial.println(voltage1);
  delay(1000);
}
