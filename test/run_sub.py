import zmq
from time import sleep

context = zmq.Context()
socket = context.socket(zmq.SUB)
# We can connect to several endpoints if we desire, and receive from all.
socket.connect("tcp://127.0.0.1:2000")

# We must declare the socket as of type SUBSCRIBER, and pass a prefix filter.
# Here, the filter is the empty string, wich means we receive all messages.
# We may subscribe to several filters, thus receiving from all.
socket.setsockopt(zmq.SUBSCRIBE, b"")

message = socket.recv_pyobj()
print(message)
# print(message.get(1)[2])
# recfile(message.get(1)[2])
