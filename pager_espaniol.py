import socket
from _thread import *
import json 
import time
from host import host,port

ClientMultiSocket = socket.socket()


header = {"name": "Markos", "language": "es", "reciever":"", "msg":""}  # a real dict.
init_header = {"name": "Markos", "language": "es"}

demo1 = "hola mi nombre es Markos"
demo2 = "No hay combustible"
demo3 = "¿Dónde está mi cepillo de dientes?"
demos = [demo1, demo2, demo3]

recievers = ['Pier','Marioo','Ivanushka']

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
