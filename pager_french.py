import socket
from _thread import *
import json 
import time

ClientMultiSocket = socket.socket()
host = '192.168.1.33'
port = 2004

header = {"name": "Pier", "language": "fr", "reciever":"", "msg":""}  # a real dict.
init_header = {"name": "Pier", "language": "fr"}

demo1 = "bonjour je m'appelle Pier et j'adore Paris"
demo2 = "Merci beaucoup"
demo3 = "n'appuyez pas sur le bouton"
demos = [demo1, demo2, demo3]

recievers = ['Markos','Marioo','Ivanushka']

print('Waiting for connection response')

try:
    ClientMultiSocket.connect((host, port))
except socket.error as e:
    print(str(e))

res = ClientMultiSocket.recv(1024)

def send_init_msg():
    data = json.dumps(init_header)
    ClientMultiSocket.send(bytes(data,encoding="utf-8"))

def send_msg():
    i = 0
    while True:
        header["reciever"] = recievers[i]
        header["msg"] = demos[i]
        data = json.dumps(header)
        ClientMultiSocket.send(bytes(data,encoding="utf-8"))
        i+=1
        if i == 3:
            i = 0
        time.sleep(10)
        
def receive_msg():
    while True:
        res = ClientMultiSocket.recv(1024)
        print(res.decode('utf-8'))



send_init_msg()
start_new_thread(receive_msg, ())
send_msg()

ClientMultiSocket.close()
