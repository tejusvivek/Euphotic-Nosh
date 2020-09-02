############################################################################
# Author : Yatin  Varachhia
# Owner  : Euphotic Labs PVT LTD
# April 2018 
#- ----------------------------------------------------------------------
# To Do : 
#   - recive ack once transfer is done 
#   - Group commands to same subassembly 
#   -
#   -
###############################################################################

import os,sys
import smbus
import time
import logging
from datetime import datetime
#import pyparsing as pp

# defines 
# arduino numbering 
# 0 : Spice powder , functions : dispense(box_no, number_of_stokes) 
# 1 : Spice whole,  functions : dispense(box_no, number_of_stokes) 
# 2 : Paste  ,   functions : dispense(box_no, number_of_stokes) 
# 3 : vegetable ,   functions : dispense(box_no, number_of_stokes) 
# 4 : stirrer ,  functions : arm, stir(speed), disarm ;    
# 5 : heat_control,     functions : on(), off(), setHeat(int heatLevel)
# 6 : chimney ,     functions :  on(), off(), setPower() 

#############################################################################
# status, command_sent, command_executed 

bus = smbus.SMBus(1);

Tempsensor_address= 0x5A
TA_addr=0x06
Tobj_addr = 0x07
micro_addr=0x54


commands = {'ingredient_dispense':0x01,'ingredient_rest':0x02,'spice_dispense':0x03, 'spice_rest': 0x04, 'water_dispense':0x05, 'oil_dispense':0x06, 'stove_on':0x07, 'stove_off':0x08, 'stove_level':0x09, 'stove_temp':0x0a, 'stir_position': 0x0b, 'stir_rest':0x0c, 'saute':0x0d, 'mix':0xe, 'mix_first':0x0f, 'mix_through_start':0x10, 'mix_through_stop':0x11, 'mix_crush':0x12}
response = {'Done':0x12, 'waiting':0x13,'error':0x14}

tempreading = 25
spiceBoxMapping = {'salt':0x02, 'garamMasala':0x04, 'turmeric':0x05, 'chilliPowder':0x03, 'mustard':0x00, 'cumin':0x01 }
#vegBoxMapping = {'coriander':0x00, 'poha':0x05, 'onion':0x03, 'peanut':0x04, 'greenchilli':0x02, 'potato':0x01  } 
vegBoxMapping={}


#address = 0x04
def writeNumber(cmd,value):
    bus.write_byte_data(micro_addr,commands[cmd], value)
    time.sleep(3) 
    #print arduino[arduinoId], "," , commands[cmd] , "," , value
    # bus.write_byte_data(address, 0, value)
    return -1

def readNumber():
    #time.sleep(1) 
    number = bus.read_byte(micro_addr)
    #return number

def processLine(recipelinelist):
    print (recipelinelist)
    #print vegBoxMapping
    if(recipelinelist[0]=="vegmap"):
        #d={recipeline[1]:int(recipeline[2],16)}
        #vegmapping.update(d)
        line=dict(x.split('=') for x in recipelinelist[1].split(','))
        line={k:(int(v,16)-1) for k,v in line.items()}
        vegBoxMapping.update(line)
    
    elif(recipelinelist[0] == "stove") :  # actions for stove
        if(recipelinelist[1] == "start")  : 
		writeNumber("stove_on" ,0) 
		time.sleep(4)
        elif(recipelinelist[1] == "stop") : writeNumber("stove_off" ,0) 
        elif(recipelinelist[1] == "heat") : writeNumber("stove_level" ,int(recipelinelist[2]))

    elif( recipelinelist[0] == "wait")      :  time.sleep(float(recipelinelist[1])-1)  
    elif( recipelinelist[0] == "oil")       :  
        writeNumber("oil_dispense",int(recipelinelist[2])) 
        #tempreading = 25
        #while(int(tempreading)<=80):
        #        writeNumber("stirrer","temp",0)
		#tempreading=readNumber("stirrer")
                #f=open('tempdata','a+')
                #f.write("data time is "+str(datetime.now())+str(" : the temperature is :")+str(tempreading)+str("\n"))
	
	time.sleep(0.04*float(recipelinelist[2])) 
    elif( recipelinelist[0] == "water")       :  
	if (int(recipelinelist[2])>250):
		writeNumber("water_dispense",250)
		time.sleep(2.5)
		writeNumber("water_dispense",int(recipelinelist[2])-250)
	else:
		writeNumber("water_dispense",int(recipelinelist[2])) 
	#time.sleep(float(recipelinelist[2])) 
    elif( recipelinelist[0] == "heat_till") :
	tempreading=10.0
	f=open('temperature_data.txt','a+')
	while(tempreading<=float(recipelinelist[1])):
		time.sleep(1)
		tempreading = bus.read_word_data(Tempsensor_address,Tobj_addr)
		tempreading=(tempreading*0.02)-273.15
		f.write("data time is "+str(datetime.now())+str(" : the temperature is :")+str(tempreading)+str("\n"))
		print("The pan is heating. The present temperature is: "+str(tempreading))
  # if(tempreading>=recipelinelist[1]):
  #   break
	print("Temperature heated till:"+str(recipelinelist[1]))



    elif( recipelinelist[0] == "spice")     :
	if(recipelinelist[1] == "rest")   :
		writeNumber("spice_rest",0)
		time.sleep(15) #6	
	else                               : 
		writeNumber("spice_dispense",spiceBoxMapping[recipelinelist[1]]) 
		time.sleep(8)
    elif(recipelinelist[0] == "vegetable") : 
	if(vegBoxMapping=={}):
                print("Enter the vegetable mapping before dispensing ")
		sys.exit()
	writeNumber("ingredient_dispense",vegBoxMapping[recipelinelist[1]]) 
	time.sleep(20 + (1.5*vegBoxMapping[recipelinelist[1]])) 
	#writeNumber("vegBowl","dispense",0) 
  	#time.sleep(5) 
    elif( recipelinelist[0] == "stir")     : 
	if(recipelinelist[1] == "position") : 
		writeNumber("stir_position",0)
		time.sleep(3.5) 	
	elif(recipelinelist[1] == "rest")   :
		writeNumber("stir_rest",0)
		time.sleep(3.5) 	
	elif(recipelinelist[1] == "saute")   :
		writeNumber("saute",int(recipelinelist[2]))
		time.sleep(float(recipelinelist[2])*17) 

	elif(recipelinelist[1] == "mix")   :
		writeNumber("mix",int(recipelinelist[2]))
		time.sleep(float(recipelinelist[2])*19) #27
	elif(recipelinelist[1] == "mix_through_start")   :
		writeNumber("mix_through_start",0)
		time.sleep(4) 
	elif(recipelinelist[1] == "mix_through_stop")   :
		writeNumber("mix_through_stop",0)
		time.sleep(3.5) 
	elif(recipelinelist[1] == "mix_first")   :
		writeNumber("mix_first",0)
		time.sleep(4.5) 
	elif(recipelinelist[1] == "crush")   :
		writeNumber("crush",0)
		#writeNumber("mix_crush",int(recipelinelist[2]))
		time.sleep(56)
		#time.sleep(float(recipelinelist[2]*58))
	  
    elif( recipelinelist[0] == "paste")    : 
	writeNumber("paste","dispense",pasteBoxMapping[recipelinelist[1]]) 
	time.sleep(5) 
    elif( recipelinelist[0] == "chimney")  : time.sleep(1)  

## start 
print "reading the recipe file"
#filne = "CauliflowerFryCurry.recipe" 
#filne = "potatoFryCurry.recipe" 
#filne = "poha_delight.recipe" 
#filne = "poha.recipe" 
#filne = "RedPasta.recipe"
filne = "temp.recipe"
#filne = "Pulao.recipe"
#filne = "Pulao4min.recipe"
#filne = "Khichdi.recipe"
#filne = "Upma.recipe"
#filne = "Delight_Upma.recipe"
#filne = "pulav.recipe" 
#filne = "KadaiPaneer.recipe" 
#filne = "SujiHalwa.recipe" 
#filne = "Dal.recipe" 
#filne = "Cabbage.recipe" 
#filne = "Chole.recipe" 
#filne = "WhitePasta.recipe" 
with open(filne, 'r') as f:
    for line in f:
        recipeline = line.strip() 
        recipelinelist = recipeline.split(" ")
        processLine(recipelinelist)  
        #print recipelinelist

#id = False 
#var = False
#noDispensing = 0 
#boxNo = -1
##boxNo = 0
#time.sleep(10)  
#print "Starting the dispensing" 
#
#while True:                                               
#    noDispensing = noDispensing + 1
#    boxNo = boxNo + 1                
#    print "Dispensing powder spices from box: ", boxNo,"times: ", noDispensing  
#    writeNumber(1,spiceBoxCommands['dispense'],boxNo)                                   
#    # sleep one second                                    
#    time.sleep(10)                                         
#    #while(readNumber(Arduino[0]) == spiceBoxResponse['dispensingDone']) 
#    print "Dispensing done " 
#    print                                                                                
#    if(boxNo == 6) :  
#        sys.exit()   
#    time.sleep(5) 
