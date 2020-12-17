# Initializer.py (OTP)
# Tyler Reece
# CS548 Final Project

# Simulates the role of a "trusted initializer" in the 1-2 OT
# based on the OTP, as specified by Ron Rivest in 1999. This
# script should be run AFTER both Sender.py and Receiver.py have
# already been run and initialized. 

# Specifically, this script establishes a Publish connection at
# the address ADDR using ZeroMQ, generates a random r0 and r1 of length 
# MAX_MSG_LEN, and a d value in {0, 1}. r0 and r1 are published
# to the sender and rd and d are published to the receiver.


import zmq
import random
import sys
import time
import string


def main():
	t = Initializer()
	t.set_initial_conditions()


class Initializer:

	# Defaults
	ADDR = "tcp://127.0.0.1:5556"
	MAX_MSG_LEN = 50

	def __init__(self):
		# Set up ZeroMQ in PUB/SUB format
		self.context = zmq.Context()
		self.socket = self.context.socket(zmq.PUB)
		self.socket.bind(self.ADDR)
		time.sleep(1) 

	def compute_r0r1(self):
		# Generate random pad pair (r0, r1) 
		self.r0 = ''.join((random.choice(string.ascii_letters + string.digits) for i in range(50)))
		self.r1 = ''.join((random.choice(string.ascii_letters + string.digits) for i in range(50)))
		self.r0r1 = (self.r0, self.r1)
		print("r0:", self.r0)
		print("r1:", self.r1)

	def initialize_sender(self):
		# Publish (r0, r1) to the sender
		topic = "Sender"
		messagedata = self.r0 + "," + self.r1
		self.socket.send_string("%s %s" % (topic, messagedata))
		time.sleep(1)

	def compute_d_rd(self):
		# Generate random d in {0, 1} and select rd from (r0, r1)
		self.d = random.randint(0, 1)
		self.rd = self.r0r1[self.d]
		print("d:", str(self.d))
		print("rd:", self.rd)

	def initialize_receiver(self):
		# Publish d and rd to receiver
		topic = "Receiver"
		messagedata = str(self.d) + "," + self.rd
		self.socket.send_string("%s %s" % (topic, messagedata))

	def set_initial_conditions(self):
		# Perform all necessary tasks to set initial conditions
		# for the OT to proceed. After setting initial conditions,
		# the Initializer ends and the OT proceeds through 
		# communication between Sender and Receiver alone. 
		print("Computing r0 and r1...")
		self.compute_r0r1()
		print("Initializing sender...")
		self.initialize_sender()
		print("Computing d and rd...")
		self.compute_d_rd()
		print("Initializing receiver...")
		self.initialize_receiver()
		print("Initialization complete!")

main()