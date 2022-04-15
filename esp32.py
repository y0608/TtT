import time
from machine import Pin
from time import sleep

import socket
import network
from _thread import *
import json

from LCD import CharLCD

lcd = CharLCD(rs=1, en=3, d4=15, d5=13, d6=12, d7=14,
                  cols=16, rows=2)

# CONSTANTS
KEY_UP   = const(0)
KEY_DOWN = const(1)

keys = [['A', 'D', 'G', '0'],
        ['J', 'M', 'P', '0'],
        ['S', 'V', 'Y', '0'],
        ['*', ' ', '1', '0']]
  #{'ABC','DEF','GHI',''},
  #{'JKL','MNO','PQR',''},
  #{'STU','VWX','YZ'},
  #{'select word','space','end message'}

# Pin names for Pico
rows = [12, 14, 27, 26]
cols = [25, 33, 32, 35]

# set pins for rows as outputs
row_pins = [Pin(pin_name, mode=Pin.OUT) for pin_name in rows]

# set pins for cols as inputs
col_pins = [Pin(pin_name, mode=Pin.IN, pull=Pin.PULL_DOWN) for pin_name in cols]

def init():
    for row in range(0,4):
        for col in range(0,4):
            row_pins[row].value(0)

def scan(row, col):
    """ scan the keypad """

    # set the current column to high
    row_pins[row].value(1)
    key = None

    # check for keypressed events
    if col_pins[col].value() == KEY_DOWN:
        key = KEY_DOWN
#        print(str(col_pins[col].value())+"   1")
    if col_pins[col].value() == KEY_UP:
        key = KEY_UP
#        print(str(col_pins[col].value())+"   2")
    row_pins[row].value(0)

    # return the key state
    return key

def get_keycodes():
    # set all the columns to low
    init()
    output = ""
    prev = ""
    
    count=-1
    last_char = '='
    while True:
        for row in range(4):
            for col in range(3):
                key = scan(row, col)
                if key == KEY_DOWN:
                    key = KEY_UP
                    chara = keys[row][col]    
                    
                    #Moje da se dobavi '.' ama e kusno
                    if chara == '*':
                        output += chr(ord(last_char)+count)
                        print(output)
                        count=-1
                    elif chara == ' ':
                        output += " "
                        print(output)
                        count=-1
                    elif chara == '1':
                        return output
                    elif last_char == chara:
                        count+=1
                        if count >= 3:
                            count=0
                    elif last_char != chara:
                        last_char=chara
                        count=0
                    
                    #print(chara,count)
                    time.sleep(0.3)

def print_lcd_message(msg):
    lcd.clear()
    lcd.message(msg)
    sleep(1.0)
    for i in range(len(msg)):
        sleep(0.25)
        lcd.move_right()

station = network.WLAN(network.STA_IF)
station.active(True)
if not station.isconnected():
    station.connect("Ndd_wrt", "tania123")
print(station.isconnected())
print(station.ifconfig())

header = {"name": "indiana", "language": "en", "reciever":"", "msg":""}  # a real dict.
init_header = {"name": "indiana", "language": "en"}

ClientMultiSocket = socket.socket()
host = '192.168.1.33'
port = 2004

print('Waiting for connection response')

try:
    ClientMultiSocket.connect((host, port))
except OSError as e:
    print(str(e))

res = ClientMultiSocket.recv(1024)

def send_init_msg():
    data = json.dumps(init_header)
    data = data.encode('utf8')
    ClientMultiSocket.send(data)

def send_msg():
    while True:
        #keyboard
        Resiver = input("Send to: ")
        Input = input("Your message: ")
        print(type(Resiver),type(Input))
        header["reciever"] = Resiver
        header["msg"] = Input
        
        #keypad
        # a = get_keycodes()
        # time.sleep(1)
        # b = get_keycodes()
        # time.sleep(1)
        # header["reciever"] = str(a)
        # header["msg"] = str(b)
        
        time.sleep(1)
        data = json.dumps(header)
        ClientMultiSocket.send(data)

def resive_msg():
    while True:
        res = ClientMultiSocket.recv(1024)
        msg = res.decode('utf-8')
        print(msg) #console
        print_lcd_message(msg) #lcd



send_init_msg()
start_new_thread(resive_msg, ())
send_msg()

ClientMultiSocket.close()
