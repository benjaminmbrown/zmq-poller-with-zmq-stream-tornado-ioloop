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
		topic =  random.randrange(7,10)
		messagedata = "server#%s" % publisher_id
		print "%s %s" % (topic, messagedata)
		socket.send("%d %s" % (topic, messagedata))
		time.sleep(1)

def getcommand(msg):
	print "received control command : %s" % msg
	if msg[0] == "Exit":
		print "Recevied exit command, client now stopping receiving"
		should_continue = false
		ioloop.IOLoop.instance().stop()

def process_message(msg):
	print "Processing ... %s" % msg


def client(port_push, port_sub):
	context = zmq.Context()

	socket_pull = context.socket(zmq.PULL)
	socket_pull.connect("tcp://localhost:%s" % port_push)
	
	#use ZMQStream class ot register callbacks - no explicit socket handlers here
	stream_pull = zmqstream.ZMQStream(socket_pull)
	stream_pull.on_recv(getcommand)
	print "Connected to server on port: ", port_push


	socket_sub = context.socket(zmq.SUB)
 	socket_sub.connect("tcp://localhost:%s" % port_sub)
 	socket_sub.setsockopt(zmq.SUBSCRIBE,"9")

 	stream_sub =zmqstream.ZMQStream(socket_sub)
 	stream_sub.on_recv(process_message)

 	print "Connected to publisher with port #: ", port_sub
 	ioloop.IOLoop.instance().start()
 	print "Worker has stopped message processing" 


if __name__ == "__main__":
	server_push_port = "5556"
	server_pub_port = "5558"
	Process(target=push_server, args=(server_push_port,)).start()
	Process(target=pub_server, args=(server_pub_port,)).start()
	Process(target=client, args=(server_push_port,server_pub_port)).start()