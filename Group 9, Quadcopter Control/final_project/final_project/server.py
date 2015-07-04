import socket, sys, time

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
    sys.stderr.write("[ERROR] %s\n" % msg[1])
    sys.exit(1)

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #reuse tcp
sock.bind(('localhost', 54321))
sock.listen(5)
cmd = ''
#sock.settimeout(10)
while True:
    (csock, adr) = sock.accept()
    print "Client Info: ", csock, adr
    print "Plz enter A)launching B)Landing:"
    while cmd != 'A':
        print "Plz enter A)launching B)Landing:"
        cmd = raw_input()
    while True:
        msg = csock.recv(1024)
        if not msg:
            print "ERROR:Lose connection with device!!"
            break
        else:
            print "Client send: " + msg
            if msg == "unstable":
                csock.send("Reset to the least stable state")
            elif msg == "rightShift":
                csock.send("Add power to the right side")
            elif msg == "leftShift":
                csock.send("Add power to the left side")
            elif msg == "hinder":
                csock.send("Turn right/left")
            elif msg == "lowPower":
                csock.send("Return voyage")
            elif msg == "unknown":
                csock.send("Reset to the least stable state")
            elif msg == "outOfRange":
                csock.send("Check gps")
            else:
                csock.send("good job")
#csock.close()