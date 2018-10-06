#! /usr/bin/env python3

# Echo server program

import socket, sys, re, os
sys.path.append("../lib")       # for params
import params

nofileerror = 0;
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
while True:
    conn, addr = s.accept()  # wait until incoming connection request (and accept it)

    if not os.fork():

        print('Connected by', addr)

        filename = conn.recv(1024).decode()

        if os.path.isfile("Received_" + filename):
            print("file is found in server, please rename file before sending")
            filename = "nullerrorfilenotfound"

        if filename == "nullerrorfilenotfound":
            nofileerror = 1

        f = open("Received_" + filename,'wb')
        try:
            file = conn.recv(1024)
            while file:
                print("Receiving '%s'" % "Received_" + filename)
                f.write(file)
                file = conn.recv(1024)
        except:
            print("disconnected")
            conn.shutdown(socket.SHUT_WR)
            conn.close()
            sys.exit(0)

        print("Received '%s'" % filename)
        conn.shutdown(socket.SHUT_WR)
        conn.close()
        if nofileerror:
            os.remove("Received_nullerrorfilenotfound")
