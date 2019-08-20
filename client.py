#!/usr/bin/python3
# PyIRC - Simple IRC Client written in python.
# Author: ubdussamad <[firstname][at][google]>
# Under MIT License
# Ref: Aug 4 , 2019

# Lib Imports
import socket
import uuid
import time

# Config
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Create the socket
# AF_INET(ipv4) Alt: ipv6
# SOCK_STREAM(TCP) Alt: UDP
clientsocket.connect((socket.gethostname(), 6969))


# Constants
CONTENT_BUFFER_SIZE = 16 # Bytes

# ID Genration
CLIENT_ID = uuid.uuid1().bytes
WEB_ID = None
REGISTERED = False
print("Welcome to PyIRC Client")

while True:
    # Loop Indefinitively

    # Send Your Client ID
    if not REGISTERED:
        clientsocket.send(bytes(str(len(CLIENT_ID)),'utf-8'))
        clientsocket.send(bytes(CLIENT_ID.hex(),'utf-8'))
        
    if clientsocket.recv(3).decode('utf-8') == "OK!":
        print("Sucessful Registered on IRC Server!")
        REGISTERED = True
    time.sleep(8)
    print("Stuck 2")
    clientsocket.send(bytes(str(len("Let's Mate! :)")),'utf-8'))
    clientsocket.send(bytes("Let's Mate! :)",'utf-8'))
    print("Stuck 1")
    
    
