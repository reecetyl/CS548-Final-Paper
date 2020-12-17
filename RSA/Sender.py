# Sender.py (RSA)
# Tyler Reece
# CS548 Final Project

# Simulates the role of Sender (Alice) in the 1-2 OT
# based on RSA, as specified by Even, Goldreich, and Lempel in 1985. 
#This script should be run AFTER Receiver.py.

# Specifically, this script establishes a REQ connection using ZeroMQ
# and follows the 1-2 OT protocol, including choosing message values,
# generating an RSA key pair, sending (x0, x1) pair to the Receiver,
# and computing and sending the (m'0, m'1) pair to the Receiver. 

import zmq
import os
import random
from Crypto.PublicKey import RSA

def main():

	s = Sender()
	s.conduct_OT()

class Sender:

	# Defaults
	SECURITY_PARAMETER = 2048
	ADDR = "tcp://localhost:5555"

	def __init__(self):
		# Receive m0 and m1 as keyboard input from the user
		# Establish ZeroMQ connection in REQ format
		print("m0 and m1 can be any ASCII values")
		m0 = input("Please enter m0: ")
		m1 = input("Please enter m1: ")
		self.m0 = self.encode_msg(m0)
		self.m1 = self.encode_msg(m1)
		self.gen_rsa_key_pair()
		self.context = zmq.Context()
		self.socket = self.context.socket(zmq.REQ)
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

	def gen_rsa_key_pair(self):
		# Generate RSA key pair and assign to object
		key = RSA.generate(self.SECURITY_PARAMETER)
		self.n, self.e, self.d = key.n, key.e, key.d

	def send_public_key(self):
		# Send only public key portion to Receiver
		self.socket.send_string(str(self.e) + "," + str(self.n))

	def get_confirmation(self):
		# Necessary because of REQ/REP format of ZeroMQ.
		# Sender must get a reply before it sends another
		# message to Receiver.
		reply = self.socket.recv_string()

	def send_x0x1(self):
		# Generate and compute (x0, x1) pair
		x0 = random.randint(0, self.n)
		x1 = random.randint(0, self.n)
		self.x0 = x0
		self.x1 = x1
		self.socket.send_string(str(self.x0) + "," + str(self.x1))

	def get_v(self):
		# Receive v value from Receiver and assign to object
		v = int(self.socket.recv_string())
		self.v = v

	def send_k0k1(self):
		# Compute (k0, k1) pair, and use to compute (m'0, m'1) pair
		# and send to Receiver.
		self.k0 = pow((self.v - self.x0), self.d, self.n)
		self.k1 = pow((self.v - self.x1), self.d, self.n)
		self.m0_prime = (self.m0 + self.k0) % self.n
		self.m1_prime = (self.m1 + self.k1) % self.n
		self.socket.send_string(str(self.m0_prime) + "," + str(self.m1_prime))

	def conduct_OT(self):
		# Perform all necessary tasks to conduct 1-2 OT from the perspective
		# of the Sender. 
		print("Sending public key to receiver...")
		self.send_public_key()
		self.get_confirmation()
		print("Generating random x0 and x1...")
		self.send_x0x1()
		print("Getting v from receiver...")
		self.get_v()
		print("Sending k0 and k1 to receiver...")
		self.send_k0k1()
		print()
		print("OT complete!")

main()