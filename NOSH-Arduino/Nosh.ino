/*************************************************************************************************************************************
// Description : Main Code Look like prototype
// Author  : Yatin 
// ToDo 
// 1.   
**************************************************************************************************************************************/


#include <Arduino.h>
#include <Wire.h>

#include "TempSensor.h"
#include "Stirrer.h"
#include "Spice.h"
#include "Ingredient.h"
#include "OilWaterStove.h"

//list of commands
//commands = {'dispense':0x07,'sleep':0x08,'mix_first':0x09, 'on': 0x0c, 'off':0x0d, 'setLevel':0x0e, 'oil':0x0f, 'water':0x0a, 'saute':0x0b, 'mix_through_start':0x0e, 'mix_through_stop':0x0f, 'crush':0x10, 'temp':0x11}

#define INGREDIENT_DISPENSE  0x01   //post 
#define INGREDIENT_REST      0x02   
#define SPICE_DISPENSE       0x03  //post
#define SPICE_REST           0x04
#define INPUT_INGREDIENT     0x15

#define DISPENSE_WATER       0x05  //post    
#define DISPENSE_OIL         0x06  //post
#define STOVE_ON             0x07  
#define STOVE_OFF            0x08  
#define STOVE_LEVEL          0x09 //post
#define STOVE_TEMP           0x0a //post

#define STIR_POSITION        0x0b
#define STIR_REST            0x0c
#define SAUTE                0x0d //post
#define MIX                  0x0e //post
#define MIX_FIRST            0x0f 
#define MIX_THROUGH_START    0x10
#define MIX_THROUGH_STOP     0x11
#define MIX_CRUSH            0x12 //post

#define NO_COMMAND           0xff 
#define BLINK                digitalWrite(13,!digitalRead(13)); delay(500) 

volatile boolean waitBoxNo = false ; 
volatile int command =  NO_COMMAND; 
volatile int boxNumber ; 

void receiveEvent(int howMany) {
  while (Wire.available()) { // loop through all but the last
    unsigned char c = Wire.read(); // receive byte as a character
    Serial.println("I2C data"); 
    Serial.println(c); 
    if(!waitBoxNo) {
      if((c == INGREDIENT_DISPENSE)|| (c == SPICE_DISPENSE)|| (c == DISPENSE_WATER) || (c == DISPENSE_OIL) || (c == STOVE_LEVEL)||(c == STOVE_TEMP) || (c == SAUTE) ||(c == MIX) || (c == MIX_CRUSH)|| (c == MIX_FIRST))
        /*if((c == INGREDIENT_DISPENSE)|| (c == DISPENSE_WATER) || (c == DISPENSE_OIL) || (c == STOVE_LEVEL)||(c == STOVE_TEMP) || (c == SAUTE) ||(c == MIX) || (c == MIX_CRUSH)|| (c == MIX_FIRST))*/{ 
              waitBoxNo=true; 
              command= c; 
      } 
       else  {
              //Serial.println("Not a two stage command"); 
              command = c;      
              waitBoxNo = false ; 
              if(Wire.available()) c = Wire.read();     
        }
    }    
    else if(waitBoxNo) {
       waitBoxNo = false ;
       boxNumber = c ;  
    }
    //Serial.print("waitboxno:");Serial.println(waitBoxNo);
    //Serial.print("Command:");Serial.println(command);         // print the character
  }
  //Serial.println("I2C data done");   
}

void sendEvent(){
  //Wire.write(TempSensor.TempRead());
  if(digitalRead(23)==0)
  {
    Wire.write(0x01);
  }
  Wire.write(0x02);
}


void setup() {
  int i,j; 
  
  Serial.begin(115200); 
  Serial.println("Star of the code");  
  Serial.flush();  

  Wire.begin(0x54);// join i2c bus with address # using sda and scl
  Wire1.begin();// join i2c bus with address # using sda1 and scl1
  Wire.onReceive(receiveEvent); // register event
  Wire.onRequest(sendEvent);  //Event for sending Temp on request
  interrupts(); 
  Serial.println("Setting up the spice");  
  Serial.flush();  

  Spice.spiceSetup(); 
  Serial.println("Spice setup done");  
  Serial.flush();


  Serial.println("setting up the ingredient plate");  
  Serial.flush();
  Ingredient.ingredientSetup();
  Serial.println("setting up the stirrer");  
  Serial.flush(); 
  Stirrer.stirrerSetup(); 
  Serial.println("stirrer done");  
  Serial.flush();

  //while(1); 
   

  Serial.println("ingredient plate setup done");  
  Serial.flush();  
  
  Stove.stoveSetup();
  Liquid.liquidSetup(); 
  Chimney.chimneySetup();
  TempSensor.TempSetup(); 
  
  Serial.println("turning on the chimney");  
  Serial.flush(); 
  Chimney.chimneyOn();
  

  
  Serial.println("stir position");  
  Serial.flush();

  //Stirrer.verticalMixingPosition(); 
  //Stirrer.saute(1);

  //Serial.println("dispensing the ingredients");  
  //Serial.flush();
     
  //Ingredient.dispense(1);
  // Stirrer.verticalRestPosition(); 
  //Ingredient.movePlatformFrnt();

  //Serial.println("dispensing spices");  
  //Serial.flush();

//  Spice.dispenseSpice(0); 
//  delay(2000); 
//  Spice.dispenseSpice(5); 
//  delay(2000); 
  //Stove.stoveStart(); 
  //
  //  delay(5000); 
  //  Stove.setStoveHeatLevel(1); 
  //
  //  delay(5000); 
  //  Stove.setStoveHeatLevel(6); 
  //
  //  delay(5000); 
  //  Stove.stoveStop(); 
  //  
 
 
}

void loop() {

  
   if(!waitBoxNo){
       
     switch (command) {
        case INPUT_INGREDIENT:
            Ingredient.movePlatformFrnt();
            command=NO_COMMAND;
            Serial.println("Command: Input the ingredients: "); Serial.println(boxNumber); Serial.flush();
            break;
        case INGREDIENT_DISPENSE:   
            Ingredient.dispense(boxNumber); 
            command = NO_COMMAND; 
            Serial.print("Commad: Ingredient dispesne: "); Serial.println(boxNumber); Serial.flush();  
            break; 
        case INGREDIENT_REST:     
            Ingredient.movePlatformBack(); 
            command = NO_COMMAND; 
            Serial.println("Commad: Ingredient rest"); Serial.flush();              
            break;            
        case SPICE_DISPENSE :
            Spice.dispenseSpice(boxNumber); 
            command = NO_COMMAND; 
            Serial.println("Commad: spice dispense"); Serial.flush();               
            break; 
        case SPICE_REST     :     
            Spice.spiceSelRest();    
            command = NO_COMMAND; 
            Serial.println("Commad: spice rest"); Serial.flush();            
            break;       
        case  DISPENSE_WATER :
             Liquid.waterDispense(boxNumber); 
            command = NO_COMMAND; 
            Serial.println("Commad: water dispense"); Serial.flush();                
            break;         
        case DISPENSE_OIL    :
            Liquid.oilDispense(boxNumber); 
            command = NO_COMMAND; 
            Serial.println("Commad: oil dispense"); Serial.flush();                
            break;         
        case  STOVE_ON       :  
            Stove.stoveStart();
            command = NO_COMMAND; 
            Serial.println("Commad: stove on"); Serial.flush();                
            break;         
        case  STOVE_OFF      : 
            Stove.stoveStop(); 
            command = NO_COMMAND; 
            Serial.println("Commad: spice off"); Serial.flush();                
            break;         
        case  STOVE_LEVEL    :
             Stove.setStoveHeatLevel(boxNumber); 
            command = NO_COMMAND; 
            Serial.println("Commad: stove level"); Serial.flush();                
            break;         
        case STOVE_TEMP      :        
            //Stove.temp(boxNumber); 
            command = NO_COMMAND; 
            Serial.println("Commad: stove temp"); Serial.flush();             
            break;        
        case STIR_POSITION      :        
            Stirrer.verticalMixingPosition(); 
            command = NO_COMMAND; 
            Serial.println("Commad: stir position"); Serial.flush();             
            break; 
        case STIR_REST      :        
            Stirrer.verticalRestPosition(); 
            command = NO_COMMAND; 
            Serial.println("Commad: stir rest"); Serial.flush();             
            break;        
        case  SAUTE          :    
            Stirrer.saute(boxNumber);   
            command = NO_COMMAND; 
            Serial.println("Commad: saute"); Serial.flush();             
            break;         
        case  MIX            :    
            Stirrer.mix(boxNumber); 
            Serial.println("Commad: mix"); Serial.flush();             
            command = NO_COMMAND; 
            break;         
        case  MIX_FIRST      :   
            Stirrer.mixFirst();   
            command = NO_COMMAND; 
            Serial.println("Commad: mix first"); Serial.flush();             
            break;         
        case  MIX_THROUGH_START :  
            Stirrer.mix_through_start();   
            command = NO_COMMAND; 
            Serial.println("Commad: mix through start"); Serial.flush();             
            break;         
        case  MIX_THROUGH_STOP  :  
            Stirrer.mix_through_stop();  
            command = NO_COMMAND; 
            Serial.println("Commad: mix through stop"); Serial.flush();             
            break;         
        case MIX_CRUSH          :  
            //Stirrer.mixCrush();  
            command = NO_COMMAND; 
            Serial.println("Commad: mix crush"); Serial.flush();             
            break;  
        default: 
            break;        
      }
   }

}
