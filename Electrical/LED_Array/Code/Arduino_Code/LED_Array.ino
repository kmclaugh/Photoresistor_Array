
/**********LED Declarations*************************/ 
int LED_S0=0;
int LED_S1=1;
int LED_S2=2;

int LED_Y0=3;
int LED_Y1=4;
int LED_Y2=5;
/**********END LED Declarations*************************/ 

void setup() {      
  
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

}

// the loop routine runs over and over again forever:
void loop() {
  
  int y=0;
  while (y <  3){
    LED_row_switch(y);
    
    int x=0;
    while (x < 3){ 
      LED_column_switch(x);
      delay(1000);               // wait for a second
      x=x+1;
    }//end x
    
    y = y + 1;
  }//end y
  
}//end loop


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
  Serial.print("x = ");Serial.println(column_number);

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
    
