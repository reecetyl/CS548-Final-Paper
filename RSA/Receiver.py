# Receiver.py (RSA)
# Tyler Reece
# CS548 Final

# Simulates the role of Receiver (Bob) in the 1-2 OT
# based on RSA, as specified by Even, Goldreich, and Lempel in 1985. 
#This script should be run BEFORE Sender.py.

# Specifically, this script establishes a REP connection using ZeroMQ
# and follows the 1-2 OT protocol, including choosing a b value,
# receiving the public key from the Sender, receiving (x0, x1), computing
# and sending v, and receiving and decrypting the m'0 and m'1 values.

import time
import zmq
import random
import sys

def main():

	r = Receiver()
	r.conduct_OT()

class Receiver:

	# Defaults
	ADDR = "tcp://*:5555"

	def __init__(self):
		# Receive b as keyboard input from user and establish 
		# ZeroMQ connection in REP format
		b = input("Please enter 0 or 1 as selection bit: ")
		assert(b == "0" or b == "1")
		self.b = int(b)
		self.context = zmq.Context()
		self.socket = self.context.socket(zmq.REP)
		self.socket.bind(self.ADDR)
		print("Selection bit is", str(self.b))
		print()
		print("Waiting for sender to initialize...")

	def get_sender_public_key(self):
		# get the Sender's public key (e, n)
		public_key = self.socket.recv_string()
		e, n = public_key.split(",")
		self.e, self.n = int(e), int(n)
		self.socket.send_string("Got public key info!")

	def get_x0x1(self):
		# get the (x0, x1) pair from the Sender
		x0x1 = self.socket.recv_string()
		x0x1 = x0x1.split(",")
		x0x1 = [int(x) for x in x0x1]
		self.v = self.compute_v(x0x1)

	def compute_v(self, x0x1):
		# Compute v = xb + k^e
		self.k = random.randint(0, self.n)
		xb = x0x1[self.b]
		v = xb + pow(self.k, self.e, self.n)
		return v

	def send_v(self):
		# Send v to the Sender
		self.socket.send_string(str(self.v))

	def get_m0m1_prime(self):
		# Receive the (m'0, m'1) pair from the Sender,
		# and compute mb using k value.
		m0m1_prime = self.socket.recv_string()
		m0m1_prime = m0m1_prime.split(",")
		m0m1_prime = [int(x) for x in m0m1_prime]
		self.mb = self.compute_mb(m0m1_prime)

	def compute_mb(self, m0m1_prime):
		# Undo encryption using k value to recover desired message
		mb_prime = m0m1_prime[self.b]
		mb = mb_prime - self.k
		return self.decode_msg(mb)

	def decode_msg(self, m):
		# decodes messages from concatenated ASCII values to plain text
		msg = ""
		m_total = str(m)
		while len(m_total) % 3 != 0:
			m_total = "0" + m_total
		ascii_list = [m_total[i: i+3] for i in range(0, len(m_total), 3)]
		chr_list = [chr(int(i)) for i in ascii_list]
		for c in chr_list:
			msg += c
		return msg

	def conduct_OT(self):
		# Perform all necessary tasks to conduct 1-2 OT, including initialization
		# proceedures, and internal computations. Prints the value
		# of the desired message mb and quits.
		self.get_sender_public_key()
		print("Getting public key from sender...")
		print("Getting x0 and x1 from sender...")
		self.get_x0x1()
		print("Computing and sending v...")
		self.send_v()
		print("Computing mb from m'0 and m'1...")
		self.get_m0m1_prime()
		print()
		print("m" + str(self.b) + " is:", self.mb)
		print()
		print("OT complete!")

main()