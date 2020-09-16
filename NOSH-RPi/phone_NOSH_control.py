import socket
from datetime import datetime
from datetime import timedelta
import threading
import time

import os, sys
import time
import logging
from datetime import datetime

timer = None

DEBUG_FLAG = False

if not DEBUG_FLAG:
    import smbus
    bus = smbus.SMBus(1)

Tempsensor_address = 0x5A
TA_addr = 0x06
Tobj_addr = 0x07
micro_addr = 0x54

commands = {'ingredient_dispense': 0x01,
            'ingredient_rest': 0x02, 'spice_dispense': 0x03,
            'spice_rest': 0x04, 'water_dispense': 0x05, 'oil_dispense': 0x06,
            'stove_on': 0x07, 'stove_off': 0x08, 'stove_level': 0x09, 'stove_temp': 0x0a,
            'stir_position': 0x0b, 'stir_rest': 0x0c, 'saute': 0x0d, 'mix': 0xe, 'mix_first': 0x0f,
            'mix_through_start': 0x10, 'mix_through_stop': 0x11, 'mix_crush': 0x12}

response = {'Done': 0x12, 'waiting': 0x13, 'error': 0x14}

tempreading = 25

spiceBoxMapping = {'salt': 0x02, 'garamMasala': 0x04, 'turmeric': 0x05, 'chilliPowder': 0x03, 'mustard': 0x00,
                   'cumin': 0x01}


spice_switcher = {1: 'Salt', 2: 'Chilli Powder', 3: 'Garam Masala', 4: 'Cumin', 5: 'Mustard', 6: 'Turmeric',
                  7: 'Spice 7', 8: 'Spice 8'}

veg_switcher = {1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}

heat_switcher = {1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8'}

# vegBoxMapping = {'coriander':0x00, 'poha':0x05, 'onion':0x03, 'peanut':0x04, 'greenchilli':0x02, 'potato':0x01  }

vegBoxMapping = {}


def server_program():
    host = '0.0.0.0'
    port = 8086
    global server_socket, conn, data_recv
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(2)
    server_socket.setblocking(1)
    # conn.send("Thank You for conecting!")
    while True:
        conn, address = server_socket.accept()
        print("Connection from: " + str(address))
        threading.Thread(target=receive_data()).start()

    conn.close()  # close the connection


def receive_data():
    global data_recv
    while True:
        data_recv_raw = conn.recv(16)
        data_recv_decoded = data_recv_raw.decode()
        data_recv = data_recv_decoded

        print("from client decoded -> " + str(data_recv))

        thread2 = threading.Thread(target=simulate_machine(data_recv))
        thread2.start()
        # delay()
        # thread2.join()


def timer_loop():
    time.sleep(2)


def send_message():
    msg = input("Enter data-->")
    conn.send(msg.encode())


def switch_spice(data_ip):
    return spice_switcher.get(data_ip)


def switch_vegetable(data_ip):
    return veg_switcher.get(data_ip)


def switch_heat(data_ip):
    return heat_switcher.get(data_ip)


def writeNumber(command_name, value):
    bus.write_byte_data(micro_addr, commands[command_name], value)
    time.sleep(3)
    return -1


def readNumber():
    number = bus.read_byte(micro_addr)


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('192.168.1.1', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def delay(b):
    T = threading.Thread(target=timer_loop)
    T.start()
    # time.sleep(1)
    T.join()
    '''start = time.time()
    while time.time()-start <= 1:
        print(time.time()-start)
        #pass'''
    msg = 'REQUEST COMPLETED'
    inv_msg = 'INVALID REQUEST PLEASE TRY AGAIN'
    if (b == 1):
        conn.sendall((msg + '\n').encode())
    elif (b == 0):
        conn.sendall((inv_msg + '\n').encode())


def simulate_machine(a):
    data = int(a, 16)
    '''start = time.time()
    while time.time() - start < 2:
        #print(time.time())
        pass'''

    print("data16:", data)
    msg = 'REQUEST COMPLETED'
    inv_msg = 'INVALID REQUEST PLEASE TRY AGAIN'
    if (data == 16):
        print('STOVE STOP')
        writeNumber("stove_off", 0)
        delay(1)

    elif (data == 17):
        print('STOVE START')
        writeNumber("stove_on", 0)
        delay(1)

    elif (data == 18):
        conn.sendall(('PC: Enter Heat Level ' + '\n').encode())
        heat_level = conn.recv(1024).decode()
        data = int(heat_level, 10)
        try:
            heat = switch_heat(data)
            print('Setting Heat Level to ' + heat)
            writeNumber("stove_level", heat)
            delay(1)

        except TypeError:
            delay(1)

    elif (data == 48):
        conn.sendall(('PC: Enter amount of Water to be dispensed in mL ' + '\n').encode())
        water_quantity = int(conn.recv(1024).decode())
        print('Dispensing ' + str(water_quantity) + ' mL of Water')
        delay(1)

        if water_quantity > 250:
            writeNumber("water_dispense", 250)
            time.sleep(2.5)
            writeNumber("water_dispense", water_quantity - 250)
        else:
            writeNumber("water_dispense", water_quantity)


    elif (data == 32):
        conn.sendall(('PC: Enter amount of Oil to be dispensed in mL ' + '\n').encode())
        oil_quantity = conn.recv(1024).decode()
        print('Dispensing ' + str(oil_quantity) + ' mL of Oil')
        delay(1)
        try:
            writeNumber("oil_dispense", oil_quantity)
        except:
            print("Invalid Value")

    elif (data == 64):
        conn.sendall(('PC: Enter the Vegetable Slot to Dispense' + '\n').encode())
        data_ip = conn.recv(1024).decode()
        data = int(data_ip, 10)
        try:
            vegetable = switch_vegetable(data)
            print('Dispensing Vegetable Slot ' + vegetable)
            delay(1)

        except TypeError:
            delay(0)


    elif (data == 65):
        print('Bringing Vegetable platform forward Please Load the tray')
        delay(1)

    elif (data == 66):
        print('Tray is loaded')
        delay(1)

    elif (data == 73):
        print("Setting to Stir rest position")
        writeNumber("stir_rest", 0)
        delay(1)

    elif (data == 80):
        print('Setting to Stir POSITION')
        writeNumber("stir_position", 0)
        delay(1)


    elif (data == 81):
        conn.sendall('PC: Set number of times to saute ' + '\n')
        data_ip = conn.recv(1024).decode()
        writeNumber("saute", data_ip)
        time.sleep(float(data_ip) * 17)

        print('Saute is done ' + str(data_ip) + ' times')
        delay(1)

    elif (data == 82):
        conn.sendall('PC: Set number of times to mix ' + '\n')
        data_ip = conn.recv(1024).decode()
        writeNumber("mix", int(data_ip))
        time.sleep(float(data_ip) * 19)
        print('Mixing is done ' + str(data_ip) + ' times')
        delay(1)

    elif (data == 83):
        print('Mix First is done')
        writeNumber("mix_first", 0)
        delay(1)

    elif (data == 84):
        conn.sendall('PC: Set number of times to crush ' + '\n')
        data_ip = conn.recv(1024).decode()
        print('Crushing is done ' + str(data_ip) + ' times')
        writeNumber("crush", 0)
        delay(1)

    elif (data == 90):
        print('Mix Through is started')
        writeNumber("mix_through_start", 0)
        delay(1)
        # conn.sendall((msg + '\n').encode())
        # result_flag.set()
    elif (data == 91):
        print('Mix Through is stopped')
        writeNumber("mix_through_stop", 0)
        delay(1)

    elif (data == 96):
        print('Spice is Rotated to Rest position')
        writeNumber("spice_rest", 0)
        delay(1)

    elif (data == 97):
        conn.sendall(('PC: Select which spice to dispense' + '\n').encode())
        data_ip = conn.recv(1024).decode()
        data = int(data_ip, 10)
        try:
            spice = switch_spice(data)
            print('Dispensing spice ' + spice)
            writeNumber("spice_dispense", data)
            delay(1)
        except TypeError:
            delay(0)

    elif (data == 112):
        conn.sendall(('PC: Enter amount of time to wait in seconds ' + '\n').encode())
        data_ip = conn.recv(1024).decode()
        print('Waiting for ' + str(data_ip) + ' seconds')
        delay(1)

    elif (data == 113):
        ip = get_ip()
        port = '8080'
        conn.sendall((str(ip) + ':' + port + '\n').encode())
        print('Streaming VIDEO')

    elif (data == 255):
        conn.sendall(("PC: Process completed Terminating connection!!" + '\n').encode())
        conn.close()
    else:
        delay(0)


server_program()