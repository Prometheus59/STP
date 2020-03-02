from common import *


class receiver:
    ACK = 0
    SEQ = 0
    # expectedSeqNum

    def isCorrupted(self, packet):
        #  Check if a received packet has been corrupted during transmission.
        # Return true if computed checksum is different than packet checksum.
        calc_cs = checksumCalc(packet)
        if (packet.checksum != calc_cs):
            return True
        else:
            return False

    def isDuplicate(self, packet):
        # check if packet sequence number is the same as expected sequence number
        if (packet.seqNum != self.SEQ):
            return False
        else:
            return True

    def getNextExpectedSeqNum(self):
        # Use modulo-2 arithmetic to ensure sequence number is 0 or 1.
        self.SEQ += 1
        ans = SEQ % 2
        if (ans == 1 or ans == 0):
            return self.SEQ

        return self.SEQ

    def __init__(self, entityName, ns):
        self.entity = entityName
        self.networkSimulator = ns
        print("Initializing receiver: B: "+str(self.entity))

    def init(self):
        # initialise expected packet sequence number
        return

    def input(self, packet):

        # This method will be called whenever a packet sent from the sender
        # arrives at the receiver.
        # If packet is corrupted or duplicate: send ACK with the last ack number of
        # last correctly received packet. In other words, you can say send
        # a packet with wrong sequence number as there is only 0 and 1.
        # If packet is OK (not a duplicate or corrupted), deliver it and send
        # correct ACK.
        return
