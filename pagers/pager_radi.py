import socket
from _thread import *
import json 
from host import host,port

ClientMultiSocket = socket.socket()


header = {"name": "RADI", "language": "es", "reciever":"", "msg":""}  # a real dict.
init_header = {"name": "RADI", "language": "es"}

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
    while True:
        Reciever = input()
        Input = input()
        header["reciever"] = Reciever
        header["msg"] = Input

        data = json.dumps(header)
        ClientMultiSocket.send(bytes(data,encoding="utf-8"))

def receive_msg():
    while True:
        res = ClientMultiSocket.recv(1024)
        print(res.decode('utf-8'))



send_init_msg()
start_new_thread(receive_msg, ())
send_msg()

ClientMultiSocket.close()
