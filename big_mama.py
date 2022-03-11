import socket
import os
from _thread import *
ServerSideSocket = socket.socket()


#host = '127.0.0.1'
host = '192.168.1.20'
port = 2004

client_host = '192.168.1.33'
client_port = 2004

try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Socket is listening..')
ServerSideSocket.listen(5)

def translete_msg(msg):
    return msg

def send_msg_to_pager(msg):
    ClientMultiSocket = socket.socket()
    try:
        ClientMultiSocket.connect((client_host, client_port))
    except socket.error as e:
        print(str(e))
    client_res = ClientMultiSocket.recv(1024)
    ClientMultiSocket.send(str.encode(msg))
    ClientMultiSocket.close()


def multi_threaded_client(connection):
    
    connection.send(str.encode('Server is working:'))

    while True:
        
        data = connection.recv(2048)
        response = 'Server message: ' + data.decode('utf-8')
        
        if not data:
            break

        msg_out = translete_msg(str(response))
        #mabe not working check old version
        print(msg_out)
        send_msg_to_pager(msg_out)
        #can be removed
        connection.sendall(str.encode(msg_out[0]))

    connection.close()

ThreadCount = 0

def make_server():
    global ThreadCount 
    Client, address = ServerSideSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(multi_threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))





while True:    
    make_server()

ServerSideSocket.close()
