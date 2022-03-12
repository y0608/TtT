import socket
from _thread import *
import json

m = {"name": "Radi", "language": "es"}  # a real dict.
data = json.dumps(m)

ClientMultiSocket = socket.socket()
host = '192.168.1.33'
port = 2004

print('Waiting for connection response')

try:
    ClientMultiSocket.connect((host, port))
except socket.error as e:
    print(str(e))

res = ClientMultiSocket.recv(1024)


def send_msg():
    while True:
        Input = input('You: ')  # TODO: 'your name: ... '
        ClientMultiSocket.send(bytes(data,encoding="utf-8"))


def resive_msg():
    while True:
        res = ClientMultiSocket.recv(1024)
        print(res.decode('utf-8'))


start_new_thread(resive_msg, ())
send_msg()

ClientMultiSocket.close()
