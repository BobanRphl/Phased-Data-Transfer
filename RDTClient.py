# Boban Pallathucharry, J.M. Gallagher, and James Whitney
# 14-Feb-2020
# EECE 5830 - Network Design, Principles, and Applications
# Programming Project Phase 2: Implement RDT over UDP
# Client portion of code

# First we define two methods to implement the
# client portion of the RDT protocol

# Method make_pkt requires open file "bytes"
# and integer packetlength. It returns a series of bytes
# with length specified by packetlength.

def make_pkt(bytes, packetlength):
	return bytes.read(packetlength)

# Method send_pkt takes a series of bytes and sends them
# to the specified socket using the given clientSocket

def send_pkt(packet, clientSocket, serverName, serverPort):
	clientSocket.sendto(packet, (serverName, serverPort))


# This line imports the socket library needed to execute this program
from socket import *

# The next two lines identify the server socket we will use for our communications
# The local machine will be running the server and it will have port 4356, as
# designated in the code written for the server. It is critical that the server code
# use the same port as designated here or the client will not be able to communicate
# with the server.

serverName ='localhost'
serverPort = 4356

# Create a UDP socket to use to send messages to a server
clientSocket = socket(AF_INET, SOCK_DGRAM)

# Open file for the make_pkt function
# The file needs to be located in the same directory as this .py file
# The "rb" flags specify options "read" and "binary"
# We want to read binary data so we can deliver it directly to the
# make_pkt function
f = open("f22.bmp", "rb")

# Make the first packet to send to the server
# and a counter "i" so we can tell the user how many packets
# are sent.
packet = make_pkt(f, 1024)
i = 0

# The while loop runs the make_pkt method until
# it exhausts all of the bits in the specified transfer file.
# In Python, the end of the file is denoted as b'', so when this point
# is reached, the while loop ends.
while (packet != b''):
	send_pkt(packet, clientSocket, serverName, serverPort)
	packet = make_pkt(f, 1024)
	#print(packet)
	#print("I just sent packet # " + str(i))
	i=i+1	

# In order to prompt the server to stop receiving packets,
# close the file, and shutoff, the client sends the empty binary packet
# b''
send_pkt(packet, clientSocket, serverName, serverPort)

# We now tell the user the file has been transmitted to the server
# and how many packets were required for transmission.
print("Image transmission complete.")
print(str(i) + " packets were transmitted to the server.")

# Close file for the make_pkt function
# and close the client socket
f.close()
clientSocket.close()
print("Closing client program.")
