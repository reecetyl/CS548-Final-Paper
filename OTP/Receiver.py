# Receiver.py (OTP)
# Tyler Reece
# CS548 Final Project

# Simulates the role of Receiver (Bob) in the 1-2 OT
# based on the OTP, as specified by Ron Rivest in 1999. This
# script should be run BEFORE Initializer.py (and along with
# Sender.py).

# Specifically, this script establishes a Subscribe connection at
# the address ADDR using ZeroMQ, and receives d and rd from the
# Initializer. The rest of the 1-2 OT protocol is followed,
# including computing and sending e = b ^ d, and receiving
# (f0, f1) from the sender, and finally computing the desired
# message mb. 

import sys
import zmq
import time


def main():
	r = Receiver()
	r.conductOT()

class Receiver:

	# Defaults
	ADDR = "tcp://127.0.0.1:5556"
	ADDR2 = "tcp://127.0.0.1:3434"
	MAX_MSG_LEN = 50

	def __init__(self):
		# Receive b as keyboard input from user and establish 
		# ZeroMQ connection in SUB format
		b = input("Please enter 0 or 1 as selection bit: ")
		assert(b == "0" or b == "1")
		self.b = int(b)
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

	def receive_initial_conditions(self):
		# Subscribes to "Receiver" topicfilter, and receives d and rd
		# from trusted initializer
		topicfilter = "Receiver"
		self.socket.setsockopt_string(zmq.SUBSCRIBE, topicfilter)
		string = self.socket.recv_string()
		topic, messagedata = string.split()
		self.d, self.rd = messagedata.split(",")
		self.socket.close()

	def connect_to_sender(self):
		# Establish new line of communication with Sender using REQ/REP
		time.sleep(1) # give small delay for Sender to connect
		self.socket = self.context.socket(zmq.REQ)
		self.socket.connect(self.ADDR2)

	def compute_e(self):
		# Computes e = b ^ d
		self.e = int(bool(self.b) != bool(int(self.d)))

	def send_e(self):
		# Sends e value to Sender
		self.compute_e()
		self.socket.send_string(str(self.e))

	def receive_f0f1(self):
		# Gets (f0, f1) pair from Sender
		f0_str, f1_str = self.socket.recv_string().split(",")
		self.f0, self.f1 = int(f0_str), int(f1_str)		
		self.f0f1 = (self.f0, self.f1)

	def compute_mb(self):
		# Computes and decodes desired message mb
		self.mb = self.decode_msg(self.f0f1[self.b] ^ self.encode_msg(self.rd))


	def conductOT(self):
		# Perform all necessary tasks to conduct 1-2 OT from the Receiver end.
		# Performs initialization proceedures, then waits on Initializer for
		# necessary input before proceeding with communication with Sender.
		print("Waiting for initializer...")
		self.receive_initial_conditions()
		print("Initialization complete!")
		print()
		print("Connecting to sender...")
		self.connect_to_sender()
		print("Computing and sending e...")
		self.send_e()
		self.receive_f0f1()
		print("Computing mb from f" + str(self.b) + "...")
		self.compute_mb()
		print()
		print("m" + str(self.b) + " is:", self.mb)
		print()
		print("OT complete!")

main()