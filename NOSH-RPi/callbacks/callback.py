def clk_button_callback(channel):
	global dtState, clkState, clkLastState
	#print("clk button pressed %s" %channel)
	clkState = GPIO.input(clk)
	rotary_fn()

def dt_button_callback(channel):
	global dtState, clkState, clkLastState
	#print("dt button pressed %s" %channel)
	dtState = GPIO.input(dt)
	rotary_fn()


'''Cooking page from MainScreen'''
def cook_callback():
	#print('The button <%s> is being pressed' % instance.text)
	select_button=0
	cook_fn()


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


'''Final Cooking page, on button press'''
def popup_callback(instance):
	global cmd,food_selected, idle_time, popup_status,final_page_status
	popup_status=0
	popup.dismiss()
	cmd=0x02
	#writeNumber('ingredient_rest',0)
	print('The button <<%s>> is being pressed' + instance)
	carousel.remove_widget(cook_page1)
	carousel.remove_widget(cook_page2)
	carousel.remove_widget(cook_page3)
	carousel.remove_widget(cook_page4)
	#carousel.remove_widget(cook_page5)
	food_selected=instance
	print('Cooking ', food_selected)
	final_page.text='Cooking '+food_selected
	#execfile('Delight.py')
	#os.system('python Delight.py')
	final_page_status=1
	carousel.add_widget(final_page)
	#os.system('python Delight.py')
	#execfile('Delight.py')
	#from Delight import *
	#cooking_test()
	#final_page_status=0
	idle_time=0