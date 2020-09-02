#ifndef Spice_h
#define Spice_h

  #include <Arduino.h>
  #include "DRV8825.h"
  #include <Servo.h>
  
  
  // Spice SEL Motor defines
  #define SPC_SEL_DIR 38  //39 
  #define SPC_SEL_STEP 52 //37,52 
  #define SPC_SEL_MOTOR_STEPS 200
  #define SPC_SEL_MICROSTEPS 32
  #define SPC_SEL_RPM 60
  #define SPC_SEL_SENSE A10
  
  DRV8825 spc_sel(SPC_SEL_MOTOR_STEPS, SPC_SEL_DIR, SPC_SEL_STEP);
  
  #define SPC_SEL_GEAR_RATIO 6.300  
  #define SPC_SEL_DIFF_STEPS (60 * SPC_SEL_GEAR_RATIO)
  //#define SPC_SEL_DIFF_STEPS 101
  #define SHAKE_ROTATION (10* SPC_SEL_GEAR_RATIO)
  #define OFFSET (44* SPC_SEL_GEAR_RATIO)
  
  #define WHITE_SENSE_THRESHOLD 120
  
  // for Spice trigger servos
  #define SPC_SERVO_PWM 2 
  #define ANGLEZERO 180  //0.5 ms
  #define ANGLEFULL -180    // 2.3 ms

  // defines for chimney motor 
  //#define CHIMNEY_FAULT_L0 48
  //#define CHIMNEY_FAULT_L1 49
  #define EXHAUST_IN1 50
  #define EXHAUST_IN2 51
  #define EXHAUST_EN  4

  #define EXHAUST_SPEED 255
  
  
   #define EXHAUST_ON(){\
    digitalWrite(EXHAUST_IN1, HIGH);\
    digitalWrite(EXHAUST_IN2, LOW);\
    }

  #define EXHAUST_OFF(){\
    digitalWrite(EXHAUST_IN1, LOW);\
    digitalWrite(EXHAUST_IN2, LOW);\
    }
  #define setFanSpeed(SPEED) analogWrite(EXHAUST_EN,SPEED)
  
  Servo spiceServo;


  class Spice {
  
    private:
      int spiceSelPos; 
      
      void selectSpices(unsigned char pos){   // correct for the middle position
        int numRotation ;
        Serial.println("moving to rotary motor to :"+ String(pos)); 
        Serial.flush(); 
      
        if(spiceSelPos==(-1)) {
          spc_sel.rotate(OFFSET);
          spiceSelPos = 0; 
        }
       
        int toMove = pos - spiceSelPos ;  
        Serial.println("spc_sel position :" + String(spiceSelPos)); 
        
        numRotation =  (toMove * SPC_SEL_DIFF_STEPS) ; // correcting rotation dir by multiplying by -1, DIFF_STEP correspond to 60 degrees, correctin 30 degree offset 
        spc_sel.rotate(numRotation);
        spiceSelPos = pos ; 
        Serial.println("Rotated to: " + String(spiceSelPos));
        delay(1000);
  
      }

      void shakeSpices() {
        //double numRotation = SHAKE_ROTATION; 
        int i; 
        spc_sel.enable(); 
        delay(100); 
        for(i=0; i<3; i++)
        {
            spc_sel.move(SHAKE_ROTATION * SPC_SEL_MICROSTEPS);
            delay(1); 
            spc_sel.move(-1 * SHAKE_ROTATION * SPC_SEL_MICROSTEPS);
          }
      }
  
     void dispense() {
       int i;
       spiceServo.write(ANGLEFULL); 
       delay(1500);  // decrease this if cumin dispensing is more
       spiceServo.write(ANGLEZERO); 
       Serial.println("Dispensing done"); 
       //delay(2000);
       EXHAUST_ON();       
     }

   public:

       void spiceSetup(){
    
         Serial.println("Spice setup"); 
         Serial.flush();
         // setup stirrer vertical motor
         spc_sel.begin(SPC_SEL_RPM,SPC_SEL_MICROSTEPS); 
         spc_sel.setRPM(SPC_SEL_RPM); 
        
         pinMode(SPC_SEL_SENSE,INPUT); 
      
         //setup spice dispense servo 
         spiceServo.attach(SPC_SERVO_PWM); 
         spiceServo.write(ANGLEZERO); 
         delay(800);
        // spiceServo.write(ANGLEZERO); 
         //while(1);
       
         //spiceServo.write(ANGLEFULL);     
         //dispense_spice(); 
      
         // goto top most position for reference
         Serial.println("configuration done, moving to zero"); 
         Serial.flush();
         
         spiceSelRest(); 
         Serial.println("Spice plate at zero"); 
         Serial.flush(); 
         delay(400); 
           
      }
    
      void dispenseSpice(int pos) {
        selectSpices(pos);
        EXHAUST_OFF();
        delay(2000);
        dispense(); 
        
      }
  
      void spiceSelRest() {
       int i; 
       Serial.println("Moving to rest position"); 
       Serial.flush(); 
       //spc_sel.setRPM(120);
       //spc_sel.rotate(360*5) ; 
       spc_sel.startRotate(-360*2*SPC_SEL_GEAR_RATIO) ; // 100 rotation for mode 1, 200 steps per rotation 
       while(analogRead(SPC_SEL_SENSE)> WHITE_SENSE_THRESHOLD) {
       //spc_sel.nextAction();
       spc_sel.rotate(-5);
       Serial.println(analogRead(SPC_SEL_SENSE)); 
      }
      spc_sel.stop(); 
      delay(100); 
      spiceSelPos=-1; 
      //spc_sel.setRPM(SPC_SEL_RPM);
      //spc_sel.disable(); 
      //delay(100);
    }

    /* void spiceRest() {
      spc_sel.startRotate(-360*2*SPC_SEL_GEAR_RATIO);
        while(analogRead(SPC_SEL_SENSE)> WHITE_SENSE_THRESHOLD) {
       //spc_sel.nextAction();
       //spc_sel.step(10);
       spc_sel.rotate(-5);
       Serial.println(analogRead(SPC_SEL_SENSE)); 
      }
      spc_sel.stop(); 
      delay(100); 
      spiceSelPos=-1;
     }*/


    
  };
  Spice Spice;  

  class Chimney {
   
   public: 
      void chimneySetup(){
        Serial.println("setting up the chimney"); 

         //pinMode(CHIMNEY_FAULT_L0,OUTPUT);
         //pinMode(CHIMNEY_FAULT_L1,OUTPUT);         
         pinMode(EXHAUST_EN,OUTPUT); 
         pinMode(EXHAUST_IN1,OUTPUT);
         pinMode(EXHAUST_IN2,OUTPUT);
 
        // digitalWrite(EXHAUST_EN,HIGH);
         //digitalWrite(CHIMNEY_FAULT_L0,HIGH);
         //digitalWrite(CHIMNEY_FAULT_L1,HIGH);
         digitalWrite(EXHAUST_IN1,LOW);
         digitalWrite(EXHAUST_IN2,LOW);
         
      
         setFanSpeed(EXHAUST_SPEED);
         EXHAUST_OFF();
         delay(250); 
         //EXHAUST_ON();

        Serial.println("Cimney setup complete");
        Serial.flush();           

      }


      void chimneyOn() {
         EXHAUST_ON(); 
         delay(500);
         Serial.println("Chimney is on");
         Serial.flush();         
      }


      void chimneyOff() {
          EXHAUST_OFF(); 
          delay(500); 
      }
    
  }; 
  Chimney Chimney; 
  

#endif
