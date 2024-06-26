#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.PULL)
socket.bind("tcp://*:65435")

print("Dummy server started ;-)")

while True:
    #  Wait for next request from client
    message = socket.recv()
    print("Received request: %s" % (message))

    #  Do some 'work'
    #time.sleep(1)
