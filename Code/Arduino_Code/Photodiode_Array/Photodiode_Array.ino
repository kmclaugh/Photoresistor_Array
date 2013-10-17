//Output bits
int Bit0 = 13;
int Bit1 = 12;
int Bit2 = 11;
//Return signals
int Sig0 = A0;
int Sig1 = A1;

//voltages
float voltage00=0;
float voltage10=0;
float voltage01=0;
float voltage11=0;
float voltage02=0;
float voltage12=0;

void setup() {
  Serial.begin(9600);
  floatPin(Bit0);
  floatPin(Bit1);
  floatPin(Bit2);

}//end setup

void loop() {
  // read the values from the diodes:
  //00,10
  voltage00 = readVoltage(Bit0, Sig0);
  voltage10 = readVoltage(Bit0, Sig1);
  //01,11
  voltage01 = readVoltage(Bit1, Sig0);
  voltage11 = readVoltage(Bit1, Sig1);
  //02,12
  voltage02 = readVoltage(Bit2, Sig0);
  voltage12 = readVoltage(Bit2, Sig1);
  
  // print the voltage values
  Serial.print(voltage00);Serial.print(", ");Serial.print(voltage10);Serial.println("");
  Serial.print(voltage01);Serial.print(", ");Serial.print(voltage11);Serial.println("");
  Serial.print(voltage02);Serial.print(", ");Serial.print(voltage12);Serial.println("");
  Serial.println("");
  
  delay(1000);  
}//end loop

float readVoltage(int bitPin, int signalPin) {
  /* Returns the voltage of the given input and output pin. Sets output back to zero*/
  int sensorValue;
  float voltage;
  pinMode(bitPin, OUTPUT);
  digitalWrite(bitPin,LOW);
  delay(10);
  sensorValue = analogRead(signalPin);
  voltage = sensorValue * (5.0 / 1024.0);
  floatPin(bitPin);
  delay(10);
  return(voltage);
}//end readVoltage

void floatPin(int pinNumber){
 /*Sets the given pin to a floating voltage*/
 pinMode(pinNumber, INPUT);
}//end floatPin
