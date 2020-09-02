#ifndef Stirrer_h
#define Stirrer_h

  #include <Arduino.h>
  #include "DRV8825.h"
 // #include <DueTimer.h>

  #define STR_V_DIR  39 //38  //39 
  #define STR_V_STEP 37 //52 //37 
  #define STR_V_MOTOR_STEPS 200
  #define STR_V_MICROSTEPS 16
  #define STR_V_RPM 200
  #define STR_V_LSU 33
  #define STR_V_LSB 35
  
  #define STR_POSITION_A A8
  DRV8825 str_vertical(STR_V_MOTOR_STEPS, STR_V_DIR, STR_V_STEP);
  
  #define STR_VERT_ROTATION 52    //13*4
  #define STR_VERT_SHAKE_ROTATION 6
  
  // Stirrer Mixing Motor defines
  #define STR_M_EN   8
  #define STR_M_IN1  A4
  #define STR_M_IN2  A5
  
  #define STR_M_SPEED 160  // out of 255
  #define STR_MT_SPEED 80
  #define STR_SAUTE_SPEED 150  
  #define STR_SHAKE_SPEED 254
  #define STR_ONE_MIX_TIME 2100

  #define mixCW(){\
    digitalWrite(STR_M_IN1, HIGH);\
    digitalWrite(STR_M_IN2, LOW);\
  }
  #define  mixCCW(){\
    digitalWrite(STR_M_IN1, LOW);\
    digitalWrite(STR_M_IN2, HIGH);\
  }
  #define mixBreak(){\
    digitalWrite(STR_M_IN1, HIGH);\
    digitalWrite(STR_M_IN2, HIGH);\
  }
  #define setMixSpeed(SPEED) analogWrite(STR_M_EN,SPEED)

  volatile unsigned char mixingDirFlag; //0- no rotation // 1- clock wise // 2- counter clock wise 
  volatile unsigned char strPosFlag;  //0 - stirrer at top rest pos //1 - stirrer at mixing pos

//  void stirrerTimerISR(){
//      mixBreak(); 
//      if(mixingDirFlag==1) {
//        mixCCW(); 
//        mixingDirFlag = 2; //counter clockwise 
//      }
//      else if(mixingDirFlag == 2){
//        mixCW();
//        mixingDirFlag = 1; //clockwise
//      }       
//}

  class Stirrer {
  
    private:
        void OneMix() {
            mixCW();
            delay(STR_ONE_MIX_TIME);
            mixBreak(); 
            //Serial.println("Reversing Mixing Direction");
            delay(100) ;  
            mixCCW();
            delay(STR_ONE_MIX_TIME);
            mixBreak(); 
        }      

       void align() {
            double Time, target; 
            setMixSpeed(STR_M_SPEED/2);
            delay(50); 
            mixCW(); 
            delay(500);  
            Serial.println("STARTING VALUE OF POSITION");
            Serial.println(analogRead(STR_POSITION_A));
            /*while(1)
            {
              Serial.println(analogRead(STR_POSITION_A));
            }*/
            while(analogRead(STR_POSITION_A)<600) 
               {
                //Serial.println(STR_POSITION_A);
               }
            Serial.println("stirrer blade aligned"); 
            Serial.flush(); 
            //delay(50);  
            mixBreak(); 
            delay(200); 
            setMixSpeed(STR_M_SPEED);
        }      

       void shakeMix() {
          mixCW();
          delay(200); 
          mixBreak(); 
          delay(20); 
          mixCCW();
          delay(200); 
          mixBreak(); 
        }

  
    public:
      void verticalRestPosition() {
          int i; 
           Serial.println("Moving to rest position"); 
           Serial.flush(); 
           if(digitalRead(STR_V_LSU)){
               // move to lowest position for aligning 
               str_vertical.startRotate(-360*40) ; 
               while(digitalRead(STR_V_LSB)) {
                 str_vertical.nextAction();
               }
               str_vertical.stop();
               align() ; 
           }
           delay(100);
           //str_vertical.rotate(360*5) ; 
           str_vertical.startRotate(360*40) ; // 100 rotation for mode 1, 200 steps per rotation 
           while(digitalRead(STR_V_LSU)) {
           str_vertical.nextAction();
          }
          str_vertical.stop(); 
          delay(100);
          strPosFlag=0; 
          Serial.println("Moved stirrer to verticle rest position"); 
          Serial.flush(); 
          //str_vertical.disable(); 
          //delay(100);
        }
        
        void verticalMixingPosition(){
          byte i; 
          strPosFlag=1;
          //str_vertical.enable(); 
          //mixCW();
          for(i=0; i < STR_VERT_ROTATION ; i++){
            str_vertical.move(-50*16);
          } 
          str_vertical.stop(); 
          delay(100);
          //mixCW();
          //delay(100);
        }
        
        // Stirrer subassembly functions 
           

        
        void saute(unsigned char durationSec) {
           int i,j,k; 
           
           // increase mixer speed to max for clearing 
           
           for(k=0; k<durationSec; k++) {
              setMixSpeed(STR_SHAKE_SPEED);
              for(i=0; i< STR_VERT_SHAKE_ROTATION; i++) {
                //str_vertical.rotate(-360);
                str_vertical.move(-50*16);
                shakeMix();
              }
              setMixSpeed(STR_SAUTE_SPEED);
              OneMix(); 
              for(j=0;j<2;j++) { 
              OneMix(); 
              for(i=0; i< (STR_VERT_SHAKE_ROTATION/2); i++) {
                str_vertical.move(50*16);
                 }
              }
           }
        }
        void mixFirst() {
           int i,j,k; 
           Serial.println("break the hill");
           Serial.flush(); 
           // increase mixer speed to max for clearing
           OneMix();
           for(i=0; i< (STR_VERT_SHAKE_ROTATION)/2; i++) {
              str_vertical.move(-50*16);
              //str_vertical.rotate(-360);
           }
           OneMix();
           for(i=0; i< (STR_VERT_SHAKE_ROTATION)/2; i++) {
              //str_vertical.rotate(360);
              str_vertical.move(50*16);
           }   
           
        }        

      void mix(unsigned char durationSec) {
         int i,j,k; 
         Serial.println("Start mixing");
         Serial.flush(); 
         // increase mixer speed to max for clearing 
         
         for(k=0; k<durationSec; k++) {
            // get down one step
            setMixSpeed(STR_SHAKE_SPEED); 
           
            for(i=0; i< (STR_VERT_SHAKE_ROTATION)/2; i++) {
            //str_vertical.rotate(-360);
            str_vertical.move(-50*16);
            shakeMix();
            }
            setMixSpeed(STR_SAUTE_SPEED);
            // mix
            OneMix();
            // get to the bottom of the pan
            for(i=0; i< (STR_VERT_SHAKE_ROTATION)/2; i++) {
            //str_vertical.rotate(-360);
            str_vertical.move(-50*16);
            }
            // mix twice
            OneMix(); 
            OneMix();
            // come up mixing     
            for(i=0; i< (STR_VERT_SHAKE_ROTATION); i++) {
              //str_vertical.rotate(360);
              str_vertical.move(50*16);
            } 
            OneMix(); 
         }
      }      

     void stirrerVegDispensingPos() {
       double Time, target; 
            setMixSpeed(STR_M_SPEED/2);
            delay(50); 
            mixCW(); 
            delay(500);  
            //Serial.println("STARTING VALUE OF POSITION");
            //Serial.println(analogRead(STR_POSITION_A));
            /*while(1)
            {
              Serial.println(analogRead(STR_POSITION_A));
            }*/
            while(analogRead(STR_POSITION_A)<600) 
               {
                //Serial.println(STR_POSITION_A);
               }
            Serial.println("stirrer blade set for mix through"); 
            Serial.flush(); 
            //delay(50);  
            mixBreak(); 
            delay(200); 
            setMixSpeed(STR_MT_SPEED);

      
     }

      void mix_through_start() {
//
         /*if(strPosFlag==0){
          verticalMixingPosition(); 
         }*/
         stirrerVegDispensingPos(); 
         Serial.println("Starting the mix through");
         Serial.flush();          
         setMixSpeed(STR_MT_SPEED);
//         
         //delay(300); 
//         
//         Timer3.start(STR_ONE_MIX_TIME); 
         mixCW();
         mixingDirFlag = 1; //clockwise 
//         
      }

      void mix_through_stop() {
//
         Serial.println("Stop the mix through");
         Serial.flush();          
         mixBreak(); 
         setMixSpeed(STR_SAUTE_SPEED);     
//         Timer3.stop(); 
         mixingDirFlag = 0; //clockwise 
//         delay(300); 
         stirrerVegDispensingPos();
//         verticalMixingPosition();  // function needs to change to track the current position 
//       
//         
      }

        
        void stirrerSetup(){
        
           
           Serial.println("Stirrer setup"); 
           Serial.flush();
           //align();
           // setup stirrer vertical motor
           str_vertical.begin(STR_V_RPM,STR_V_MICROSTEPS);
           str_vertical.setRPM(STR_V_RPM); 
          
           pinMode(STR_V_LSU,INPUT_PULLUP); 
           pinMode(STR_V_LSB,INPUT_PULLUP);  
        
           // setup stirrer mixing motor
           pinMode(STR_M_EN,OUTPUT); 
           pinMode(STR_M_IN1,OUTPUT);
           pinMode(STR_M_IN2,OUTPUT);

           // goto top most position for reference
           Serial.println("configuration done, moving to zero"); 
           Serial.flush();

           //setMixSpeed(STR_M_SPEED); 
           //mixBreak();

           
           verticalRestPosition(); 
           Serial.println("Stirrer at topmost position"); 
           Serial.flush(); 

           //align(); 

           // setup stirrer position detection 
            mixingDirFlag = 0 ; 
           // Timer3.attachInterrupt(stirrerTimerISR);
           // setup temparature sensor 
          
        }

      
  
  };
  Stirrer Stirrer;

#endif
