/*
  Blink
  Turns on an LED on for one second, then off for one second, repeatedly.
 
  This example code is in the public domain.
 */
 
// Pin 13 has an LED connected on most Arduino boards.
// give it a name:
int S0=0;
int S1=1;
int S2=2;

int Y0=3;
int Y1=4;
int Y2=5;

// the setup routine runs once when you press reset:
void setup() {                
  // initialize the digital pin as an output.
  pinMode(S0, OUTPUT);
  pinMode(S1, OUTPUT);
  pinMode(S2, OUTPUT);  
  digitalWrite(S0,LOW);
  digitalWrite(S1,LOW);
  digitalWrite(S2,LOW);
  pinMode(Y0, OUTPUT);
  pinMode(Y1, OUTPUT);
  pinMode(Y2, OUTPUT);  
  digitalWrite(Y0,HIGH);
  digitalWrite(Y1,HIGH);
  digitalWrite(Y2,HIGH);

}

// the loop routine runs over and over again forever:
void loop() {
  
  int y=0;
  while (y <  3){
    row_switch(y);
    
    int x=0;
    while (x < 3){ 
      column_switch(x);
      delay(1000);               // wait for a second
      x=x+1;
    }//end x
    
    y = y + 1;
  }//end y
  
}//end loop

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
  Serial.print("x = ");Serial.println(column_number);

}//end column switch 
    
void row_switch(int row_number){
  /*case statement that turns the given column number on based on the 8:1 mux*/
  switch (row_number) {
    case 0:
      digitalWrite(Y0,LOW);
      digitalWrite(Y1,HIGH);
      digitalWrite(Y2,HIGH);
      break;
    case 1:
      digitalWrite(Y0,HIGH);
      digitalWrite(Y1,LOW);
      digitalWrite(Y2,HIGH);
      break;
    case 2:
      digitalWrite(Y0,HIGH);
      digitalWrite(Y1,HIGH);
      digitalWrite(Y2,LOW);
      break;
  }//end switch
}//end row switch
    
