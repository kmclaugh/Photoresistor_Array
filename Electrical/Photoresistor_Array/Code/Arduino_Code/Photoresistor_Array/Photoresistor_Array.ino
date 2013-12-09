//Select Bits
int S0=2;
int S1=3;
int S2=4;

//Return signals
int Y0 = A0;
int Y1 = A1;
int Y2 = A2;
int Y3 = A3;

//voltages
float voltage0_0=0;float voltage1_0=0;
float voltage0_1=0;float voltage1_1=0;
float voltage0_2=0;float voltage1_2=0;

void setup() {
  Serial.begin(9600);
  pinMode(S0, OUTPUT);
  pinMode(S1, OUTPUT);
  pinMode(S2, OUTPUT);  
  digitalWrite(S0,LOW);
  digitalWrite(S1,LOW);
  digitalWrite(S2,LOW);
  
}//end setup

void loop() {
  // read the values from the diodes:
  //00,10
  voltage0_0 = readVoltage(0, Y0); voltage1_0 = readVoltage(1, Y0);
  //01,11
  voltage0_1 = readVoltage(0, Y1); voltage1_1 = readVoltage(1, Y1);
  //02,12
  voltage0_2 = readVoltage(0, Y2); voltage1_2 = readVoltage(1, Y2);
  // print the voltage values
  Serial.print(voltage0_0);Serial.print(", ");Serial.print(voltage1_0);Serial.println("");
  Serial.print(voltage0_1);Serial.print(", ");Serial.print(voltage1_1);Serial.println("");
  Serial.print(voltage0_2);Serial.print(", ");Serial.print(voltage1_2);Serial.println("");
  Serial.println("");
  
  delay(1000);  
}//end loop

float readVoltage(int x, int y) {
  /* Returns the voltage of the given input and output pin. Sets output back to zero*/
  int sensorValue;
  float voltage;
  column_switch(x);
  delay(10);
  sensorValue = analogRead(y);
  voltage = sensorValue * (5.0 / 1024.0);
  delay(10);
  return(voltage);
}//end readVoltage

void column_switch(int column_number){
  /*case statement that turns the given column number on based on the 8:1 mux*/
  switch (column_number) {
    case 0:
      digitalWrite(S0,LOW);
      digitalWrite(S1,LOW);
      digitalWrite(S2,LOW);
      break;
    case 1:
      digitalWrite(S0,HIGH);
      digitalWrite(S1,LOW);
      digitalWrite(S2,LOW);
      break;
    case 2:
      digitalWrite(S0,LOW);
      digitalWrite(S1,HIGH);
      digitalWrite(S2,LOW);
      break;
    case 3:
      digitalWrite(S0,HIGH);
      digitalWrite(S1,HIGH);
      digitalWrite(S2,LOW);
      break;
    case 4:
      digitalWrite(S0,LOW);
      digitalWrite(S1,LOW);
      digitalWrite(S2,HIGH);
      break;
    case 5:
      digitalWrite(S0,HIGH);
      digitalWrite(S1,LOW);
      digitalWrite(S2,HIGH);
      break;
    case 6:
      digitalWrite(S0,LOW);
      digitalWrite(S1,HIGH);
      digitalWrite(S2,HIGH);
      break;
    case 7:
      digitalWrite(S0,HIGH);
      digitalWrite(S1,HIGH);
      digitalWrite(S2,HIGH);
      break;
  }//end switch

}//end column switch 
