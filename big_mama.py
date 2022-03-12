import socket
import json
import os
from _thread import *
import threading

ServerSideSocket = socket.socket()
ThreadCount = 0

host = '192.168.1.20'
port = 2004


try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))
print('Socket is listening..')
ServerSideSocket.listen(5)

clients = set()
clients_lock = threading.Lock()


def translete_msg(json):
    return json

def save_init_msg(json):
   print(json) 

def send_msg(json, connection):
    global clients_lock
    msg = json['name'] + ': ' + translete_msg(str(json['msg'])) + '\n'
    with clients_lock:
        for curr in  clients:
            if(curr!=connection):
                curr.sendall(msg.encode())


def multi_threaded_client(connection):
    global clients_lock

    connection.send(str.encode('Server is working:'))
    
    with clients_lock:
        clients.add(connection)
    try:
        while True:
            data = connection.recv(2048)
            
            if not data:
                break
              
            response = json.loads(data)
            
            print (len(response)) 

            if len(response) == 2:
                save_init_msg(response)

            else:
                send_msg(response, connection)
           
    finally:
        with clients_lock:
            clients.remove(connection)
            connection.close() 


def make_server():
    global ThreadCount
    Client, address = ServerSideSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    
    start_new_thread(multi_threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))

#Program loop:
while True:    
    make_server()
ServerSideSocket.close()
