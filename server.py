import socket
import pickle
from threading import Thread
from tools import *
from config import *
from betterlog import log

# Setting up server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
log('Successfully created server_socket').header()
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
log(f'Successfully binded to {SERVER_HOST}:{SERVER_PORT}').header()
server_socket.listen()
log(f'Server is now listening for connections!').header()

clients_list = {}


def greeting(client_socket, address):
    username_header = client_socket.recv(HEADER_SIZE)
    username = client_socket.recv(get_length(decode(username_header)))
    return {
        'username': decode(username),
        'socket': client_socket
    }



def get_connections():
    while True:
        client_socket, address = server_socket.accept()
        user = greeting(client_socket, address)
        clients_list[user['username']] = user
        Thread(target=incomming_messages, args=(client_socket,)).start()
        log(f'Connection from {address[0]}:{address[1]} has been established!').info()
        user = {
            'username': user['username'],
        	'message': 'User Has Joined The Chat!'
        }
        user = pickle.dumps(user)
        for client in clients_list:
            client = clients_list[client]
            try:
                client['socket'].send(encode(create_header(user))+user)
            except BrokenPipeError:
            	del clients_list[client]
Thread(target=get_connections).start()

def incomming_messages(client_socket):
    while True:
        message_header = client_socket.recv(HEADER_SIZE)
        if len(message_header):
            message = decode(client_socket.recv(get_length(decode(message_header))))
            for client in clients_list:
                if clients_list[client]['socket'] == client_socket:
                    user = {
                        'username': clients_list[client]['username'],
                        'message' : message
                    }
            user = pickle.dumps(user)
            for client in clients_list:
                client = clients_list[client]
                try:
                    client['socket'].send(encode(create_header(user))+user)
                except:
                    pass
while True:
    message = input('Send message to all: ')
    user = {
        'username': 'Announcements',
        'message': message
    }
    user = pickle.dumps(user)
    for client in clients_list:
        client = clients_list[client]
        try:
            client['socket'].send(encode(create_header(user))+user)
        except BrokenPipeError:
            pass
