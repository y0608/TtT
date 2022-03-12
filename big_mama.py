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


#Client:
def multi_threaded_client(connection):
    global clients_lock

    connection.send(str.encode('Server is working:'))
    
    with clients_lock:
        clients.add(connection)
    try:
        while True:
            data = connection.recv(2048)
            #response = data.decode('utf-8') 
             
            response = json.loads(data)
            print(response['name'] + ': ' + response['msg'])

            if not data:
                break
            
            msg_out = translete_msg(str(response)) + '\n'
            
            with clients_lock:
                for curr in  clients:
                    if(curr!=connection):
                        curr.sendall(msg_out.encode())
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
