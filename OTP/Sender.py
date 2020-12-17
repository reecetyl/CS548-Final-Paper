# Sender.py (OTP)
# Tyler Reece
# CS548 Final Project

# Simulates the role of Sender (Alice) in the 1-2 OT
# based on the OTP, as specified by Ron Rivest in 1999. This
# script should be run BEFORE Initializer.py (and along with
# Receiver.py).

# Specifically, this script establishes a Subscribe connection at
# the address ADDR using ZeroMQ, and receives the (r0, r1) pad pair
# from the Initializer. The rest of the 1-2 OT protocol is followed,
# including receiving e from the Receiver, and computing the (f0, f1) pair.

import sys
import zmq
import time

def main():
	s = Sender()
	s.conductOT()

class Sender:

	# Defaults
	ADDR = "tcp://127.0.0.1:5556"
	ADDR2 = "tcp://*:3434"
	MAX_MSG_LEN = 50

	def __init__(self):
		# Receive m0 and m1 as keyboard input from user and establish
		# ZeroMQ connection in SUB format
		print("m0 and m1 can be any ASCII values")
		print("MAX_MSG_LEN = ", self.MAX_MSG_LEN)
		m0 = input("Please enter m0: ")
		m1 = input("Please enter m1: ")
		assert(len(m0) <= MAX_MSG_LEN and len(m1) <= MAX_MSG_LEN)
		self.m0 = self.encode_msg(m0)
		self.m1 = self.encode_msg(m1)
		self.context = zmq.Context()
		self.socket = self.context.socket(zmq.SUB)
		self.socket.connect(self.ADDR)

	def encode_msg(self, m):
		# encodes messages as concatenated ASCII values
		m_total = ""
		for c in m:
			ascii_val = str(ord(c))
			while len(ascii_val) != 3:
				ascii_val = "0" + ascii_val
			m_total += ascii_val
		return int(m_total)

	def receive_initial_conditions(self):
		# decodes messages from concatenated ASCII values to plain text
		topicfilter = "Sender"
		self.socket.setsockopt_string(zmq.SUBSCRIBE, topicfilter)
		string = self.socket.recv_string()
		topic, messagedata = string.split()
		self.r0, self.r1 = messagedata.split(",")
		self.r0r1 = (self.r0, self.r1)
		self.socket.close()

	def connect_to_receiver(self):
		# Establish new line of communication with Receiver
		self.socket = self.context.socket(zmq.REP)
		self.socket.bind(self.ADDR2)

	def receive_e(self):
		# Get e from Receiver
		self.e = int(self.socket.recv_string())

	def compute_f0f1(self):
		# Compute (f0, f1) pair from m0, m1 and (r0, r1) pads
		self.f0 = self.m0 ^ self.encode_msg(self.r0r1[self.e])
		self.f1 = self.m1 ^ self.encode_msg(self.r0r1[(1-self.e) % 2])

	def send_f0f1(self):
		# Send (f0, f1) pair to Receiver
		self.compute_f0f1()
		self.socket.send_string(str(self.f0) + "," + str(self.f1))

	def conductOT(self):
		# Perform all necessary tasks to conduct 1-2 OT. Performs
		# initialization procedures, and waits for necessary
		# (r0, r1) pad from Initializer before proceeding with 
		# communication to Receiver. 
		print("Waiting for initializer...")
		self.receive_initial_conditions()
		print("Initialization complete!")
		print()
		print("Connecting to receiver...")
		self.connect_to_receiver()
		self.receive_e()
		print("Computing and sending f pair from e...")
		self.send_f0f1()
		print()
		print("OT complete!")

main()
