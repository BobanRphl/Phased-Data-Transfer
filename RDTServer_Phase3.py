# Boban Pallathucharry, J.M. Gallagher, and James Whitney
# 18-Mar-2020
# EECE 5830 - Network Design, Principles, and Applications
# Programming Project Phase 3: Implement RDT 2.2 over UDP
# Server portion of code

# This line imports the socket library needed to execute this program
# We chose serverPort 4356 so the code doesn't interfere with any system processes
from socket import *
serverPort = 4356

# Import statement for content needed for the checksum function
from bitstring import *

import random #library needed for generating random numbers

# Create a UDP socket to receive messages from a client
serverSocket=socket(AF_INET,SOCK_DGRAM)

# This next line sets the server socket for our program as the current users'
# machine with the port specified in the earlier line of code
serverSocket.bind(('localhost', serverPort)) #sets up connection

# We now define a method recv_pkt to implement the RDT protocol
# This method requires a server socket and specified packet length
# It only returns the received message to the user in binary.
# It does not return the clientAddress as this code is not meant to send
# content back to the client.
def recv_pkt(serverSocket, packetlength):
	message, clientAddress = serverSocket.recvfrom(packetlength)
	return message, clientAddress

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

# is_corrupt returns True or False based on analysis of the checksum
# of the input packet. It expects the packet to be input as bytes, e.g. b'2343x\00x\123' 
def is_corrupt(packet):
	data=bytearray(packet)
	#print("Packet data is: " + str(packet))
	checksum = int.from_bytes(data[1:3], 'big')
	#print("Checksum is: " + str(checksum))
	serverSum = ~comp_checksum(data[3:len(data)])
	#serverSum = 0xdf
	#print("Server sum is: " + str(BitStream(serverSum)))
	#print(checksum + serverSum)	
	if checksum + serverSum == -1:
		return False
	else:
		return True

# has_seq0 determines if the packet has sequence number 0
def has_seq0(data):
	if data[0:1] == b'0':
		return True
	else:
		return False

# Requires input of packet with 5 byte header 
# The first byte is the ACK byte
# bytes 2-5 are the checksum, the remaining data is
# the packet content
def extract_bits(data):
	#print(data[3])
	return data[3:len(data)]

# make_pkt takes 3 sets of bytes and concatenates them to be sent on a Socket
def make_pkt(ACK, checksum, data):
	ACK_b = bytearray(ACK)
	checksum_b = bytearray(checksum)
	data_b = bytearray(data)	
	return ACK_b + checksum_b + data_b

# udt_send sends packets from the designated server socket to the given client address
def udt_send(packet, serverSocket, clientAddress):
	  serverSocket.sendto(packet, clientAddress)

# The corrupting function simulates bit corruption in the packets received from a client.
# The amount of corruption is determined by the corrupt_chance parameter, which equates to a percent chance of a bit
# being flipped in the packet.
# The function flips one bit based on whether a random number is less than the given corrupt_chance
def corrupting(data, corrupt_chance): #function for corrupting packet
	rand = random.randint(1,100) #random integer between 0-99 is generated
	if rand<=corrupt_chance: #checks if random number is less than percentage chance
		original_value = data[3]
		data[3] ^= 0x1F #if it is less, it corrupts the bit
		if original_value == data[3]: data[3] = 0xFF # this line of code ensures some sort of corruption is introduced into the code
		return data #returns data
	
# Now we make a file in which the code will write binary
# information received in the form of packets from the socket.

print("Enter A Whole Number Between 0 and 100 For Data Corruption Chance\n") #enters number to be used as percentage of corruption
corrupt_chance = int(input()) #takes the number and places it in a variable to test against other random numbers

f=open('serverimage.bmp','wb')
print("The server is ready to receive") 

# i = 0

# The while loop runs idle until the server begins to receive information from
# a client communicating with the server socket. The loop receives a packet,
# writes this packet to the open file and repeats until the packet contents
# is b''. When this final empty packet is received, the loop terminates.

onceThru = 0
send_pkt_cpy=b'0'
while True:
	#serverSocket.settimeout(5) #times out once data stops being sent 

	#Analyze content with server logic
	
	#Wait for 0 from below
	# ACK = b'0'
	# seq = b'1'
	# send_pkt = make_pkt(ACK, seq, checksum)
	
	while True:
		content = recv_pkt(serverSocket, 1024) #receives next batch of data
		data = bytearray(content[0]) #gets data from packet
		if data == b'': #if empty, break out of inner while loop
			break
		checksum = data[1:3] #gets checksum
		clientAddress = content[1] #gets client address
		corrupting(data, corrupt_chance) #chance to corrupt packet

		if (is_corrupt(data) or not(has_seq0(data))):
			#if is_corrupt(data): print("This packet is corrupt.")	
			#if not has_seq0(data): print("wrong bit1")
			ACK = b'1' #sets ack to opposite of what it should be
			seq = b'00' #sets seq number
			send_pkt = make_pkt(ACK, seq, b'')	#makes packet to send
			udt_send(send_pkt, serverSocket, clientAddress) #sends packet to tell client to resend data
			break
				
		if (not(is_corrupt(data)) and has_seq0(data)):
			ACK = b'0' #sets ack to proper value
			seq = b'00' #sets sequence number
			send_pkt = make_pkt(ACK, seq, b'') #makes packet out of ack and sequence number
			if send_pkt == send_pkt_cpy: #if packet is equal to last packet saved, ack corruption, do not write data 
				udt_send(send_pkt, serverSocket, clientAddress) #tells client to send new data
				break
			else: #if packet is different than last packet saved
				f.write(extract_bits(data)) #write to file
				send_pkt_cpy = send_pkt #saves a copy of the ack and sequence number
				udt_send(send_pkt, serverSocket, clientAddress) #asks client to send new data
				#print("I wrote seq_0 packet to the file.")
			# extract, write, send ack
				break
	if data == b'': break #if data is blank, break out of outer while loop

	while True:
		
		content = recv_pkt(serverSocket, 1024) #receives next batch of data
		data = bytearray(content[0])
		if data == b'':
			break
		checksum = data[1:3]
		clientAddress = content[1]
		corrupting(data, corrupt_chance) #chance to corrupt packet

		if (is_corrupt(data) or has_seq0(data)):
			#if is_corrupt(data): print("This packet is corrupt.")		
			#if has_seq0(data): print("wrong bit2")
			ACK = b'0'
			seq = b'10'
			send_pkt = make_pkt(ACK, seq, b'')		
			udt_send(send_pkt, serverSocket, clientAddress)
			break
				
		if (not(is_corrupt(data)) and not(has_seq0(data))):
			ACK = b'1'
			seq = b'10'
			send_pkt = make_pkt(ACK, seq, b'')
			if send_pkt == send_pkt_cpy:
				udt_send(send_pkt, serverSocket, clientAddress)
				break
			else:
				f.write(extract_bits(data))
				send_pkt_cpy = send_pkt
				udt_send(send_pkt, serverSocket, clientAddress)
				#print("I wrote seq_1 packet to the file.")
			# extract, write, send ack
				break
	if data == b'': break 
	
		# extract, write, send ack
	
	#print(message)


	#print("Score! I received packet # " + str(i))
	#i = i+1
	#if i > 50000:
	#	break

# serverSocket.sendto("Image received".encode(), clientAddress)

# Tell the user the image is received and close the file so the user may go and open it.
print("Image received")
f.close()
