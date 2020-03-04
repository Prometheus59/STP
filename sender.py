from common import *


class sender:
    ACK = 0
    RTT = 20

    def isCorrupted(self, packet):
        #  Check if a received packet (ACK) has been corrupted during transmission.
        # similar to the corresponding function in receiver side

        calc_cs = checksumCalc(packet)
        if (packet.checksum != calc_cs):
            return True
        else:
            return False

    def isDuplicate(self, packet):
        # checks if an ACK is duplicate or not
        # similar to the corresponding function in receiver side
        if (packet.ackNum != self.ACK):
            return False
        else:
            return True

    def getNextSeqNum(self):
        # generate the next sequence number to be used
        # similar to the corresponding function in receiver side

        self.currentSeqNum += 1
        mod = self.currentSeqNum % 2

        return mod

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
        timeout_val = float(self.RTT*2.0)
        self.networkSimulator.startTimer(12345, timeout_val)
        
        return

    def output(self, message):
        self.currentPacket = Packet(self.currentSeqNum, self.ACK, 0, message.data)
        # Calculate checksum
        c = checksumCalc(self.currentPacket)
        # prepare a packet and send the packet through the network layer
        self.currentPacket.checksum = c
        # call utdSend
        self.networkSimulator.udtSend(self.entity, self.currentPacket)
        # start the timer
        self.networkSimulator.startTimer(self.entity, 5.0)
        # you must ignore the message if there is one packet in transit
        return

    def input(self, packet):

        # If ACK isn't corrupted or duplicate, transmission complete.
        if (not self.isCorrupted(packet) or not self.isDuplicate(packet)):
        # timer should be stopped, and sequence number should be updated
            self.networkSimulator.stopTimer(self.entity)
            self.seqNum = self.getNextSeqNum()
            return

        # In the case of duplicate ACK the packet, you do not need to do
        # anything and the packet will be sent again since the
        # timerInterrupt will be called by the simulator.
        return