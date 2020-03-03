from common import *


class sender:
    ACK = 0
    RTT = 20

    def isCorrupted(self, packet):
        #  Check if a received packet (ACK) has been corrupted during transmission.
        # similar to the corresponding function in receiver side
        # TODO: Check if ACK (and/or) SEQ must be included in checksum calculation

        calc_cs = checksumCalc(packet.payload)
        if (packet.checksum != calc_cs):
            return True
        else:
            return False

        return

    def isDuplicate(self, packet):
        # checks if an ACK is duplicate or not
        # similar to the corresponding function in receiver side
        if (packet.ACK != self.ACK):
            return False
        else:
            return True

    def getNextSeqNum(self):
        # generate the next sequence number to be used
        # similar to the corresponding function in receiver side

        self.ACK += 1
        mod = self.ACK % 2

        

        return

    def __init__(self, entityName, ns):
        self.entity = entityName
        self.networkSimulator = ns
        print("Initializing sender: A: "+str(self.entity))

    def init(self):
        # initialize the currentSeqNum and currentPacket
        self.currentSeqNum = 0
        self.currentPacket = Packet(currentSeqNum, ACK, 0, '')
        return

    def timerInterrupt(self):
        # This function implements what the sender does in case of timer interrupt
        # It sends the packet again.
        # It starts the timer, sets the timeout value to be twice the RTT

        # output(msg)
        self.networkSimulator.udtSend(self.entity, currentPacket)
        timeout_val = self.RTT*2.0
        self.networkSimulator.startTimer(12345, timeout_val)
        
        return

    def output(self, message):
        # print("THis is " + message.data)
        c = checksumCalc(message.data)

        # TODO: Change 'npacket' to 'self.currentPacket'
        npacket = Packet(self.currentSeqNum, self.ACK, c, message.data)
        # prepare a packet and send the packet through the network layer

        # call utdSend
        self.networkSimulator.udtSend(self.entity, npacket)
        # start the timer
        self.networkSimulator.startTimer(self.entity, self.RTT)
        # you must ignore the message if there is one packet in transit
        return

    def input(self, packet):

        # If ACK isn't corrupted or duplicate, transmission complete.
        # timer should be stopped, and sequence number  should be updated
        # In the case of duplicate ACK the packet, you do not need to do
        # anything and the packet will be sent again since the
        # timerInterrupt will be called by the simulator.
        return
