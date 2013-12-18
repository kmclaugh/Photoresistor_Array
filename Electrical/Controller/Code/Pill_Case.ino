#include <SoftwareSerial.h> //software serial

#define ARRAY_X 2
#define ARRAY_Y 3
const int TEST_LED = 6;
/*************Electric Imp Declarations*********/
const int EITX_ARX = 3;
const int EIRX_ATX = 2;
SoftwareSerial electricimpSerial(EITX_ARX,EIRX_ATX);
/*************END Electric Imp Declarations*****/

/**************Mux Declarations*****************/
//Select Bits
int S0=7;
int S1=8;
int S2=9;
/************END Mux Delcarations*****************/

/**********LED Declarations*************************/ 
//Y outputs
int LEDY0=10;
int LEDY1=11;
int LEDY2=12;
int LEDY3=13;
/**********END LED Declarations*************************/ 

/*************LDR Declarations******************/
#define LDR_COMPARE_VALUE 1
//Return signals
int LDR_Read0 = A0;
int LDR_Read1 = A1;
int LDR_Read2 = A2;
int LDR_Read3 = A3;
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
  electricimpSerial.begin(19200);    // configure imp serial
  
  //Configure LED Pins
  pinMode(S0, OUTPUT);
  pinMode(S1, OUTPUT);
  pinMode(S2, OUTPUT);  
  digitalWrite(S0,LOW);
  digitalWrite(S1,LOW);
  digitalWrite(S2,LOW);
  
  pinMode(LEDY0, OUTPUT);
  pinMode(LEDY1, OUTPUT);
  pinMode(LEDY2, OUTPUT);  
  digitalWrite(LEDY0,HIGH);
  digitalWrite(LEDY1,HIGH);
  digitalWrite(LEDY2,HIGH);
  
  pinMode(TEST_LED,OUTPUT);
  digitalWrite(TEST_LED,HIGH);
  delay(1000);
  digitalWrite(TEST_LED,LOW);
  
  
}//end setup

void loop() {
  
  //Check the state of all the pill
  if (electricimpSerial.available () > 0) {
    int recieved_data = electricimpSerial.read();
    Serial.println(recieved_data);
    if (recieved_data == 105){
      Serial.println("Pill Check");
      digitalWrite(TEST_LED,HIGH);
      check_all_pills();
      //Print them to the USB-Serial Monitor
      print_pills();  
      //Send the voltage info to the imp
      send_state();
      delay(1000);
      digitalWrite(TEST_LED,LOW);
    }
  }

}//end loop


/****************************************Connection Functions*****************************/
void send_state() {
  /*Sends the states over to the electric imp via UART by bitmasking them to a single int
    and sending them using the Serial.write function*/
  int statex_y;
  int counter = 0;
  int send_number = 0;
  int this_bit;
  for (int y = 0; y < ARRAY_Y; y++){
    for (int x = 0; x < ARRAY_X; x++){
      statex_y = *LDR_states_array[y][x];
      this_bit = statex_y * pow(2,counter)+0.25;
      send_number = send_number + this_bit;
      counter ++;
      }//end x
  }//end y
  //Serial.print(send_number,BIN);Serial.print(" ");Serial.println(send_number);
  Serial.println(send_number);
  electricimpSerial.write(send_number);
  electricimpSerial.write(111);
  delay(10);
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
  column_switch(x);
  LED_row_switch(y);
}//end LED_on
  
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
  
void LED_row_switch(int row_number){
  /*case statement that turns the given column number on based on the 8:1 mux*/
  switch (row_number) {
    case 0:
      digitalWrite(LEDY0,LOW);
      digitalWrite(LEDY1,HIGH);
      digitalWrite(LEDY2,HIGH);
      break;
    case 1:
      digitalWrite(LEDY0,HIGH);
      digitalWrite(LEDY1,LOW);
      digitalWrite(LEDY2,HIGH);
      break;
    case 2:
      digitalWrite(LEDY0,HIGH);
      digitalWrite(LEDY1,HIGH);
      digitalWrite(LEDY2,LOW);
      break;
  }//end switch
}//end row switch

void LED_all_off(){
  /*Turns all the LED rows high, thus turning all LEDs off*/
  digitalWrite(LEDY0,HIGH);
  digitalWrite(LEDY1,HIGH);
  digitalWrite(LEDY2,HIGH);
}//end LED all off
  
/*****************************************END LED Functions************************************/    

/*****************************************LDR Functions***********************************/
float LDR_readVoltage(int x, int y) {
  /* Returns the voltage of the given input and output pin. Sets output back to zero*/
  int sensorValue;
  float voltage;
  column_switch(x);
  delay(10);
  sensorValue = analogRead(y);
  voltage = sensorValue * (5.0 / 1024.0);
  delay(10);
  return(voltage);
}//end LDR_readVoltage

/*****************************************END LDR Functions***********************************/
