#ifndef Ingredient_h
#define Ingredient_h

  #include <Arduino.h>
  
  // vegetable Platform Motor defines
  
  #define PLM_EN   3
  #define PLM_IN1  43
  #define PLM_IN2  45
  
  #define PLM_ENCA 31
  #define PLM_ENCB 29
  
  #define PLM_SPEED 255 // out of 255
  #define PLM_BACK_LIMIT 25
  #define PLM_FRNT_LIMIT 23
  
  
  #define PLM_FRWD(){\
    digitalWrite(PLM_IN1, HIGH);\
    digitalWrite(PLM_IN2, LOW);\
  }
  #define  PLM_BKWD(){\
    digitalWrite(PLM_IN1, LOW);\
    digitalWrite(PLM_IN2, HIGH);\
  }
  #define PLM_STP(){\
    digitalWrite(PLM_IN1, HIGH);\
    digitalWrite(PLM_IN2, HIGH);\
  }
  #define setPlatformSpeed(SPEED) analogWrite(PLM_EN,SPEED)
  
  // Vegetable pusher motor defines 
  
  #define PSH_EN   5
  #define PSH_IN1  46
  #define PSH_IN2  44
  
  #define PSH_ENCA 42
  #define PSH_ENCB 40
  
  #define PSH_SPEED 255  // out of 255
  #define PSH_LEFT_LIMIT 26
  #define PSH_RIGHT_LIMIT 28
  
  #define PSH_FRWD(){\
    digitalWrite(PSH_IN1, HIGH);\
    digitalWrite(PSH_IN2, LOW);\
  }
  #define  PSH_BKWD(){\
    digitalWrite(PSH_IN1, LOW);\
    digitalWrite(PSH_IN2, HIGH);\
  }
  #define PSH_STP(){\
    digitalWrite(PSH_IN1, HIGH);\
    digitalWrite(PSH_IN2, HIGH);\
  }
  #define setPusherSpeed(SPEED) analogWrite(PSH_EN,SPEED)
  
  
  // function defines
  
  #define COUNT_PER_ROTATION 3280
  
  #define HIGH_THRESOLD (3*COUNT_PER_ROTATION)
  #define TOLERANCE 20
  
  // for PID
  #define SPEED_PLM_H 255 // out of 255
  #define SPEED_PLM_M 200
  #define SPEED_PLM_S 120 
  
  #define KpPLM (SPEED_PLM_M/(0.04*9840))
  
  
  #define SPEED_PSH_H 255 // out of 255
  #define SPEED_PSH_M 250
  #define SPEED_PSH_S 140 
  
  #define HIGH_THRESOLD_PSH (3*3280)
  #define TOLERANCE_PSH 100
  #define KpPSH (SPEED_PSH_M/(0.5*3280))
  
  
  #define PLATFORM_END (COUNT_PER_ROTATION*15+4500)  
  #define PLATFORM_HOOK_DISPLACEMENT 6150
  
  #define PUSHER_INITIAL_POS 3280*10
 // #define PUSHER_END         3280*133
  #define PUSHER_END         3280*130 

    #define PUSHER_INITIAL_POS 4920*9
    #define PUSHER_END         4920*133 

// globals 
      volatile double encoderPosPSH, encoderPosPLM ; 
      const int QEM[4][4] = {{0,-1,1,2},{1,0,2,-1},{-1,2,0,1},{2,1,-1,0}};               // Quadrature Encoder Matrix
      volatile unsigned char  NewPLM,OldPLM;
      volatile unsigned char  NewPSH,OldPSH;


//ISRs
  
  void enAPLMInterrupt(){
        NewPLM = (digitalRead(PLM_ENCA)<<1)|(digitalRead(PLM_ENCB)); 
        encoderPosPLM+= QEM[OldPLM][NewPLM];
        OldPLM = NewPLM ; 
        //Serial.println("enAPLM"); 
        //delay(3); 
  }
      
  void enBPLMInterrupt(){
    NewPLM = (digitalRead(PLM_ENCA)<<1)|(digitalRead(PLM_ENCB)); 
    encoderPosPLM+= QEM[OldPLM][NewPLM];
    OldPLM = NewPLM ; 
    //Serial.println("enBPLM"); 
    //delay(3); 
  }
  
  void enAPSHInterrupt(){
    NewPSH = (digitalRead(PSH_ENCA)<<1)|(digitalRead(PSH_ENCB)); 
    encoderPosPSH+= QEM[OldPSH][NewPSH];
    OldPSH = NewPSH ; 
    //Serial.println("enAPSH"); 
    //delay(3); 
  }
  
  void enBPSHInterrupt(){
    NewPSH = (digitalRead(PSH_ENCA)<<1)|(digitalRead(PSH_ENCB)); 
    encoderPosPSH+= QEM[OldPSH][NewPSH];
    OldPSH = NewPSH ; 
    //Serial.println("enBPSH"); 
    //delay(3); 
  }



 class Ingredient {
  
    private:
            
      const int channelPosition[5] = {2500+1200+6650,(int)(2500 + (COUNT_PER_ROTATION*5)- 6650) ,(int)(2500 + (COUNT_PER_ROTATION*5.2*2)- 6650) ,(int)(2500 + (COUNT_PER_ROTATION*5.3*3) - 6650) ,(int)(2500 + (COUNT_PER_ROTATION*5.35*4) - 6650)}; 
//      const int channelPosition[5] = {2500,(int)(2500 + (COUNT_PER_ROTATION*5)) ,(int)(2500 + (COUNT_PER_ROTATION*5.2*2)) ,(int)(2500 + (COUNT_PER_ROTATION*5.3*3) ) ,(int)(2500 + (COUNT_PER_ROTATION*5.35*4) )}; 
      
      const int slotPosition[2] = {87084,174168}; 
      
      //functions 
            
      void movePusherZero(){
        PSH_BKWD(); 
        while(digitalRead(PSH_LEFT_LIMIT)); 
        PSH_STP(); 
        Serial.println("Pusher limit Switch pressed");  
        Serial.flush();
        encoderPosPSH = 0; 
      }
           
      //platform motor 
      void movePlatformTo(double targetCount){
        double error ; 
        
        PLM_STP();   
        error = (targetCount - encoderPosPLM); 
        Serial.print("moving the platform");
        Serial.println(error);
        Serial.flush(); 
      
        // set things up the first time
        if(abs(error) > TOLERANCE) 
        {
            if(error > 0) {
                PLM_FRWD(); 
           }
           else { 
                PLM_BKWD();  
           }
           
           if(abs(error) > HIGH_THRESOLD) { 
              setPlatformSpeed(SPEED_PLM_H);
            }
            else {
              setPlatformSpeed((int)(KpPLM*abs(error)));
            } 
      
       }
        
        // move fast till the HIGH_THRESOLD
        while(abs(targetCount - encoderPosPLM) > HIGH_THRESOLD);
//        {
//          Serial.println(encoderPosPLM); 
//        }
        //Serial.flush(); 
        // slow down
        error = (targetCount - encoderPosPLM);  
            
        //proportion control 
        while (abs(error) > TOLERANCE) 
         {
           if(error > TOLERANCE) {
                PLM_FRWD(); 
           }
           else if(error < (-1*TOLERANCE)) { 
                PLM_BKWD();  
           }
           
           if(abs(error) < HIGH_THRESOLD)  setPlatformSpeed((int)(KpPLM*abs(error))+20);
      
          error = (targetCount - encoderPosPLM); 
          //Serial.println(encoderPosPLM); 
          //Serial.print("error:");
          //Serial.println(error);
          //Serial.flush();
         }  
        PLM_STP(); 
        Serial.flush(); 
        Serial.print("Platform moved to: "); 
        Serial.println(encoderPosPLM); 
        setPlatformSpeed(SPEED_PLM_M); 
      }
      
      void movePlatformToChannel(int channel){
        Serial.print("moving to channel: "); Serial.println(channel); 
        movePlatformTo(channelPosition[channel]); 
      }
      
      // pusher motor
      void movePusherTo(double targetCount){
      
        double error ; 
        PSH_STP();   
      
        error = (targetCount - encoderPosPSH); 
        //Serial.print("Pusher error first time:");
        //Serial.println(error);
        //Serial.flush(); 
      
        // set things up the first time
        if(abs(error) > TOLERANCE_PSH) 
        {
            if(error > 0) {
                PSH_FRWD(); 
               // Serial.println("Moving Forward");
           }
           else { 
                PSH_BKWD();        
               // Serial.println("Moving Backward");
           }
           
           if(abs(error) > HIGH_THRESOLD_PSH) { 
              setPusherSpeed(SPEED_PSH_H);
            }
            else {
              setPusherSpeed((int)(KpPSH*abs(error)));
            } 
      
       }
        
        // move fast till the HIGH_THRESOLD
        while(abs(targetCount - encoderPosPSH) > HIGH_THRESOLD_PSH); 
        // slow down
        error = (targetCount - encoderPosPSH);  
            
        //proportion control 
        while (abs(error) > TOLERANCE_PSH) 
         {
           if(error > TOLERANCE_PSH) {
                PSH_FRWD(); 
                //Serial.println("Moving Forward correction");
           }
           else if(error < (-1*TOLERANCE_PSH)) { 
                PSH_BKWD();  
                //Serial.println("Moving backward correction");
           }
           
           if(abs(error) < HIGH_THRESOLD_PSH)  setPusherSpeed((int)(KpPSH*abs(error))+20);
      
          error = (targetCount - encoderPosPSH); 
          //Serial.print("error:");
          //Serial.println(encoderPosPSH);
          //Serial.flush();
         }
        
        PSH_STP(); 
        //Serial.println("one dispense"); 
        setPusherSpeed(SPEED_PSH_H);
      }
      
      void attachhook()
      {
        Serial.println("Attaching Hook");
        Serial.flush(); 
        delay(300);
        //moving the pusher ahead
        movePusherTo(PUSHER_INITIAL_POS);
        delay(300);
        // moving platform to the aligned position
        movePlatformTo(encoderPosPLM+PLATFORM_HOOK_DISPLACEMENT);
        Serial.println("Hook Attached");
      }
      
      void detachhook()
      {
        Serial.println("Detaching Hook");
        Serial.flush();
        delay(500);
        movePlatformTo(encoderPosPLM-(PLATFORM_HOOK_DISPLACEMENT+1000)); 
        delay(500);
        movePusherZero();
        Serial.println("Hook Detached");
      }

      void attachhookZero()
      {
        Serial.println("Attaching Hook");
        Serial.flush(); 
        delay(300);
        //moving the pusher ahead
        movePusherTo(PUSHER_INITIAL_POS);
        delay(300);
        // moving platform to the aligned position
        movePlatformTo(encoderPosPLM-PLATFORM_HOOK_DISPLACEMENT);
        delay(500); 
        Serial.println("Hook Attached");
        Serial.flush(); 
      }

      void detachhookZero()
      {
        Serial.println("Detaching Hook");
        Serial.flush();
        delay(500);
        movePlatformTo(encoderPosPLM+(PLATFORM_HOOK_DISPLACEMENT+1000)); 
        delay(500);
        movePusherZero();
        Serial.println("Hook Detached");
      }


    public: 
      void dispense(int channel) {
        Serial.print("Moving the channel to: ");  Serial.println(channel);
        movePlatformTo(channelPosition[channel]); 
        Serial.println("attaching the hook: ");
        if(channel) {
          attachhook(); 
          delay(100);
          movePusherTo(PUSHER_END); 
          delay(500); 
          // move back pusher to the intial position
          movePusherTo(PUSHER_INITIAL_POS-11000); 
          delay(300); 
         //movePusherZero();
          // detach hook 
          detachhook();
          //movePlatformBack();
        }  
        else {
          attachhookZero(); 
          delay(500);
          movePusherTo(PUSHER_END); 
          delay(500); 
//          // move back pusher to the intial position
          movePusherTo(PUSHER_INITIAL_POS-11000);
          delay(300); 
          detachhookZero(); 
          //movePlatformBack()   ;
        }
        delay(200); 
        // move the platform to zero 
        movePlatformBack(); 
        delay(300); 
      }
      
      void ingredientSetup(){
      
        // setup veg platform motor
         pinMode(PLM_EN,OUTPUT); 
         pinMode(PLM_IN1,OUTPUT);
         pinMode(PLM_IN2,OUTPUT);

         digitalWrite(PLM_EN,LOW); 
         digitalWrite(PLM_IN1,LOW);
         digitalWrite(PLM_IN2,LOW);
         
      
         setPlatformSpeed(SPEED_PLM_M); 
      
         pinMode(PLM_FRNT_LIMIT, INPUT_PULLUP); 
         pinMode(PLM_BACK_LIMIT,INPUT_PULLUP);
      
         pinMode(PLM_ENCA, INPUT);
         pinMode(PLM_ENCA, INPUT_PULLUP);
      
         pinMode(PLM_ENCB, INPUT);
         pinMode(PLM_ENCB, INPUT_PULLUP);
      
         attachInterrupt(digitalPinToInterrupt(PLM_ENCA),enAPLMInterrupt,CHANGE); 
         attachInterrupt(digitalPinToInterrupt(PLM_ENCB),enBPLMInterrupt,CHANGE); 
      
         // setup veg pusher motor
         pinMode(PSH_EN,OUTPUT); 
         pinMode(PSH_IN1,OUTPUT);
         pinMode(PSH_IN2,OUTPUT);
      
         setPusherSpeed(PSH_SPEED);
      
         pinMode(PSH_LEFT_LIMIT, INPUT_PULLUP); 
         pinMode(PSH_RIGHT_LIMIT,INPUT_PULLUP);
      
         pinMode(PSH_ENCA, INPUT);
         pinMode(PSH_ENCA, INPUT_PULLUP);
      
         pinMode(PSH_ENCB, INPUT);
         pinMode(PSH_ENCB, INPUT_PULLUP);
      
         attachInterrupt(digitalPinToInterrupt(PSH_ENCA),enAPSHInterrupt,CHANGE); 
         attachInterrupt(digitalPinToInterrupt(PSH_ENCB),enBPSHInterrupt,CHANGE); 

         Serial.print("Moving the pusher to zero: ");  Serial.flush();
        
         movePusherZero(); 
         Serial.print("Moved pusher to zero: ");  Serial.flush();
         Serial.print("Moving the platform to zero: ");  Serial.flush();
         movePlatformBack();
         Serial.print("Moved the platform to zero: ");  Serial.flush();
      }

        void movePlatformBack(){
        PLM_BKWD(); 
        while(digitalRead(PLM_BACK_LIMIT)); 
        PLM_STP(); 
        delay(500); 
        encoderPosPLM = 0; 
        Serial.println("Platfrom back Switch pressed");  
        Serial.flush();
        
      }
      
      void movePlatformFrnt(){
        PLM_FRWD(); 
        while(digitalRead(PLM_FRNT_LIMIT)); 
        PLM_STP(); 
        Serial.println("Platform front Switch pressed");  
        Serial.flush();  
      
      }


 }; 
 Ingredient Ingredient;


#endif
