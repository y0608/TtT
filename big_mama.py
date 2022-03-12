import socket
from _thread import *
import threading
import json
import os

ServerSideSocket = socket.socket()
ThreadCount = 0

host = '192.168.1.33'
port = 2004

try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))
print('Socket is listening..')
ServerSideSocket.listen(5)

clients = set()
clients_lock = threading.Lock()

name_to_client = {}
name_to_language = {}

def translate_msg(json):
    return json

def save_init_msg(json, connection):
    name_to_client[json["name"]]=connection
    name_to_language[json["name"]]=json["language"]


def send_msg(json, connection):
    global clients_lock
    msg = json['name'] + ': ' + translate_msg(str(json['msg'])) + '\n'
    
    if json['reciever'] not in name_to_client:
        msg = translate_msg("Reciever not available") + '\n'
        connection.sendall(msg.encode())
    else:
        with clients_lock:
            name_to_client[json['reciever']].sendall(msg.encode())


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

            if len(response) == 2:
                save_init_msg(response, connection)

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