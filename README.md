# Reece CS548 Final Project
Implementation of Rivest 1999 and EGL 1985 1-2 Oblivious Transfer for CS548 Final Project


## Description of Software
This repository contains Python based implementations of two protocols for oblivious transfer. The first protocol, based on the OTP, was first described by Rivest in 1999, and the other protocol, based on RSA, was described by Even, Goldreich, and Lempel in 1985. Please refer to the attached paper (PDF provided in this repository) for further details on the protocol specifications. 

OTP Specification (Rivest 1999):

![alt text](https://github.com/reecetyl/CS548-Final-Paper/blob/master/Demo/otp.PNG)

RSA Specification (Even, Goldreich, Lempel 1985):

![alt text](https://github.com/reecetyl/CS548-Final-Paper/blob/master/Demo/rsa.PNG)

## Instructions for Use
The scripts are intended to be run in Receiver-Sender or Receiver-Sender-Initializer order for the OTP and RSA based implementations, respectively. Please see the GIF below for a demonstration of the OTP implementation:

![alt text](https://github.com/reecetyl/CS548-Final-Paper/blob/master/Demo/otp.gif)

As demonstrated, the scripts are run in the order Receiver-Sender-Initializer. The Receiver specifies a selection bit (0 or 1), and the Sender inputs two ASCII text messages, m0 and m1. The Initializer generates the necessary randomized information and sends the information to the Sender and Receiver to allow the protocol to proceed. 

Please see the GIF below for a demonstration of the EGL implementation:

![alt text](https://github.com/reecetyl/CS548-Final-Paper/blob/master/Demo/rsa.gif)

As demonstrated, the scripts are run in the order Receiver-Sender. The Receiver specifies a selection bit (0 or 1) and the Sender inputs two ASCII text messages, one of which will be sent to the Receiver through oblivious transfer. 
