import socket, sys
import distanceope
import gps
import time
import random

situate = ["unstable”,”RightShift”,”LeftShift”,”Hinder”,”LowPower","unknown”,”OutOfRange”,”Stable!”,”Stable!”,”Stable!”,”Stable!”,”Stable!"]
startGPS = getdata(initialise()) #Get GPS data of Starting point

#Initial
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
    sys.stderr.write("[ERROR] %s\n" % msg[1])
    sys.exit(1)

try:
    sock.connect((’192.168.0.11’, 54321))
except socket.error, msg:
    sys.stderr.write("[ERROR] %s\n" % msg[1])
    exit(1)




while True:
	if csock.recv(1024) == "Launching":
		start = time.clock()

	    #avoid of traffic accident
	    if get_distance() < 20:
		sock.send("Obstacle")
		while get_distance() < 50:
		    sock.send("Go Back")
		    #to do: control motor to go back
		sock.send("Maintain safe distance")
	    if time.clock() - start >=2: #Report in every 2 sec
	        num = random.randint(0,11)
	        msg = situate[num]
	        sock.send(msg)
	        print sock.recv(1024)
	        start = time.clock()
#sock.close()
