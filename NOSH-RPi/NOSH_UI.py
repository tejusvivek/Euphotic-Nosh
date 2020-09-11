# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 11:47:55 2020

@author: Tejus V
"""

import kivy

kivy.require("1.8.0")

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.carousel import Carousel
from kivy.uix.image import Image
from kivy.uix.popup import Popup

from datetime import datetime
from datetime import timedelta

from RPi import GPIO

from subprocess import call
import os, sys
import smbus
import time
import logging

'''I2C communication'''
bus = smbus.SMBus(1);
TA_addr = 0x06
Tobj_addr = 0x07
micro_addr = 0x54

time_text = ""
cook_time_text = ""

carousel = Carousel(direction='right')
carousel.loop = True

timer_label = Label(text=time_text, font_size='50sp', color=(1, 1, 0, 1))
cook_timer_label = Label(text=time_text, font_size='10sp')

'''Status Variables'''
page_number_in_cook = 0
MAXIMUM_PAGES = 3
MINIMUM_PAGES = 1
MAXIMUM_PAGES_IN_COOK = 5
MINIMUM_PAGES_IN_COOK = 1
CLOCK_PAGE_NUMBER = 1
MAIN_APP_PAGE_NUMBER = 2
FOOD_PAGE_NUMBER = 3
SETUP_PAGE_NUMBER = 4
timed_out_page = 0
idle_time = 0
IDLE_THRESHOLD = 20
idle_status = 0
popup_status = 0
final_page_status = 0
select_button = 0

'''Rotary Switch Variables'''
count = 0
counter = 0
push_button = 22
clk = 17
dt = 18

clkState = 0
dtState = 0

'''GPIO SETUP'''
GPIO.setmode(GPIO.BCM)
GPIO.setup(push_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_UP)

clkLastState = GPIO.input(clk)

popup_title = ''

'''Initial Page Number'''
page_number = MAIN_APP_PAGE_NUMBER

commands = {'ingredient_dispense': 0x01, 'ingredient_rest': 0x02, 'spice_dispense': 0x03, 'spice_rest': 0x04,
            'water_dispense': 0x05, 'oil_dispense': 0x06, 'stove_on': 0x07, 'stove_off': 0x08, 'stove_level': 0x09,
            'stove_temp': 0x0a, 'stir_position': 0x0b, 'stir_rest': 0x0c, 'saute': 0x0d, 'mix': 0xe, 'mix_first': 0x0f,
            'mix_through_start': 0x10, 'mix_through_stop': 0x11, 'mix_crush': 0x12, 'input_ingredient': 0x15}

# FOR COOKING
'''def cooking_test():
	global page_number,final_page_status,idle_time
	#os.system('python Delight.py')
	#page_number=CLOCK_PAGE_NUMBER
	#screen_maintainer()
	call(["python", "Delight.py"])
	final_page_status=0
	print(final_page_status)
	page_number=CLOCK_PAGE_NUMBER
	print(page_number)
	idle_time=10
	print(idle_time)
	home_screen_timer()
	#import Delight

def writeNumber(cmd,value):
    bus.write_byte_data(micro_addr,commands[cmd],value)
    time.sleep(3)
    #print arduino[arduinoId], "," , commands[cmd] , "," , value
    # bus.write_byte_data(address, 0, value)
    return -1

def readNumber():
    #time.sleep(1)
    global number
    number = bus.read_byte(micro_addr)
    return number'''

'''Cooking page from MainScreen'''


def cook_callback():
    # print('The button <%s> is being pressed' % instance.text)
    select_button = 0
    cook_fn()


'''Adding the dish pages'''


def cook_fn():
    global page_number_in_cook, idle_time
    # print('The button <%s> is being pressed' % instance.text)
    carousel.remove_widget(main_page)
    carousel.add_widget(cook_page1)
    carousel.add_widget(cook_page2)
    carousel.add_widget(cook_page3)
    carousel.add_widget(cook_page4)
    # carousel.add_widget(cook_timer_label)
    # carousel.add_widget(cook_page5)
    page_number = FOOD_PAGE_NUMBER
    page_number_in_cook = 1
    idle_time = 0


'''Setup Page from MainScreen'''


def setup_callback():
    global idle_time, page_number
    select_button = 0
    # print('The button <%s> is being pressed' % instance.text)
    carousel.remove_widget(main_page)
    carousel.add_widget(setup_page)
    page_number = SETUP_PAGE_NUMBER
    idle_time = 0


'''Home CallBack from final cook screen'''


def home_callback():
    global page_number, final_page_status, idle_time, idle_status
    page_number = MAIN_APP_PAGE_NUMBER
    final_page_status = 0
    carousel.remove_widget(final_page)
    screen_maintainer()
    idle_time = 0


# idle_status=0

'''Home CallBack from setup page'''


def home_callback_from_setup():
    global page_number, idle_time, idle_status
    page_number = MAIN_APP_PAGE_NUMBER
    carousel.remove_widget(setup_page)
    screen_maintainer()
    idle_time = 0


# idle_status=0

'''Cook page callback for dishes'''


def cook_inside_page_callback(instance):
    print('The button <%s> is being pressed' + instance)
    food_fn(instance)


'''Do you want to cook Popup'''


def food_fn(instance):
    global number, cmd, food_selected, idle_time, popup_status
    print("Do you want to prepare", instance)
    food_selected = instance
    popup.title = 'Do you want to cook ' + instance
    print(popup_status)
    popup_status = 1
    print(popup_status)
    cmd = 0x15
    # if(readNumber()!=0x01):
    # writeNumber("input_ingredient",0)
    popup.open()
    idle_time = 0


# print("Do you want to prepare)

'''Final Cooking page, on button press'''


def popup_callback(instance):
    global cmd, food_selected, idle_time, popup_status, final_page_status
    popup_status = 0
    popup.dismiss()
    cmd = 0x02
    # writeNumber('ingredient_rest',0)
    print('The button <<%s>> is being pressed' + instance)
    carousel.remove_widget(cook_page1)
    carousel.remove_widget(cook_page2)
    carousel.remove_widget(cook_page3)
    carousel.remove_widget(cook_page4)
    # carousel.remove_widget(cook_page5)
    food_selected = instance
    print('Cooking ', food_selected)
    final_page.text = 'Cooking ' + food_selected
    # execfile('Delight.py')
    # os.system('python Delight.py')
    final_page_status = 1
    carousel.add_widget(final_page)
    # os.system('python Delight.py')
    # execfile('Delight.py')
    # from Delight import *
    # cooking_test()
    # final_page_status=0
    idle_time = 0


'''Main Screen Maintainer for UI'''


def screen_maintainer():
    global idle_status, time_text, page_number, idle_time, timed_out_page
    print("screen maintainer")
    if page_number == CLOCK_PAGE_NUMBER:
        idle_status = 1
        idle_time = 0
        if (timed_out_page == MAIN_APP_PAGE_NUMBER):
            carousel.remove_widget(main_page)
        elif (timed_out_page == SETUP_PAGE_NUMBER):
            carousel.remove_widget(setup_page)
        elif (timed_out_page == FOOD_PAGE_NUMBER):
            carousel.remove_widget(cook_page1)
            carousel.remove_widget(cook_page2)
            carousel.remove_widget(cook_page3)
            carousel.remove_widget(cook_page4)
        # carousel.remove_widget(cook_page5)
        carousel.remove_widget(setup_page)
        popup_status = 0
        print(time_text)
        # carousel.remove_widget(timer_label)
        timer_label.text = time_text
        carousel.add_widget(timer_label)
    # popup.dismiss()
    elif page_number == MAIN_APP_PAGE_NUMBER:
        carousel.remove_widget(timer_label)
        carousel.add_widget(main_page)
        popup.dismiss()
        popup_status = 0
    elif page_number == SETUP_PAGE_NUMBER:
        carousel.remove_widget(main_page)
        carousel.add_widget(setup_page)
        popup.dismiss()
        popup_status = 0


'''Timer for homescreen'''


def home_screen_timer(*args):
    global idle_time, idle_status, IDLE_THRESHOLD, time_text, page_number, final_page_status, timed_out_page
    now = datetime.now()
    now = now + timedelta(seconds=1)
    time_text = now.strftime('%H:%M:%S') + "\n" + now.strftime('%A, %d %B')
    timer_label.text = time_text
    if ((idle_status != 1) & (popup_status == 0)) & (final_page_status == 0):
        idle_time = idle_time + 1
        if idle_time >= IDLE_THRESHOLD:
            print("Timeout")
            if (page_number == MAIN_APP_PAGE_NUMBER):
                timed_out_page = MAIN_APP_PAGE_NUMBER
                page_number = CLOCK_PAGE_NUMBER
            elif (page_number == SETUP_PAGE_NUMBER):
                timed_out_page = SETUP_PAGE_NUMBER
                page_number = CLOCK_PAGE_NUMBER
            elif (page_number == FOOD_PAGE_NUMBER):
                timed_out_page = FOOD_PAGE_NUMBER
                page_number = CLOCK_PAGE_NUMBER
            # idle_status=1
            screen_maintainer()


'''----------------------------------------USER INTERFACE ELEMENTS DEFINITION------------------------------------------'''
'''Various Buttons in the User Interface'''

image_size = (200,290)
image_pos_initial = (140,100)
button_size = (210,300)
button_pos_initial = (135,95)

'''Cook Button'''
cook_img = Image(source='resources/cook_button.png', allow_stretch=True, keep_ratio=False, pos=image_pos_initial, opacity=1, size = image_size)
cook_button = Button(size = button_size, text='COOKING', halign='left', valign='bottom', text_size=(50, 160),
                     pos=button_pos_initial, on_press=cook_callback, opacity=1, border=(10, 10, 10, 10), background_normal='',
                     background_color=(0, 0, 0, 1))
cook_button.add_widget(cook_img)

'''Setup Button'''
setup_img = Image(source='resources/setup_button.png', allow_stretch=True, keep_ratio=False, pos=(450, 100), opacity=1, size = image_size)
setup_button = Button(size = button_size, text='SETUP', halign='left', valign='bottom', border=(10, 10, 10, 10),
                      text_size=(50, 160), pos=(445, 95), size_hint=(.8, .6), on_press=setup_callback, opacity=1,
                      background_normal='', background_color=(0, 0, 0, 1))
setup_button.add_widget(setup_img)

'''Reheat Button'''
reheat_img = Image(source='cook_button.png', allow_stretch=True, keep_ratio=False, pos=(140, 100), opacity=1, width=200,
                   height=290)
reheat_button = Button(height=300, width=210, text='COOK', halign='left', valign='bottom', text_size=(50, 160),
                       pos=(135, 95), on_press=cook_callback, opacity=1, border=(10, 10, 10, 10), background_normal='',
                       background_color=(0, 0, 0, 1))
reheat_button.add_widget(reheat_img)

'''Clean Button'''
clean_img = Image(source='setup_button.png', allow_stretch=True, keep_ratio=False, pos=(450, 100), opacity=1, width=200,
                  height=290)
clean_button = Button(height=300, width=210, text='SETUP', halign='left', valign='bottom', border=(10, 10, 10, 10),
                      text_size=(50, 160), pos=(445, 95), size_hint=(.8, .6), on_press=setup_callback, opacity=1,
                      background_normal='', background_color=(0, 0, 0, 1))
clean_button.add_widget(clean_img)

'''Taste Button'''
taste_img = Image(source='resources/cook_button.png', allow_stretch=True, keep_ratio=False, pos=(140, 100), opacity=1, width=200,
                  height=290)
taste_button = Button(height=300, width=210, text='COOK', halign='left', valign='bottom', text_size=(50, 160),
                      pos=(135, 95), on_press=cook_callback, opacity=1, border=(10, 10, 10, 10), background_normal='',
                      background_color=(0, 0, 0, 1))
taste_button.add_widget(taste_img)

'''power Button'''

power_img = Image(source='resources/setup_button.png', allow_stretch=True, keep_ratio=False, pos=(450, 100), opacity=1, width=200,
                  height=290)
power_button = Button(height=300, width=210, text='SETUP', halign='left', valign='bottom', border=(10, 10, 10, 10),
                      text_size=(50, 160), pos=(445, 95), size_hint=(.8, .6), on_press=setup_callback, opacity=1,
                      background_normal='', background_color=(0, 0, 0, 1))
power_button.add_widget(power_img)

'''Various Pages in User Interface'''

'''Popup'''
popup = Popup(title_size='30sp', title=popup_title, opacity=0.75,
              content=Button(font_size='60sp', text='YES', background_color=(1, 1, 1, 1), on_press=popup_callback,
                             size_hint=(1, 1)), auto_dismiss=False, pos_hint={'x': 0.11, 'y': 0.12},
              size_hint=(.77, .75))

'''Main page'''
main_page = Widget()

'''Adding Widgets to main page'''
main_page.add_widget(cook_button)
main_page.add_widget(setup_button)
# main_page.add_widget(reheat_button)
# main_page.add_widget(taste_button)
# main_page.add_widget(clean_button)
# main_page.add_widget(power_button)

'''Inside Setup Page'''
setup_label = Label(text='STOVE SETUP', font_size='50sp', pos=(180, 380))
setup_page = Button(text=' ', halign='left', valign='bottom', text_size=(150, 320), pos_hint={'x': 0.25, 'y': 0.23},
                    on_press=home_callback_from_setup, background_normal='', background_color=(0, 0, 0, 0))
setup_page.add_widget(setup_label)

'''After Cook Page'''
home_button = Button(text='HOME', font_size='20sp', pos_hint={'x': 0.4, 'y': 0}, size_hint=(.2, .1),
                     background_color=(0, 0, 0, 1), on_press=home_callback)
final_page = Label(text='Cooking', font_size='50sp')
final_page.add_widget(home_button)

'''Various dishes'''
'''DISH 1'''
cook_img1 = Image(source='resources/carrot_beans.png', allow_stretch=True, keep_ratio=False, pos=(95, 65), opacity=1, width=600,
                  height=350)
cook_page1 = Button(font_size='5sp', text='CARROT BEANS', opacity=1, text_size=(1, 1), height=30, width=30,
                    on_press=cook_inside_page_callback, background_normal='', background_color=(0, 0, 0, 1))
cook_page1.add_widget(cook_img1)
'''DISH 2'''
cook_img2 = Image(source='resources/channa_masala.png', allow_stretch=True, keep_ratio=False, pos=(95, 65), opacity=1, width=600,
                  height=350)
cook_page2 = Button(font_size='30sp', text='CHANA MASALA', halign='left', valign='bottom', text_size=(150, 320),
                    on_press=cook_inside_page_callback, background_normal='', background_color=(0, 0, 0, 1))
cook_page2.add_widget(cook_img2)
'''DISH 3'''
cook_img3 = Image(source='resources/bhindi_curry.png', allow_stretch=True, keep_ratio=False, pos=(95, 65), opacity=1, width=600,
                  height=350)
cook_page3 = Button(font_size='30sp', text='BHINDI CURRY', halign='left', valign='bottom', text_size=(150, 320),
                    on_press=cook_inside_page_callback, background_normal='', background_color=(0, 0, 0, 1))
cook_page3.add_widget(cook_img3)
'''DISH 4'''
cook_img4 = Image(source='resources/upma.png', allow_stretch=True, keep_ratio=False, pos=(95, 65), opacity=1, width=600,
                  height=350)
cook_page4 = Button(font_size='30sp', text='UPMA', halign='left', valign='bottom', text_size=(150, 320),
                    on_press=cook_inside_page_callback, background_normal='', background_color=(0, 0, 0, 1))
cook_page4.add_widget(cook_img4)

'''-------------------------------------------UI END----------------------------------------------'''

'''------------------------------------------CONTROLLER START------------------------------------------------'''

'''Next Action'''


def next_fn():
    global page_number, page_number_in_cook, idle_time, idle_status, popup_status
    if idle_status == 1:
        page_number = MAIN_APP_PAGE_NUMBER
        screen_maintainer()
        idle_status = 0
        return
    elif page_number == FOOD_PAGE_NUMBER:
        page_number_in_cook = (page_number_in_cook + 1) % 4
        carousel.load_next()

    popup.dismiss()
    popup_status = 0
    idle_time = 0


'''Previous Action'''


def prev_fn():
    global page_number, page_number_in_cook, idle_time, idle_status, popup_status

    if idle_status == 1:
        page_number = MAIN_APP_PAGE_NUMBER
        screen_maintainer()
        idle_status = 0
        return
    elif page_number == FOOD_PAGE_NUMBER:
        page_number_in_cook = (page_number_in_cook - 1) % 4
        carousel.load_previous()

    popup.dismiss()
    popup_status = 0
    idle_time = 0


'''Switcher function for selecting the dishes in cook_page'''
switcher = {-1: 3, -2: 2, -3: 1, 1: 1, 2: 2, 3: 3, 0: 4}


def switch(page_number_in_cook):
    return switcher.get(page_number_in_cook)


'''Push Button'''


def push_button_callback(channel):
    global page_number, idle_status, idle_time, popup_status, final_page_status, select_button
    print("Push button pressed %s" % channel)
    print(popup_status)
    # idle_status=0
    idle_time = 0
    if ((select_button == 0) | (select_button == 2)) & (page_number == MAIN_APP_PAGE_NUMBER):
        cook_callback()
        page_number = FOOD_PAGE_NUMBER

    elif (select_button == 1) & (page_number == MAIN_APP_PAGE_NUMBER):
        setup_callback()
        page_number = SETUP_PAGE_NUMBER

    elif (page_number == SETUP_PAGE_NUMBER) & (page_number != FOOD_PAGE_NUMBER) & (page_number != MAIN_APP_PAGE_NUMBER):
        home_callback_from_setup()

    elif (page_number == FOOD_PAGE_NUMBER) & (page_number != MAIN_APP_PAGE_NUMBER) & (popup_status == 0) & (
            final_page_status == 0):
        # push_button_inside_inside_cook_page()
        a = switch(page_number_in_cook)
        if (a == 1):
            cook_inside_page_callback(cook_page1.text)
        elif (a == 2):
            cook_inside_page_callback(cook_page2.text)
        elif (a == 3):
            cook_inside_page_callback(cook_page3.text)
        elif (a == 4):
            cook_inside_page_callback(cook_page4.text)
    # elif(a==5):
    # cook_inside_page_callback(cook_page5.text)

    elif (popup_status == 1) & (final_page_status == 0):
        # print(popup_status)
        b = switch(page_number_in_cook)
        if (b == 1):
            popup_callback(cook_page1.text)
            final_page_status = 1
        elif (b == 2):
            popup_callback(cook_page2.text)
            final_page_status = 1
        elif (b == 3):
            popup_callback(cook_page3.text)
            final_page_status = 1
        elif (b == 4):
            popup_callback(cook_page4.text)
            final_page_status = 1
        # elif(b==5):
        # popup_callback(cook_page5.text)
        # final_page_status=1

    elif (final_page_status == 1) & (popup_status == 0):
        home_callback()

    # screen_maintainer()


'''Rotary Function'''


def rotary_fn():
    global count, counter, dtState, clkState, clkLastState, page_number, select_button, idle_status, idle_time
    # print("rotary")
    idle_time = 0
    if (page_number == MAIN_APP_PAGE_NUMBER):
        if clkState != clkLastState:
            if dtState != clkState:
                select_button = 1
                counter += 1
                if (counter == 5):
                    main_page.remove_widget(cook_button)
                    main_page.remove_widget(setup_button)
                    setup_button.background_color = (0.678, 0.847, 0.902, 1)
                    cook_button.background_color = (0, 0, 0, 1)
                    main_page.add_widget(cook_button)
                    main_page.add_widget(setup_button)
                    counter = 0
            else:
                select_button = 2
                counter -= 1
                if (counter == -5):
                    main_page.remove_widget(cook_button)
                    main_page.remove_widget(setup_button)
                    cook_button.background_color = (0.678, 0.847, 0.902, 1)
                    setup_button.background_color = (0, 0, 0, 1)
                    main_page.add_widget(cook_button)
                    main_page.add_widget(setup_button)
                    counter = 0

        clkLastState = clkState

    elif (page_number == FOOD_PAGE_NUMBER):
        if clkState != clkLastState:
            if dtState != clkState:
                count = count + 1
                if (count == 5):
                    count = 0
                    # print(count)
                    next_fn()
            else:
                count = count - 1
                if (count == -5):
                    count = 0
                    # print(count)
                    prev_fn()
        clkLastState = clkState

    elif (page_number == CLOCK_PAGE_NUMBER):
        if clkState != clkLastState:
            if dtState != clkState:
                next_fn()
            else:
                prev_fn()


def clk_button_callback(channel):
    global dtState, clkState, clkLastState
    # print("clk button pressed %s" %channel)
    clkState = GPIO.input(clk)
    rotary_fn()


def dt_button_callback(channel):
    global dtState, clkState, clkLastState
    # print("dt button pressed %s" %channel)
    dtState = GPIO.input(dt)
    rotary_fn()


'''--------------------------------------------CONTROLLER END--------------------------------------------'''

'''INTERRUPTS'''
GPIO.add_event_detect(push_button, GPIO.FALLING, bouncetime=250, callback=push_button_callback)
GPIO.add_event_detect(clk, GPIO.BOTH, callback=clk_button_callback)
GPIO.add_event_detect(dt, GPIO.BOTH, callback=dt_button_callback)

'''Main APP Class'''


class Nosh_UI(App, Widget):
    def build(self):
        screen_maintainer()
        Clock.schedule_interval(home_screen_timer, 1)
        return carousel


if __name__ == "__main__":
    Nosh_UI().run()
