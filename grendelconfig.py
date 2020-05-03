# this is a set up and config file for the other programs.
# also all code that is used by multiple programs goes here.
# christopher rehm  15 jan 2020
#

import os
import time
import json

DEBUG = True

msgPath = "/media/grendelData102/GrendelData/grendelMsgs/"
msgPathAI = "/media/grendelData102/GrendelData/grendelMsgs/AI"
msgPathPY = "/media/grendelData102/GrendelData/grendelMsgs/PY"
msgPathOT = "/media/grendelData102/GrendelData/grendelMsgs/OT"

fotoPath = "/media/grendelData102/GrendelData/grendelFotos/"
audioPath = "/media/grendelData102/GrendelData/grendellAudio/"

grendelOtherData = "/media/grendelData102/GrendelData/grendelOtherData/"
grendelWorldData = "/media/grendelData102/GrendelData/grendelWorldData/"
processFotoPath = "/media/grendelData102/lowLevelPrograms/processFoto.py"
grendelLogData = "/media/grendelData102/grendelLogs/"


###############################################################
def makeMsg(sender, title, text, priority, reciever, otherRecievers, files):
    debugBreakPoint("Entering makeMsg", "grendelconfig")
    mymessage = message()
    mytime = str(time.time())
    mymessage.write(mytime, sender, title, text, priority,
                    reciever, otherRecievers, files)


################################################################
def debugBreakPoint(message, location, stopBreak=False):
    if DEBUG is True: print(str(time.time()) + " :" + str(message) + " :" + str(location))
    if stopBreak is True:
        prompt = "Any key to continue, s stops program, at location " + str(location)
        myanswer = input(prompt)
        if myanswer == "s":
            shutdownGrendel()
    logdata = (str(time.time()) + " :" + str(message) + " :" + str(location) + " :" + str(stopBreak) + "\n")
    with open(grendelLogData + "masterlog.log", 'a+') as f:
        f.write(logdata)
    f.close


###############################################################
def shutdownGrendel():
    debugBreakPoint("In shutdownGrendel", "grendelconfig.py")
    makeMsg("zero", "shutdown", "shutdown", "1", "ALL", "ALL", "NONE")


###############################################################
class message():
    indexNumber = 0

    def __init__(self):
        debugBreakPoint("In message init", "grendelconfig.py")
        self.indexNumber = message.indexNumber
        self.timeStamp = ""
        self.sender = ""
        self.title = ""
        self.text = ""
        self.primeRecipient = ""
        self.priority = ""
        self.otherRecipients = ""
        self.files = ""
        message.indexNumber = message.indexNumber + 1

#######################################
    def saveMessageNumber(self):
        debugBreakPoint("In saveMessageNumber", "grendelconfig.py")
        mydata = [message.indexNumber]
        jsonData = json.dumps(mydata, sort_keys = True,  indent = 4, separators = (",", ": "))
        with open("currentMessageNumber", 'w') as f:
            f.write(jsonData)


##########################################
    def loadMessageNumber(self):
        pass

###############################################

    def write(self, timeStamp, title, text, sender, priority, primeRecipient, otherRecipients, files):
        debugBreakPoint("In messageWrite", "grendelconfig.py")
        debugBreakPoint(timeStamp, "grendelconfig.py")
        myCurrentDir = os.getcwd()
        mydata = [timeStamp,
                  sender,
                  title,
                  text,
                  priority,
                  primeRecipient,
                  otherRecipients,
                  files,
                  self.indexNumber]
        debugBreakPoint(mydata, "grendelconfig.py")
        jsonData = json.dumps(mydata,
                              sort_keys=True,
                              indent=4,
                              separators=(",", ": "))
        debugBreakPoint(jsonData, "grendelconfig.py")
        debugBreakPoint(primeRecipient, "grendelconfig.py")
        filename = str(timeStamp) + sender + ".json"
        if primeRecipient == "AI":
            os.chdir(msgPathAI)
        elif primeRecipient == "PY":
            os.chdir(msgPathPY)
        elif primeRecipient == "OT":
            os.chdir(msgPathOT)
        elif primeRecipient == "ALL":
            for each in [msgPathAI, msgPathPY, msgPathOT]:
                os.chdir(each)
                with open(filename, 'w') as f:
                    f.write(jsonData)
            os.chdir(myCurrentDir)
            return "0"
        with open(filename, 'w') as f:
            f.write(jsonData)
        os.chdir(myCurrentDir)
        return "0"

    ##########################################################
    def read(self, msgStamp, program):
        debugBreakPoint("Message.read we are here", "grendelconfig.py")
        myCurrentDir = os.getcwd()
        filename = msgStamp
        if program == "AI":
            os.chdir(msgPathAI)
        elif program == "PY":
            os.chdir(msgPathPY)
        elif program == "OT":
            os.chdir(msgPathOT)
        with open(filename, "r") as content:
            if DEBUG is True: print("now trying to read json data")
            datastuff = json.load(content)
            if DEBUG is True: print(datastuff)
            self.timeStamp = datastuff[0]
            if DEBUG is True: print(self.timeStamp)
            self.title = datastuff[1]
            if DEBUG is True: print(self.title)
            self.text = datastuff[2]
            if DEBUG is True: print(self.text)
            self.sender = datastuff[3]
            if DEBUG is True: print(self.sender)
            self.priority = datastuff[4]
            if DEBUG is True: print(self.priority)
            self.primeRecipient = datastuff[5]
            if DEBUG is True: print(self.primeRecipient)
            self.otherRecipients =datastuff[6]
            if DEBUG is True: print(self.otherRecipients)
            self.files = datastuff[7]
#            if DEBUG is True: print(self.files)
            self.indexNumber = datastuff[8]
            if DEBUG is True: print(self.indexNumber)

            return datastuff
        os.chdir(myCurrentDir)
