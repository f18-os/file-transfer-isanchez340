#! /usr/bin/env python3

# Echo client program
import socket, sys, re
sys.path.append("../lib")       # for params
import params

switchesVarDefaults = (                                 # socket and connection setup before file transfer
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "framedClient"
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

file = input("Enter file name including extension eg. ""graceful.gif ")

try:                # tries to open file and if not found send error name so the server handles the error
    outfile = open(file, 'rb')
except:
    print("file not found")
    s.send("nullerrorfilenotfound".encode())
    s.shutdown(socket.SHUT_WR)
    s.close()
    sys.exit(0)

try:                # trys to send file and if error occurs like disconnection, prints out message and exits program
    s.send(file.encode())

    sending = outfile.read(1024)
    while len(sending):
        print("sending '%s'" % file)
        s.send(sending)
        sending = outfile.read(1024)
except:
    print("Disconnected")
    s.shutdown(socket.SHUT_WR)  # no more output
    s.close()
    sys.exit(0)

print("sent '%s'" % file)

s.shutdown(socket.SHUT_WR)  # no more output
s.close()
