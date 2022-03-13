//www.elegoo.com
//2016.12.9

/* @file CustomKeypad.pde
|| @version 1.0
|| @author Alexander Brevig
|| @contact alexanderbrevig@gmail.com
||
|| @description
|| | Demonstrates changing the keypad size and key values.
|| #
*/
#include <Keypad.h>

const byte ROWS = 4; //four rows
const byte COLS = 4; //four columns
//define the cymbols on the buttons of the keypads
char hexaKeys[ROWS][COLS] = {
  {'A','D','G','-1'},
  {'J','M','P','0'},
  {'S','V','Y','0'},
  {'*',' ','\n','0'}
  /*
  {'ABC','DEF','GHI',''},
  {'JKL','MNO','PQR',''},
  {'STU','VWX','YZbackspace',''},
  {'select word','space','enter/new line',''}*/
};
byte rowPins[ROWS] = {9, 8, 7, 6}; //connect to the row pinouts of the keypad
byte colPins[COLS] = {5, 4, 3, 2}; //connect to the column pinouts of the keypad

int count=-1;
char lastKey = 0;
String result;
//initialize an instance of class NewKeypad
Keypad customKeypad = Keypad( makeKeymap(hexaKeys), rowPins, colPins, ROWS, COLS); 

void setup(){
  Serial.begin(9600);
}
  
void loop(){
  char customKey = customKeypad.getKey();
  /*Serial.print("key, count: ");
    Serial.print(count);
    Serial.print(" ");
    Serial.print(lastKey);
    Serial.print("\n");*/
  Serial.println(result);

  if (customKey)
  {  
    if(customKey=='*')
    {   
      result += (char)(lastKey+count);    
      count=-1;
    }
    else if(customKey==' ')
    {   
      result += " ";
      count=-1;
    }  
    else if(customKey=='\n')
    {   
      result += "\n";
      count=-1;
    }  
    else if(lastKey==customKey)
    {
      count++;
      if(count>=3)
        count=0;
    }
    else if(lastKey!=customKey)
    {
      lastKey=customKey;
      count=0;
    }
  }
}
