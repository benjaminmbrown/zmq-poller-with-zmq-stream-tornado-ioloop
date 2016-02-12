import zmq
import time
import sys
import random

#allow multiprocessing
from multiprocessing import Process

from zmq.eventloop import ioloop, zmqstream
ioloop.install()

def push_server(port="5556"):
	context=zmq.Context()
	socket =context.socket(zmq.PUSH)
	socket.bind("tcp://*:%s" % port)

	print "Started server on port: ", port


	for reqnum in range(10):
		if reqnum < 6:
			socket.send("Continue")
		else:
			socket.send("Next")
			break
		time.sleep(1)



