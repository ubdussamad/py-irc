#!/usr/bin/python3
# PyIRC - Simple IRC server written in python.
# Author: ubdussamad <[firstname][at][google]>
# Under MIT License
# Ref: Aug 4 , 2019
# samad-Latitude-E6400

# Lib Imports
import socket
import time
import select

# Config
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Create the socket
# AF_INET(ipv4) Alt: ipv6
# SOCK_STREAM(TCP) Alt: UDP
server_socket.bind((socket.gethostname(), 6969)) # Workin on Localhost @:6969
server_socket.listen(5) # Base Queue of 5 Clients


# Constants
CONTENT_BUFFER_SIZE =  16#Bytes

# Runtime Data
SOCKETS = [server_socket]
STATIONS = {}

print("Welcome to PyIRC Server!")


def rscv(client_socket):
    # Max Content size is CONTENT_BUFFER_SIZE
    try:
        message_header = client_socket.recv(CONTENT_BUFFER_SIZE)
        if not len(message_header):return False
        print(message_header)
        message_width = int(message_header.decode('utf-8').strip())
        return {'header': message_header,
                'data': client_socket.recv(message_width)}
    except Exception as err:
        print(err)
        print("Client Dropped Unexpectedly. :(")
        return False





while True: # Main Event Loop
    ''' Tasks:
    * Handle a Register Request ( Register a new client in the IRC )
    * Handle Postings
    * Handle Chat Groups
    '''
    read_sockets, x , exception_sockets = select.select(SOCKETS,[],SOCKETS)
    # Iterate over notified sockets
    for notified_socket in read_sockets:
        # If notified socket is a server socket - new connection, accept it
        if notified_socket == server_socket:
            # New connection Request
            client_socket, client_address = server_socket.accept()
            # Wait for client to send their UID
            u_id = rscv(client_socket)
            if not u_id:continue
            SOCKETS.append(client_socket)
            STATIONS[client_socket] = [u_id]
            print("\n%1.f: %s:%d, uid: %s\n"% (time.time(),
                                               *client_address ,
                                               u_id['data'].hex()))
            client_socket.send(bytes("OK!",'utf-8'))
        else:
            # Receive message
            message = rscv(notified_socket)
            if message is False:
                print('Closed connection from: {}'.format(STATIONS[notified_socket][0]['data'].hex()))
                SOCKETS.remove(notified_socket)
                del STATIONS[notified_socket]
                
            try:
                print(message['data'].decode('utf-8'))
            except:
                print("Client Error!")
            # Get user by notified socket, so we will know who sent the message
            '''user = clients[notified_socket]

            print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')

            # Iterate over connected clients and broadcast message
            for client_socket in clients:

                # But don't sent it to sender
                if client_socket != notified_socket:

                    # Send user and message (both with their headers)
                    # We are reusing here message header sent by sender, and saved username header send by user when he connected
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
'''

    # It's not really necessary to have this, but will handle some socket exceptions just in case
    for notified_socket in exception_sockets:

        # Remove from list for socket.socket()
        sockets_list.remove(notified_socket)

        # Remove from our list of users
        del clients[notified_socket]
