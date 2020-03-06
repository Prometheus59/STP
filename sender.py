'''
------------------------------------------------------
Names: Ryan Karumanchery & Ramandeep Saini
Date: March 6th, 2020
Description: Implementing Reliable transport protocal
Course: CP372
Proffesor: Dr. Rudafshani
------------------------------------------------------
'''

from common import *

class sender:
    ACK = 0
    RTT = 20

    def isCorrupted(self, packet):
        #  Check if a received packet (ACK) has been corrupted during transmission.
        # similar to the corresponding function in receiver side
        # print("Packet acknum is: " + str(packet.ackNum))
        calc_cs = checksumCalc(packet)

        if (packet.checksum != calc_cs):
            print("Sender checksum is corrupted")
            print("packet.checksum = " + str(packet.checksum) + ", calc_cs = " + str(calc_cs))
            return True
        else:
            if (packet.ackNum != self.currentSeqNum):
                return True
            print("Sender checksum is NOT corrupted")
            print("packet.checksum = " + str(packet.checksum) + ", calc_cs = " + str(calc_cs))
            return False

    def isDuplicate(self, packet):
        # checks if an ACK is duplicate or not
        # similar to the corresponding function in receiver side
        if (packet.ackNum != self.ACK):
            print("Sender packet is not duplicate")
            print("Sender: Packet.acknum = " + str(packet.ackNum) + ", self.ACK = " + str(self.ACK))
            return False
        else:
            print("Sender packet is duplicated")
            print("Sender: Packet.acknum = " + str(packet.ackNum) + ", self.ACK = " + str(self.ACK))
            return True

    def getNextSeqNum(self):
        # generate the next sequence number to be used
        # similar to the corresponding function in receiver side

        self.currentSeqNum += 1
        self.currentSeqNum %= 2

        return self.currentSeqNum

    def __init__(self, entityName, ns):
        self.entity = entityName
        self.networkSimulator = ns
        print("Initializing sender: A: "+str(self.entity))

    def init(self):
        # initialize the currentSeqNum and currentPacket
        self.currentSeqNum = 0
        self.currentPacket = Packet(self.currentSeqNum, self.ACK, 0, '')
        return

    def timerInterrupt(self):
        # This function implements what the sender does in case of timer interrupt
        # It sends the packet again.
        # It starts the timer, sets the timeout value to be twice the RTT

        # output(msg)
        self.networkSimulator.udtSend(self.entity, self.currentPacket)
        self.networkSimulator.startTimer(self.entity, float(self.RTT*2.0))

        return

    def output(self, message):
        self.currentPacket.payload = message.data
        self.currentPacket.ackNum = 0
        self.currentPacket.seqNum = self.currentSeqNum
        # Calculate checksum
        c = checksumCalc(self.currentPacket)
        # prepare a packet and send the packet through the network layer
        self.currentPacket.checksum = c
        # call utdSend
        self.networkSimulator.udtSend(self.entity, self.currentPacket)
        # start the timer (asssuming 10 seconds is a time unit)
        self.networkSimulator.startTimer(self.entity, 20.0)

        return

    
    def input(self, packet):

        # If ACK isn't corrupted or duplicate, transmission complete.
        if ((not self.isCorrupted(packet)) or (not self.isDuplicate(packet))):
            # timer should be stopped, and sequence number should be updated
            self.networkSimulator.stopTimer(self.entity)
            self.currentSeqNum = self.getNextSeqNum()
            return
        else:
            print("A - Recieved a corrupted packet, packet will resend")

        # In the case of duplicate ACK the packet, you do not need to do
        # anything and the packet will be sent again since the
        # timerInterrupt will be called by the simulator.
        self.ACK = (self.ACK+1)%2
        return