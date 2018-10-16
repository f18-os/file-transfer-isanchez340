#! /usr/bin/env python3

# Echo server program

import socket, sys, re, os, time
from threading import Thread
sys.path.append("../lib")       # for params
import params

nofileerror = 0;    # error state variable
switchesVarDefaults = (     # socket setup and connection stuff
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
s.listen(1)     # allow only one outstanding request
print("Connected to:", s)
# s is a factory for connected sockets

class ServerThread(Thread):
    requestCount = 0
    def __init__(self, sock):
        Thread.__init__(self, daemon=True)
        self.start()
    def run(self):
        while True:
            filename = conn.recv(1024).decode()     # receives file name
            while os.path.isfile("Received_" + filename):  # checks if file is in folder and handles the situation accordingly
                filename = "(1)" + filename    # renames file for error state
            if filename == "nullerrorfilenotfound":     # error state handing
                nofileerror = 1
            f = open("Received_" + filename,'wb')
            try:    # recieves file and if diconnected prints message and exits
                file = conn.recv(1024)
                while file:
                    print("Receiving '%s'" % "Received_" + filename)
                    f.write(file)
                    file = conn.recv(1024)

                requestNum = ServerThread.requestCount
                time.sleep(0.001)
                ServerThread.requestCount = requestNum + 1
            except:
                print("disconnected")
                conn.shutdown(socket.SHUT_WR)
                conn.close()
                sys.exit(0)

            print("Received '%s'" % filename)   # socket cleanup and error file removal if needed
            conn.shutdown(socket.SHUT_WR)
            conn.close()
            if nofileerror:
                os.remove("Received_nullerrorfilenotfound")
            try:
                os.remove("Received_")
            except:
                sys.exit(0)

while True:
    conn, addr = s.accept()  # wait until incoming connection request (and accept it)
    ServerThread(conn)
