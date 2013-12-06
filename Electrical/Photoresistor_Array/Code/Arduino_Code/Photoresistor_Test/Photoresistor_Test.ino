int sensorPin = A0;    // select the input pin for the potentiometer      // select the pin for the LED
int sensorValue = 0;  // variable to store the value coming from the sensor
float voltage = 0;

void setup() {
  // declare the ledPin as an OUTPUT:
  Serial.begin(9600); 
}

void loop() {
  // read the value from the sensor:
  sensorValue = analogRead(sensorPin);    
  voltage = sensorValue * (5.0 / 1024.0);
  Serial.println(voltage);
  delay(100); 
}
