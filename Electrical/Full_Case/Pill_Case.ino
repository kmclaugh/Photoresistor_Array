#include <SoftwareSerial.h> //software serial

#define ARRAY_X 2
#define ARRAY_Y 3

/*************Electric Imp Declarations*********/
SoftwareSerial electricimpSerial(8,9);
/*************END Electric Imp Declarations*****/

/**********LED Declarations*************************/ 
//Select Bits
int LED_S0=5;
int LED_S1=6;
int LED_S2=7;
//Y outputs
int LED_Y0=10;
int LED_Y1=11;
int LED_Y2=12;
/**********END LED Declarations*************************/ 

/*************LDR Declarations******************/
#define LDR_COMPARE_VALUE 1
//Select Bits
int LDR_S0=2;
int LDR_S1=3;
int LDR_S2=4;
//Return signals
int LDR_Read0 = A0;
int LDR_Read1 = A1;
int LDR_Read2 = A2;
//Read voltages
float voltage0_0=0;float voltage1_0=0;
float voltage0_1=0;float voltage1_1=0;
float voltage0_2=0;float voltage1_2=0;
//Read voltages array
float *voltage_array[][ARRAY_X] = {{&voltage0_0, &voltage1_0},
                            {&voltage0_1, &voltage1_1},
                            {&voltage0_2, &voltage1_2}
                           };
//LDR States
float state0_0=0;float state1_0=0;
float state0_1=0;float state1_1=0;
float state0_2=0;float state1_2=0;
//Read voltages array
//LDR States array
float *LDR_states_array[][ARRAY_X] = {{&state0_0, &state1_0},
                            {&state0_1, &state1_1},
                            {&state0_2, &state1_2}
                           };
/*************END LDR Declarations******************/

void setup() {
  
  //USB-Serial Configure
  Serial.begin(9600);
  Serial.println("Set up");
  //Electric Imp Configure
  electricimpSerial.begin(9600);    // configure imp serial
  
  //Configure LED Pins
  pinMode(LED_S0, OUTPUT);
  pinMode(LED_S1, OUTPUT);
  pinMode(LED_S2, OUTPUT);  
  digitalWrite(LED_S0,LOW);
  digitalWrite(LED_S1,LOW);
  digitalWrite(LED_S2,LOW);
  
  pinMode(LED_Y0, OUTPUT);
  pinMode(LED_Y1, OUTPUT);
  pinMode(LED_Y2, OUTPUT);  
  digitalWrite(LED_Y0,HIGH);
  digitalWrite(LED_Y1,HIGH);
  digitalWrite(LED_Y2,HIGH);
  
  //Configure LDR Pins
  pinMode(LDR_S0, OUTPUT);
  pinMode(LDR_S1, OUTPUT);
  pinMode(LDR_S2, OUTPUT);  
  digitalWrite(LDR_S0,LOW);
  digitalWrite(LDR_S1,LOW);
  digitalWrite(LDR_S2,LOW);
  
}//end setup

void loop() {
  
  //Check the state of all the pill
  Serial.println("Pill Check");
  check_all_pills();
  //Print them to the USB-Serial Monitor
  print_pills();  
  //Send the voltage info to the imp
  send_state();
  
  delay(1000);  
}//end loop


/****************************************Connection Functions*****************************/
void send_state() {
  /*Sends the states over to the electric imp via UART*/
  int statex_y;
  for (int y = 0; y < ARRAY_Y; y++){
    for (int x = 0; x < ARRAY_X; x++){
      statex_y = *LDR_states_array[y][x];
      electricimpSerial.write(statex_y);
      delay(100);
    }//end x
    electricimpSerial.write(100);
    delay(100);
  }//end y
}//end send voltage
/****************************************END Connection Functions*****************************/

/****************************************Check Pills Routines**********************************/
void print_pills(){
  /*Loops the voltages and prints them to the Serial-USB*/
  float voltagex_y;
  int statex_y;
  for (int y = 0; y < ARRAY_Y; y++){
    for (int x = 0; x < ARRAY_X; x++){
      voltagex_y = *voltage_array[y][x];
      statex_y = *LDR_states_array[y][x];
      Serial.print("(");Serial.print(voltagex_y);Serial.print(", ");Serial.print(statex_y);Serial.print("),");
    }//end x
    Serial.println(" ");
  }//end y
}//end print_pills

void check_all_pills(){
  /*Loops through all pills in the array, and checks each one*/
  float voltagex_y;
  int state;
  for (int y = 0; y < ARRAY_Y;y++){
    for (int x = 0; x < ARRAY_X; x++){ 
      //Serial.print("B ");Serial.print(x);Serial.print(", ");Serial.println(y);
      voltagex_y = check_single_pill(x,y);
      *voltage_array[y][x] = voltagex_y;
      if (voltagex_y > LDR_COMPARE_VALUE) {
        state = 1;
      }
      else{
        state = 0;
      }
      *LDR_states_array[y][x] = state;
    }//end x
  }//end y
}//end check_all_pills

float check_single_pill(int x, int y){
  /*Turn the LED and check the LDR voltage for the given x,y value*/
  float voltagex_y;
  LED_on(x,y);
  voltagex_y = LDR_readVoltage(x,y);
  delay(100);  
  LED_all_off();
  return(voltagex_y);
}//end check_single_pill

/****************************************Check Pills Routines**********************************/

/*****************************************LED Functions************************************/
void LED_on(int x, int y){
  /*Turns the LED (x,y) on*/
  //Serial.print("A ");Serial.print(x);Serial.print(", ");Serial.println(y);
  LED_column_switch(x);
  LED_row_switch(y);
}//end LED_on
  
void LED_column_switch(int column_number){
  /*case statement that turns the given column number on based on the 8:1 mux*/
  switch (column_number) {    
    case 0:
      digitalWrite(LED_S0,LOW);
      digitalWrite(LED_S1,LOW);
      digitalWrite(LED_S2,LOW);
      break;
    case 1:
      digitalWrite(LED_S0,HIGH);
      digitalWrite(LED_S1,LOW);
      digitalWrite(LED_S2,LOW);
      break;
    case 2:
      digitalWrite(LED_S0,LOW);
      digitalWrite(LED_S1,HIGH);
      digitalWrite(LED_S2,LOW);
      break;
    case 3:
      digitalWrite(LED_S0,HIGH);
      digitalWrite(LED_S1,HIGH);
      digitalWrite(LED_S2,LOW);
      break;
    case 4:
      digitalWrite(LED_S0,LOW);
      digitalWrite(LED_S1,LOW);
      digitalWrite(LED_S2,HIGH);
      break;
    case 5:
      digitalWrite(LED_S0,HIGH);
      digitalWrite(LED_S1,LOW);
      digitalWrite(LED_S2,HIGH);
      break;
    case 6:
      digitalWrite(LED_S0,LOW);
      digitalWrite(LED_S1,HIGH);
      digitalWrite(LED_S2,HIGH);
      break;
    case 7:
      digitalWrite(LED_S0,HIGH);
      digitalWrite(LED_S1,HIGH);
      digitalWrite(LED_S2,HIGH);
      break;
  }//end switch
}//end column switch 
  
void LED_row_switch(int row_number){
  /*case statement that turns the given column number on based on the 8:1 mux*/
  switch (row_number) {
    case 0:
      digitalWrite(LED_Y0,LOW);
      digitalWrite(LED_Y1,HIGH);
      digitalWrite(LED_Y2,HIGH);
      break;
    case 1:
      digitalWrite(LED_Y0,HIGH);
      digitalWrite(LED_Y1,LOW);
      digitalWrite(LED_Y2,HIGH);
      break;
    case 2:
      digitalWrite(LED_Y0,HIGH);
      digitalWrite(LED_Y1,HIGH);
      digitalWrite(LED_Y2,LOW);
      break;
  }//end switch
}//end row switch

void LED_all_off(){
  /*Turns all the LED rows high, thus turning all LEDs off*/
  digitalWrite(LED_Y0,HIGH);
  digitalWrite(LED_Y1,HIGH);
  digitalWrite(LED_Y2,HIGH);
}//end LED all off
  
/*****************************************END LED Functions************************************/    

/*****************************************LDR Functions***********************************/
float LDR_readVoltage(int x, int y) {
  /* Returns the voltage of the given input and output pin. Sets output back to zero*/
  int sensorValue;
  float voltage;
  LDR_column_switch(x);
  delay(10);
  sensorValue = analogRead(y);
  voltage = sensorValue * (5.0 / 1024.0);
  delay(10);
  return(voltage);
}//end LDR_readVoltage

void LDR_column_switch(int column_number){
  /*case statement that turns the given column number on based on the 8:1 mux*/
  switch (column_number) {
    case 0:
      digitalWrite(LDR_S0,LOW);
      digitalWrite(LDR_S1,LOW);
      digitalWrite(LDR_S2,LOW);
      break;
    case 1:
      digitalWrite(LDR_S0,HIGH);
      digitalWrite(LDR_S1,LOW);
      digitalWrite(LDR_S2,LOW);
      break;
    case 2:
      digitalWrite(LDR_S0,LOW);
      digitalWrite(LDR_S1,HIGH);
      digitalWrite(LDR_S2,LOW);
      break;
    case 3:
      digitalWrite(LDR_S0,HIGH);
      digitalWrite(LDR_S1,HIGH);
      digitalWrite(LDR_S2,LOW);
      break;
    case 4:
      digitalWrite(LDR_S0,LOW);
      digitalWrite(LDR_S1,LOW);
      digitalWrite(LDR_S2,HIGH);
      break;
    case 5:
      digitalWrite(LDR_S0,HIGH);
      digitalWrite(LDR_S1,LOW);
      digitalWrite(LDR_S2,HIGH);
      break;
    case 6:
      digitalWrite(LDR_S0,LOW);
      digitalWrite(LDR_S1,HIGH);
      digitalWrite(LDR_S2,HIGH);
      break;
    case 7:
      digitalWrite(LDR_S0,HIGH);
      digitalWrite(LDR_S1,HIGH);
      digitalWrite(LDR_S2,HIGH);
      break;
  }//end switch

}//end column switch 

/*****************************************END LDR Functions***********************************/
