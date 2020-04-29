# Boban Pallathucharry, J.M. Gallagher, and James Whitney
# 14-Feb-2020
# EECE 5830 - Network Design, Principles, and Applications
# Programming Project Phase 2: Implement RDT over UDP
# Server portion of code

# This line imports the socket library needed to execute this program
# We chose serverPort 4356 so the code doesn't interfere with any system processes
from socket import*
serverPort = 4356

# Create a UDP socket to use to receive messages from a client
serverSocket=socket(AF_INET,SOCK_DGRAM)

# This next line sets the server socket for our program as the current users'
# machine with the port specified in the earlier line of code
serverSocket.bind(('localhost',serverPort)) #sets up connection

# We now define a method recv_pkt to implement the RDT protocol
# This method requires a server socket and specified packet length
# It only returns the received message to the user in binary.
# It does not return the clientAddress as this code is not meant to send
# content back to the client.
def recv_pkt(serverSocket, packetlength):
	message, clientAddress = serverSocket.recvfrom(packetlength)
	return message

# Now we make a file in which the code will write binary
# information received in the form of packets from the socket.
f=open('serverimage.bmp','wb')

print("The server is ready to receive") 

# Create a counter to track the number of packets received from the client
i = 0

# The while loop runs idle until the server begins to receive information from
# a client communicating with the server socket. The loop receives a packet,
# writes this packet to the open file and repeats until the packet contents
# is b''. When this final empty packet is received, the loop terminates.
while True:
	#message, clientAddress = serverSocket.recvfrom(1024) #receives first batch of data
	#f.write(message) #writes to file
	#serverSocket.settimeout(5) #times out once data stops being sent 
	message = recv_pkt(serverSocket, 1024) #receives next batch of data
	f.write(message)
	#print(message)
	if message == b'':
		break	
	#print("Score! I received packet # " + str(i))
	#i = i+1
	#if i > 50000:
	#	break

# serverSocket.sendto("Image received".encode(), clientAddress)

# Tell the user the image is received and close the file so the user may go and open it.
print("Image received")
f.close()
serverSocket.close()
