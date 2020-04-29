# Phased-Data-Transfer

This is a phased project developed by me and my classmates as part of our course project for Network Design. It contains 5 Phases which are fully functional. Phase 6 is in progress.


Phase 1: Transfer a simple text message from a 'client' machine to a 'server' machine using UDP socket in Python.
         The cleint and server are just two different VM's on the same computer.

Phase 2: Introduces the concept of packets. We trnasfer a JPEG image through a UDP socket by parsing the image as packets of 1  
         byte.

Phase 3: Builds on Phase 2 and considers the possibility of errors in the data as well as the acknowledgement of packets sent by 
         the client. The client calculates a check-sum for every packet that it transmits. This phase takes into perspective the 
         size of the UDP datagram which includes the checksum, data and
         sequence number.
         
Phase 4: Introduces a timeout to simulate a delay in the reception of packets and thereby a delay in sending an ACK. This is to 
         allow the client-server exchange to recover a lost packet.
   
Phase 5: Implements Go-Back-N to simulate a pipelined data transfer protocl which tries to achieve data transfer times close to 
         those in the real world. Introduces the concept of a moving windows to send groups of packet at a time and receive 
         acumulative ACK showing the number of received packets.
        
Phase 6: This phase implements the functionality of the TCP protocol on top of Phase 5. It's in progress.
