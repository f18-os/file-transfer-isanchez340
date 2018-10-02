#! /usr/bin/env python3

import sys, re, socket, codecs
sys.path.append("../lib") #for params
import params

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "fileClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage  = paramMap["server"], paramMap["usage"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)



file = input("Enter file name")
with open(file, 'rb') as fp:
  outMessage= fp.read()

while len(outMessage):
    print("sending '%s'" % file)
    bytesSent = s.send(outMessage.encode())
    outMessage = outMessage[bytesSent:]

data = s.recv(1024).decode()
print("Received '%s'" % data)

while len(outMessage):
    print("sending '%s'" % file)
    bytesSent = s.send(outMessage.encode())
    outMessage = outMessage[bytesSent:]

s.shutdown(socket.SHUT_WR)  # no more output

while 1:
    data = s.recv(1024).decode()
    print("Received '%s'" % data)
    if len(data) == 0:
        break
print("Zero length read.  Closing")
s.close()
