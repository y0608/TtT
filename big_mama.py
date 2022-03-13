from operator import imod
import socket
from _thread import *
import threading
import json
import os
from argostranslate import package, translate
from socketio import ClientNamespace
from host import host,port

ServerSideSocket = socket.socket()
ThreadCount = 0

def translate_msg(message, from_language, to_language):
    from argostranslate import package, translate

def translate_msg(msg, fromL, toL):

    first = fromL.upper()
    second = toL.upper()
    output = ""
    temp = ""
    languages = {"EN": 0, "AR": 1, "ZH": 2, "FR": 3,
                 "DE": 4, "IT": 5, "JA": 6, "PR": 7, "RU": 8, "ES": 9}
    language_installers = {
        languages["EN"] * 10 + languages["AR"]: 'models/en_ar.argosmodel.zip',
        languages["EN"] * 10 + languages["ZH"]: 'models/en_zh.argosmodel.zip',
        languages["EN"] * 10 + languages["FR"]: 'models/en_fr.argosmodel.zip',
        languages["EN"] * 10 + languages["DE"]: 'models/en_de.argosmodel.zip',
        languages["EN"] * 10 + languages["IT"]: 'models/en_it.argosmodel.zip',
        languages["EN"] * 10 + languages["PR"]: 'models/en_pr.argosmodel.zip',
        languages["EN"] * 10 + languages["RU"]: 'models/en_ru.argosmodel.zip',
        languages["EN"] * 10 + languages["ES"]: 'models/en_es.argosmodel.zip',
        languages["EN"] * 10 + languages["JA"]: 'models/en_ja.argosmodel.zip',
        languages["AR"] * 10 + languages["EN"]: 'models/ar_en.argosmodel.zip',
        languages["ZH"] * 10 + languages["EN"]: 'models/zh_en.argosmodel.zip',
        languages["FR"] * 10 + languages["EN"]: 'models/fr_en.argosmodel.zip',
        languages["DE"] * 10 + languages["EN"]: 'models/de_en.argosmodel.zip',
        languages["IT"] * 10 + languages["EN"]: 'models/it_en.argosmodel.zip',
        languages["PR"] * 10 + languages["EN"]: 'models/pr_en.argosmodel.zip',
        languages["RU"] * 10 + languages["EN"]: 'models/ru_en.argosmodel.zip',
        languages["ES"] * 10 + languages["EN"]: 'models/es_en.argosmodel.zip',
        languages["JA"] * 10 + languages["EN"]: 'models/ja_en.argosmodel.zip'
    }

    # for value in language_installers.values():
    #     if value != 0:
    #         package.install_from_path(value)

    if first not in ["EN", "AR", "ZH", "FR", "DE", "IT", "PR", "RU", "ES", "JA"] or second not in ["EN", "AR", "ZH", "FR", "DE", "IT", "PR", "RU", "ES", "JA"]:
        print("oopsie")
    if first==second:
        return msg
    elif first != "EN" and second != "EN":
        installed_languages = translate.get_installed_languages()
        translation = installed_languages[languages[first]].get_translation(
            installed_languages[languages["EN"]])
        translation2 = installed_languages[languages["EN"]].get_translation(
            installed_languages[languages[second]])

        temp += translation.translate(msg.strip()) + "\n"

        output += translation2.translate(temp.strip()) + "\n"
    else:
        installed_languages = translate.get_installed_languages()

        translation = installed_languages[languages[first]].get_translation(
            installed_languages[languages[second]])

        output += translation.translate(msg.strip()) + "\n"

    return output


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
client_to_language = {}

def translate_pager_msg(from_language,to_language, message):
    print(from_language + '   ' + to_language)
    msg = translate_msg(message, from_language, to_language)
    return msg

def save_init_msg(json, connection):
    name_to_client[json["name"]] = connection
    name_to_language[json["name"]] = json["language"]
    client_to_language[connection] = json['language'] 

def send_msg(connection,json):
    global clients_lock
    
    if json['reciever'] == 'all':
        for curr in clients:
            if curr != connection:
                msg = json['name'] + ': ' + translate_pager_msg(json["language"], client_to_language[curr],json["msg"]) + '\n'
                curr.sendall(msg.encode())
        return None
    elif json['reciever'] not in name_to_client:
        print("there is nobody like that")
        return None
    else:
        translated = translate_pager_msg(json["language"],name_to_language[json["reciever"]],json["msg"])
        
        #server prints
        print("Original: " + json['name'] + '--->' + json['reciever'] + " " + json['msg'])
        print("Sent: " + json['name'] + '--->' + json['reciever'] + " " + translated)
        
        msg = json['name'] + ': ' + translated + '\n'
        
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
                send_msg(connection,response)
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


# Program loop:
while True:
    make_server()
ServerSideSocket.close()
