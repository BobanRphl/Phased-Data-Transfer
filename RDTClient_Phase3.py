# Boban Pallathucharry, J.M. Gallagher, and James Whitney
# 18-Mar-2020
# EECE 5830 - Network Design, Principles, and Applications
# Programming Project Phase 3: Implement RDT 2.2 over UDP
# Client portion of code

# Import statement for content needed for the checksum function
from bitstring import *

import time #imports time function

import random #library needed for generating random numbers


# make_pkt expects all inputs to be in the form of bytes
# Example implementation make_pkt(b'1', b'4444', b'678432')
# Returns b'1444678432'
def make_pkt(ACK, checksum, data):
	ACK_b = bytearray(ACK)
	checksum_b = bytearray(checksum)
	data_b = bytearray(data)	
	return ACK_b + checksum_b + data_b

# recv_pkt receives packets from the designated Socket with size up to the given packetlength	
def recv_pkt(Socket, packetlength):
	message, Address = serverSocket.recvfrom(packetlength)
	return message, Address

# comp_checksum calculates the UDP checksum for a set of input bytes
def comp_checksum(data):
	#declaring variables used in the checksum function
	carry = bytes(2)                          # variable to store the actual carry bits from the 16-bit sum of a packet
	checksum = bytes(2)                      # variable to store the checksum
	value1 = bytes(2)                         # variable to store copies of the 16-bit sum during swapping
	sum2 = bytes(2)                           # variable to store copies of the 16-bit sum during swapping
	actual_sum = bytes(2)
	suminput = bytes(2)
	m = BitStream(bytearray(2))               # internediate variables to convert a string into a stream of Bits
	n=BitStream(bytearray(2))                 # internediate variables to convert a string into a stream of Bits	
	c = bytearray(data)
	k = BitStream(c)
	total_sum = sum(c)
	m.bin = bin(total_sum)[2:]
	n = BitStream(m)
	v = len(n)
	sum2 = total_sum
	while(v>8):                                # if length > 8 it means we have carry bits
		s = v-8                            # this value shows the number of carry bits
        	#print(s)
		# Acquires the sum bits        	
		actual_sum = sum2 & 0x00FF
		# print(bin(value3)[2:])
		# Acquires carry bits      		
		carry = (sum2 & 0xFF00) >> 8
        	#print(bin(carry)[2:])
		value3 = actual_sum + carry     # 1's compliment addition
        	#print(bin(value2)[2:])
		v = len(bin(value3)[2:])           # checks the length of new sum
        	#print(v)
		sum2 = value3             # swap values to make a copy for the next iteration, sum2 is a bytes type variable

        #print('\n' + bin(~value2) + '\n' + bin(value2))                          

	return sum2                                 # this final value will contain the checksum 

# is_corrupt returns True or False based on analysis of the ACK packet 
# acknowledgement and sequence number. It expects the packet to be input as bytes, e.g. b'2343x\00x\123' 
def is_corrupt(packet):
	#return False	
	data=bytearray(packet)
	#print("Packet data is: " + str(packet))
	ACK = data[0:1]
	seq = data[1:2]
	if ACK == seq:
		return False
	else:
		return True

	
# is_ACK requires data to be bytes and seq to be bytes as well
# Example implementation: is_ACK(b'12345', b'1') will return True
# The ACK corruption is also implemented in this function
# When the user sets corruption to a non-zero value, there is a chance that the is_ACK is corrupted and returns the wrong boolean.
# How often this happens is determined by how large a value the use inputs for corrupt_chance
def is_ACK(data, seq):
	rand = random.randint(1,100) #generates random number
	if rand<=corrupt_chance: #if random number is smaller than corrupt chance
		return True
	else: 
		if data[0:1] == bytes(seq):
			return True
		else:
			return False

# Method udt_send takes a series of bytes and sends them
# to the specified socket using the given clientSocket
def udt_send(packet, Socket, Address):
	  Socket.sendto(packet, Address)

# This line imports the socket library needed to execute this program
from socket import *
import time #imports time functions for timer

# The next two lines identify the server socket we will use for our communications
# The local machine will be running the server and it will have port 4356, as
# designated in the code written for the server. It is critical that the server code
# use the same port as designated here or the client will not be able to communicate
# with the server.

start_time = time.perf_counter() #starts the timer
serverName ='localhost'
serverPort = 4356
serverAddress = (serverName, serverPort)

# Create a UDP socket to use to send messages to a server
clientSocket = socket(AF_INET, SOCK_DGRAM)

# Open file for the make_pkt function
# The file needs to be located in the same directory as this .py file
# The "rb" flags specify options "read" and "binary"
# We want to read binary data so we can deliver it directly to the
# make_pkt function


print("Enter A Whole Number Between 0 and 100 for ACK Corruption Chance\n") #enters number to be used as percentage of corruption
corrupt_chance = int(input()) #takes the number and places it in a variable to test against other random numbers

f = open("image1.bmp", "rb")
file_bytes = f.read(1000)

# Make the first packet to send to the server
# and a counter "i" so we can tell the user how many packets
# are sent.

i = 0
start_time = time.perf_counter() #starts the timer
# The while loop runs the make_pkt method until
# it exhausts all of the bits in the specified transfer file.
# In Python, the end of the file is denoted as b'', so when this point
# is reached, the while loop ends.
while (file_bytes != b''):
	
	file_data = make_pkt(b'0', comp_checksum(file_bytes).to_bytes(2, 'big'), file_bytes)
	#print(file_bytes[0])
	#print(file_data)	
	#print(comp_checksum(file_bytes).to_bytes(2, 'big'))
	#print(is_corrupt(file_data))
	#print(file_bytes)
	udt_send(file_data, clientSocket, serverAddress)
	#print("I sent a seq_0 packet")
	# Wait for ACK 0
	while True:
		content = clientSocket.recvfrom(1024)
		rec_pkt = bytearray(content[0])
		#print(rec_pkt)
		#if (is_corrupt(rec_pkt)): print("ACK_0 is corrupt.") 
		if (is_corrupt(rec_pkt) or is_ACK(rec_pkt, b'1')):
			#if is_ACK(rec_pkt, b'1'): print("is wrong ack1")
			udt_send(file_data, clientSocket, serverAddress)
		else: 
			#print("I received ack for seq_0")
			break

	i = i+1
	file_bytes = f.read(1000)
	if (file_bytes== b''):
		break
	#print(file_bytes)
	file_data = make_pkt(b'1', comp_checksum(file_bytes).to_bytes(2, 'big'), file_bytes)
	udt_send(file_data, clientSocket, serverAddress)
	#print("I sent a seq_1 packet.")
	# Wait for ACK 1
	while True:
		content = clientSocket.recvfrom(1024)
		rec_pkt = bytearray(content[0])
		if (is_corrupt(rec_pkt) or is_ACK(rec_pkt, b'0')):
			#if is_ACK(rec_pkt, b'0'): print("is wrong ack2")
			udt_send(file_data, clientSocket, serverAddress)
		else: 
			#print("I just received ack for seq_1")			
			break	

	#print(packet)
	#print("I just sent packet # " + str(i))
	i=i+1	
	file_bytes = f.read(1000)
	if (file_bytes== b''):
		break

# In order to prompt the server to stop receiving packets,
# close the file, and shutoff, the client sends the empty binary packet
# b''
#print("sending a blank")
udt_send(b'', clientSocket, serverAddress)

# We now tell the user the file has been transmitted to the server
# and how many packets were required for transmission.
stop_time = time.perf_counter() #stops timer
total_time = stop_time-start_time #subtracts start time from stop time to get total time timer runs
print("Image transmission complete.")
print(str(i) + " packets were transmitted to the server.")
print("Transmission time: " + str(total_time) + " seconds") #prints the total time taken to upload image in seconds

# Close file for the make_pkt function
# and close the client socket
f.close()
clientSocket.close()
print("Closing client program.")
