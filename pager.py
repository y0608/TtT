import socket
from _thread import *
import json

header = {"name": "Radi", "language": "en", "msg":""}  # a real dict.

ClientMultiSocket = socket.socket()
host = '192.168.1.20'
port = 2004

print('Waiting for connection response')

try:
    ClientMultiSocket.connect((host, port))
except socket.error as e:
    print(str(e))

res = ClientMultiSocket.recv(1024)


def send_msg():
    while True:
        Input = input()  # TODO: 'your name: ... '
        header["msg"] = Input
        data = json.dumps(header)
        ClientMultiSocket.send(bytes(data,encoding="utf-8"))

def resive_msg():
    while True:
        res = ClientMultiSocket.recv(1024)
        print(res.decode('utf-8'))


start_new_thread(resive_msg, ())
send_msg()

ClientMultiSocket.close()
