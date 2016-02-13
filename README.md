# zmq-poller-with-zmq-stream-tornado-ioloop
ZMQ Poller that uses ZMQStream and Torndado's ioloop for handling poll events on ZMQ sockets

<br>This poller uses ZMQStream to handle polling events from ZeroMQ sockets. This also enables usage of callbacks to send & receive data. There's a push server that sends out "Continue" or "Stop" messages which the worker client reads and uses to continue work or not.

<br/>
To run: python zmq-stream-poller.py