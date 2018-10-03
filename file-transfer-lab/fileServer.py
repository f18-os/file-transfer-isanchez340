#! /usr/bin/env python3

# Echo server program

import socket, sys, re
sys.path.append("../lib")       # for params
import params

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "fileserver"
paramMap = params.parseParams(switchesVarDefaults)

listenPort = paramMap['listenPort']
listenAddr = ''       # Symbolic name meaning all available interfaces

if paramMap['usage']:
    params.usage()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((listenAddr, listenPort))
s.listen(1)              # allow only one outstanding request
# s is a factory for connected sockets

conn, addr = s.accept()  # wait until incoming connection request (and accept it)
print('Connected by', addr)
filename = conn.recv(1024).decode()
f = open("Received_" + filename,'wb')

file = conn.recv(1024)
while file:
        print("Receiving " + filename)
        f.write(file)
        file = conn.recv(1024)

print("Received " + filename)
conn.shutdown(socket.SHUT_WR)
conn.close()
