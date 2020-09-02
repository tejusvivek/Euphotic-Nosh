#ifndef OilWaterStove_h
#define OilWaterStove_h

// connections Red-black : On//k1 
//           grey-white : Manual //k2
//         blue-violate: Plus//k3
//        yellow-green: minus //k4
// Liquid pins 

#define WATER_IN1 16
#define WATER_IN2 17
#define WATER_EN  6

#define OIL_IN1 18
#define OIL_IN2 19
#define OIL_EN  7

// stove Pins
#define ON_OFF_C 9 //k1 
#define MANUAL   14 //k2
#define TEMP_P   15 //K3
#define TEMP_N   28 //K4 

#define ON_TIME 400 //ms 
#define TEMP_TIME 400 //ms
#define OFF_TIME 800

#define OIL_SPEED 255
#define WATER_SPEED 255 

 #define WATER_FWD(){\
    digitalWrite(WATER_IN1, HIGH);\
    digitalWrite(WATER_IN2, LOW);\
  }

  #define WATER_STOP(){\
    digitalWrite(WATER_IN1, LOW);\
    digitalWrite(WATER_IN2, LOW);\
  }


 #define OIL_FWD(){\
    digitalWrite(OIL_IN1, HIGH);\
    digitalWrite(OIL_IN2, LOW);\
  }

  #define OIL_STOP(){\
    digitalWrite(OIL_IN1, LOW);\
    digitalWrite(OIL_IN2, LOW);\
  }

#define setWaterSpeed(SPEED) analogWrite(WATER_EN,SPEED)
#define setOilSpeed(SPEED)   analogWrite(OIL_EN,SPEED)

#include <Arduino.h>


  class Liquid {
  
    private:

    public: 
    void oilDispense(int amountML) {
        Serial.println("Starting dispensing oil"); 
        OIL_FWD(); 
        for(int i=1; i <= amountML/5 ; i++) {
            //  delay((OIL_RATIO_1ML)*amountML); // 1ml/sec
          delay(400); // 1ml/sec
        }
        OIL_STOP();
        Serial.println("Dispensed oil");
        Serial.flush();
    }
    
    void waterDispense(int amountML) {
        //Serial.println("Starting  dispensing water"); 
        WATER_FWD(); 
        for(int i=1; i <= (amountML/10) ; i++) {
          
        delay(315); // 1ml/sec
        //Serial.println("Dispensing oil");
        }
        //delay(40000); 
        WATER_STOP();
        Serial.println("Dispensed water");
        Serial.flush(); 
        
    }

    void liquidSetup(){

         pinMode(WATER_EN,OUTPUT); 
         pinMode(WATER_IN1,OUTPUT);
         pinMode(WATER_IN2,OUTPUT);
      
         setWaterSpeed(WATER_SPEED); 

         pinMode(OIL_EN,OUTPUT); 
         pinMode(OIL_IN1,OUTPUT);
         pinMode(OIL_IN2,OUTPUT);
      
         setOilSpeed(OIL_SPEED);  
    }
    
  };
  Liquid Liquid; 


   class Stove {
  
    private:
      volatile boolean stoveStatus = false ; // false == OFF, true == ON 
      volatile unsigned char heatLevel; 


    public: 

    void stoveStart() {
      Serial.println("Starting the stove") ; 
      Serial.flush();
      
       if(stoveStatus == false) 
       {  
          delay(200); 
          digitalWrite(ON_OFF_C,LOW) ;  
          delay(ON_TIME);
          digitalWrite(ON_OFF_C,HIGH) ;  
          
          delay(2600); 
          digitalWrite(MANUAL,LOW) ;  
          delay(180);
          digitalWrite(MANUAL,HIGH) ;  
          Serial.println("ON") ; 
          Serial.flush();
          delay(100);  
          heatLevel = 4 ;
          stoveStatus = true ; 
          
       }
       else Serial.println("Already ON") ;
      
    }
    
    void stoveStop() {
       if(stoveStatus == true) 
       {  
          digitalWrite(ON_OFF_C,LOW) ;  
          delay(OFF_TIME);
          digitalWrite(ON_OFF_C,HIGH) ;  
          Serial.println("OFF") ; 
          Serial.flush(); 
          heatLevel = 0 ;
          stoveStatus = false ; 
       }
       else Serial.println("Already OFF") ;
      
    }
    
    void setStoveHeatLevel(unsigned char endLevel) {
       if(stoveStatus == true) 
       {  
          int diff, i ; 
          diff = endLevel - heatLevel ; 
          if(diff > 0) { 
            for(i=0; i < diff; i++) {
              digitalWrite(TEMP_P,LOW) ;  
              delay(TEMP_TIME);
              digitalWrite(TEMP_P,HIGH) ;  
              heatLevel++; 
              delay(500);
            }
          }
          else if(diff < 0) {
            for(i=0; i < abs(diff); i++) {
              digitalWrite(TEMP_N,LOW) ;  
              delay(TEMP_TIME);
              digitalWrite(TEMP_N,HIGH) ;  
              heatLevel--; 
              delay(500);
            }
          }
       }
       else Serial.println("Already OFF") ;
    }

    void stoveSetup() {
        
      pinMode(ON_OFF_C,OUTPUT); 
      digitalWrite(ON_OFF_C,HIGH); 
    
      pinMode(MANUAL,OUTPUT); 
      digitalWrite(MANUAL,HIGH); 
    
      pinMode(TEMP_P,OUTPUT); 
      digitalWrite(TEMP_P,HIGH);
    
       pinMode(TEMP_N,OUTPUT); 
      digitalWrite(TEMP_N,HIGH);
  
      stoveStatus = false ; 
      heatLevel = 0 ; 
     
   }

  };
  Stove Stove;

#endif 
