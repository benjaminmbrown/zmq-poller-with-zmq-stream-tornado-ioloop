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

def pub_server(port="5558"):
	context = zmq.Context()
	socket = context.socket(zmq.PUB)
	socket.bind("tcp://*:%s" % port)
	publisher_id = random.randrange(0,9999)
	print "Created publisher server with id: ", publisher_id
	print "Running server on port: ", port
	for reqnum in range(100):
		topic =  random.randrange(8,10):
		messagedata = "server#%s" % publisher_id
		print "%s %s" % (topic, messagedata)
		socket.send("%d %s" % (topic, messagedata)
		time.sleep(1)

def getcommand(msg):
	print "received control command : %s" % msg
	if msg[0] == "Exit":
		print "Recevied exit command, client now stopping receiving"
		should_continue = false
		ioloop.IOLoop.instance().stop()

def process_message(msg):
	print "Processing ... %s" % msg

