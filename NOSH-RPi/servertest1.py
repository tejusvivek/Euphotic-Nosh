import socket
from datetime import datetime
from datetime import timedelta
import threading
import time

timer = None

def server_program():
    host = '0.0.0.0' 
    port = 8086
    global server_socket,conn,data_recv
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(2)
    server_socket.setblocking(1)
    #conn.send("Thank You for conecting!")
    while True:
        conn, address = server_socket.accept() 
        print("Connection from: " + str(address))
        #receive_data()
	#conn.send("Thank You for conecting!")
	# receive data stream. it won't accept data packet greater than 1024 bytes
        
        #threading.Thread(target=simulate_machine(data)).start()
        threading.Thread(target=receive_data()).start()
        #print('dsfasdfasd')
        
        #threading.Timer(2,timer_loop).start()
        #threading.Thread(target=simulate_machine(data_recv)).start()
        #data1 = input('from server -> ')
        #bytes(data1,encoding='utf8')
        #time.sleep(2)
        #conn.sendall((data1 + '\n').encode())  # send data to the client
	
    #send_message()

    conn.close()  # close the connection

def receive_data():
    global data_recv
    while True:
        data_recv = conn.recv(16).decode()
        print("from client -> " + str(data_recv))
        #if not data: sys.exit(0)
        #time.sleep(2)
        print("simulating...")
        #simulate_machine(data)
        #delay()
        
        thread2 = threading.Thread(target=simulate_machine(data_recv))
        thread2.start()
        #delay()
        #thread2.join()

def timer_loop():
    time.sleep(2)


def send_message():
    msg = input("Enter data-->")
    conn.send(msg.encode())
    
spice_switcher={1:'Salt', 2:'Chilli Powder', 3:'Garam Masala', 4:'Cumin', 5:'Mustard', 6:'Turmeric', 7:'Spice 7', 8:'Spice 8'}

veg_switcher = {1:'1', 2:'2',3:'3',4:'4',5:'5'}

heat_switcher = {1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8'}

def switch_spice(data_ip):
    return spice_switcher.get(data_ip)

def switch_vegetable(data_ip):
    return veg_switcher.get(data_ip)

def switch_heat(data_ip):
    return heat_switcher.get(data_ip)

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
    '''b=0
    while(b<50000):
        b = b+1
        print(b)'''
    T = threading.Thread(target=timer_loop)
    T.start()
    #time.sleep(1)
    T.join()
    '''start = time.time()
    while time.time()-start <= 1:
        print(time.time()-start)
        #pass'''
    msg='REQUEST COMPLETED'
    inv_msg = 'INVALID REQUEST PLEASE TRY AGAIN'
    if(b==1):
        conn.sendall((msg + '\n').encode())
    elif(b==0):
        conn.sendall((inv_msg + '\n').encode())


def simulate_machine(a):
    #result_flag = threading.Event()
    #data = conn.recv(1024).decode()
    #time.sleep(2)
    #delay()
    data = int(a,16)
    '''start = time.time()
    while time.time() - start < 2:
        #print(time.time())
        pass'''
    #delay()
    #print('asdasd')
    print(data)
    msg='REQUEST COMPLETED'
    inv_msg = 'INVALID REQUEST PLEASE TRY AGAIN'
    if(data == 16):
        print('STOVE STOP')
        delay(1)
        #conn.sendall((msg + '\n').encode())
        #result_flag.set()
    elif(data == 17):
        print('STOVE START')
        delay(1)
        #conn.sendall((msg + '\n').encode())
        #result_flag.set()
    elif(data == 18):
        conn.sendall(('Enter Heat Level ' + '\n').encode())
        data_ip = conn.recv(1024).decode()
        data = int(data_ip,10)
        try:
            heat = switch_heat(data)
            print('Setting Heat Level to ' + heat)
            delay(1)
            #conn.sendall((msg + '\n').encode())
            #result_flag.set()
        except TypeError:
            delay(1)
            #conn.sendall((inv_msg + '\n').encode())
            #result_flag.set()
    elif(data == 32):
        conn.sendall(('Enter amount of Water to be dispensed in mL ' + '\n').encode())
        data_ip = conn.recv(1024).decode()
        print('Dispensing ' + str(data_ip) + ' mL of Water' )
        delay(1)
        #conn.sendall((msg + '\n').encode())
        #result_flag.set()
    elif(data == 48):
        conn.sendall(('Enter amount of Oil to be dispensed in mL ' + '\n').encode())
        data_ip = conn.recv(1024).decode()
        print('Dispensing ' + str(data_ip) + ' mL of Oil' )
        delay(1)
        #conn.sendall((msg + '\n').encode())
        #result_flag.set()
    elif(data == 64):
        conn.sendall(('Enter the Vegetable Slot to Dispense' + '\n').encode())
        data_ip = conn.recv(1024).decode()
        data = int(data_ip,10)
        try:
            vegetable = switch_vegetable(data)
            print('Dispensing Vegetable Slot ' +vegetable)
            delay(1)
            #conn.sendall((msg + '\n').encode())
            #result_flag.set()
        except TypeError:
            delay(0)
            #conn.sendall((inv_msg + '\n').encode())
            #result_flag.set()
    elif(data==65):
        print('Bringing Vegetable platform forward Please Load the tray')
        delay(1)
    elif(data==66):
        print('Tray is loaded')
        delay(1)
    elif(data == 80):
        print('Setting to Stir POSITION')
        delay(1)
        #conn.sendall((msg + '\n').encode())
        #result_flag.set()
    elif(data == 81):
        conn.sendall('Set number of times to saute ' + '\n')
        data_ip = conn.recv(1024).decode()
        print('Saute is done ' + str(data_ip) + ' times')
        delay(1)
        #conn.sendall((msg + '\n').encode())
        #result_flag.set()
    elif(data == 82):
        conn.sendall('Set number of times to mix ' + '\n')
        data_ip = conn.recv(1024).decode()
        print('Mixing is done ' + str(data_ip) + ' times')
        delay(1)
        #conn.sendall((msg + '\n').encode())
        #result_flag.set()
    elif(data == 83):
        print('Mix First is done')
        delay(1)
        #conn.sendall((msg + '\n').encode())
        #result_flag.set()
    elif(data == 84):
        conn.sendall('Set number of times to crush ' + '\n')
        data_ip = conn.recv(1024).decode()
        print('Crushing is done ' + str(data_ip) + ' times')
        delay(1)
        #conn.sendall((msg + '\n').encode())
        #result_flag.set()
    elif(data == 90):
        print('Mix Through is started')
        delay(1)
        #conn.sendall((msg + '\n').encode())
        #result_flag.set()
    elif(data == 91):
        print('Mix Through is stopped')
        delay(1)
        #conn.sendall((msg + '\n').encode())
        #result_flag.set()
    elif(data == 96):
        print('Spice is Rotated to Rest position')
        delay(1)
        #conn.sendall((msg + '\n').encode())
        #result_flag.set()
    elif(data == 97):
        conn.sendall('Select which spice to dispense'+ '\n')
        data_ip = conn.recv(1024).decode()
        data = int(data_ip,10)
        try:
           spice = switch_spice(data)
           print('Dispensing spice ' + spice)
           delay(1)
           #conn.sendall((msg + '\n').encode())
           #result_flag.set()
        except TypeError:
           delay(0)
           #conn.sendall((inv_msg +'\n').encode())
           #result_flag.set()
    elif(data == 112):
        conn.sendall('Enter amount of time to wait in seconds ' + '\n')
        data_ip = conn.recv(1024).decode()
        print('Waiting for ' + str(data_ip) + ' seconds')
        delay(1)
        #conn.sendall((msg + '\n').encode())
        #result_flag.set()
    elif(data==113):
        ip=get_ip()
        port='8080'
        conn.sendall((str(ip)+':'+port + '\n').encode())
        print('Streaming VIDEO')
    elif(data == 255):
        conn.sendall(("Process completed Terminating connection!!" + '\n').encode())
        conn.close()
    else:
        delay(0)
        #conn.sendall((inv_msg + '\n').encode())
        #result_flag.set()

if __name__ == '__main__':
    server_program()
