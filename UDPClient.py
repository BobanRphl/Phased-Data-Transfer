'''

Phase One code for UDP Client
Name: Boban R. Pallathucharry
Student ID: 01810169

'''


from socket import *
serverName = '127.0.0.1'                                        # specifiy IP address to run server on local machine
serverPort = 12000                                              # assigned 12000 as port number to the server 
clientSocket = socket(AF_INET, SOCK_DGRAM)                      # opened a socket for the client based on UDP protocol 
message = input('Input lowercase sentence:')                    # asks for user input
clientSocket.sendto(message.encode(), (serverName, serverPort)) # encodes message into bytes and puts it on the socket
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)    # reads the message from server
print(modifiedMessage.decode())                                 # prints the message from server on the terminal
clientSocket.close()                                            # closes the client socket
