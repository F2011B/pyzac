import zmq
from time import sleep

context = zmq.Context()

socket = context.socket(zmq.PUB)
socket.bind("tcp://127.0.0.1:2000")

# Allow clients to connect before sending data
sleep(10)
socket.send_pyobj(20)
