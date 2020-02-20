from common import *

class sender:
    ACK = 0
    RTT = 20
    #currentSeqNum
    #currentPacket
    
    def isCorrupted (self, packet):
        #  Check if a received packet (ACK) has been corrupted during transmission.
        #similar to the corresponding function in receiver side
        return

    def isDuplicate(self, packet):
        # checks if an ACK is duplicate or not
        #similar to the corresponding function in receiver side
        return
 
    def getNextSeqNum(self):
        #generate the next sequence number to be used
        #similar to the corresponding function in receiver side
 
        return 

    def __init__(self, entityName, ns):
        self.entity = entityName
        self.networkSimulator = ns
        print("Initializing sender: A: "+str(self.entity))

    def init(self):
        #initialize the currentSeqNum  and currentPacket
        return

    def timerInterrupt(self):
        #This function implements what the sender does in case of timer interrupt
        #It sends the packet again. 
        #It starts the timer, sets the timeout value to be twice the RTT
        return


    def output(self, message):
        #prepare a packet and send the packet through the network layer
        #call utdSend
        #start the timer
        #you must ignore the message if there is one packet in transit
        return
 
    
    def input(self, packet):

        #If ACK isn't corrupted or duplicate, transmission complete.
        #timer should be stopped, and sequence number  should be updated
        #In the case of duplicate ACK the packet, you do not need to do 
        #anything and the packet will be sent again since the
        #timerInterrupt will be called by the simulator.
        return 
