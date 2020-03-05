from common import *


class receiver:
    ACK = 0
    SEQ = 0

    def isCorrupted(self, packet):
        # Check if a received packet has been corrupted during transmission.
        # Return true if computed checksum is different than packet checksum.
        calc_cs = checksumCalc(packet)
        if (packet.checksum != calc_cs):
            print("Reciever checksum is corrupted")
            return True
        else:
            print("Reciever checksum is NOT corrupted")
            return False

    def isDuplicate(self, packet):
        # check if packet sequence number is the same as expected sequence number
        if (packet.seqNum != self.SEQ):
            print("Reciever packet is not duplicate: Packet.seqNum->" + str(packet.seqNum) + " self.seqNum-> " + str(self.expectedSeqNum))
            return False
        else:
            print("Reciever packet is duplicated: Packet->" + str(packet.seqNum) + " self-> " + str(self.expectedSeqNum))
            return True

    def getNextExpectedSeqNum(self):
        # Use modulo-2 arithmetic to ensure sequence number is 0 or 1.
        self.expectedSeqNum += 1
        self.expectedSeqNum %= 2

        return self.expectedSeqNum

    def __init__(self, entityName, ns):
        self.entity = entityName
        self.networkSimulator = ns
        print("Initializing receiver: B: " + str(self.entity))

    def init(self):
        # initialise expected packet sequence number
        self.expectedSeqNum = 0
        return

    def input(self, packet):

        # This method will be called whenever a packet sent from the sender
        # arrives at the receiver.
        
        # If packet is corrupted or duplicate: send ACK with the last ACK number of
        # last correctly received packet. In other words, you can say send
        # a packet with wrong sequence number as there is only 0 and 1.

        # Set SEQ = expected sequence number
        self.SEQ = self.getNextExpectedSeqNum()

        if (self.isCorrupted(packet) or self.isDuplicate(packet)):
            # packet.seqNum = self.getNextExpectedSeqNum()
            print("Packet sent to B is corrupted/duplicated")
            packet.payload = ''
            packet.seqNum = (packet.seqNum + 1) % 2
            packet.checksum = packet.ackNum
            packet.ackNum = self.ACK
            self.networkSimulator.udtSend(self.entity, packet)
    
        # If packet is OK (not a duplicate or corrupted), deliver it and send
        # correct ACK.
        else:
            self.networkSimulator.deliverData(self.entity, packet.payload)

            npacket = Packet(0, self.ACK, 0, '')
            c = checksumCalc(npacket)
            npacket.checksum = c
            self.networkSimulator.udtSend(self.entity, npacket)
            self.ACK = (self.ACK + 1)%2

        return