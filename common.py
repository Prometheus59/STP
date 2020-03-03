A = 12345
B = 67890
TRACE = 2
# This constant controls the maximum size of the buffer in a Message and in a Packet
MAXDATASIZE = 20


def checksumCalc(payload):
    # The implemention of function that calculates checksum goes here


    checksum = 0 #payload.ackNum + payload.seqNum
    for x in payload:
        checksum += ord(x)

    return checksum


class Packet:
    def __init__(self, s, a, c, p=''):
        self.seqNum = s
        self.ackNum = a
        self.checksum = c
        self.payload = p

    def toStr(self):
        return "seqNum: "+str(self.seqNum) + " ackNum: " + str(self.ackNum) + " checksum: " + str(self.checksum) + " payload: " + str(self.payload)


class Message:
    data = ''

    def __init__(self, inputData):
        self.data = inputData


class Event:
    def __init__(self, t, ty, ent, p=None):
        self.self = self
        self.time = t
        self.event_type = ty
        self.entity = ent
        self.packet = p


class EventType:
    TIMERINTERRUPT = 0
    FROMAPP = 1
    FROMNETWORK = 2


class EventList:
    def __init__(self):
        self.self = self
        self.event_list = []

    def add(self, e):
        return self.event_list.append(e)

    def removeNext(self):
        if len(self.event_list) == 0:
            return None
        # print(len(self.event_list))
        index = 0
        soonest = self.event_list[index].time

        for i in range(0, len(self.event_list)):
            if self.event_list[i].time < soonest:
                soonest = self.event_list[i].time
                index = i
        #print(" i ======" + str(i))
        next_event = self.event_list[index]
        self.event_list.pop(index)
        return next_event

    def removeTimer(self, entity):
        timerIndex = -1
        timerEvent = None

        for i in range(0, len(self.event_list)):
            if self.event_list[i].event_type == EventType.TIMERINTERRUPT and self.event_list[i].entity == entity:
                timerIndex = i
                break

        if timerIndex != -1:
            timerEvent = self.event_list[timerIndex]
            self.event_list.pop(timerIndex)

        return timerEvent

    def getLastPacketTime(self, entityTo):
        time = 0.0

        for i in range(0, len(self.event_list)):
            if self.event_list[i].event_type == EventType.FROMNETWORK:
                if self.event_list[i].entity == entityTo:
                    time = self.event_list[i].time

        return time
