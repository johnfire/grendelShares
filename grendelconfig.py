# this is a set up and config file for the other programs.
# also all code that is used by multiple programs goes here.
# christopher rehm  15 jan 2020
#

import os
import json
import sys
import time

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
    print("entering makeMsg")
    mymessage = message()
    mytime = str(time.time())
    mymessage.write(mytime, title, text, sender, priority, reciever, otherRecievers, files)

################################################################
def debugBreakPoint(message, location, stopBreak = False):
    # uncomment next line for debugging
    print(str(time.time())+ " :" + str(message)+" :" + str(location) )
    if stopBreak != False:
        prompt ="any key to continue s stops program,at location "+ str(location)
        myanswer = input(prompt)
        if myanswer == "s":
            sys.exit()
    logdata = (str(time.time()) + " :" + str(message) + " :" + str(location) + " :" + str(stopBreak) + "\n")
    with open(grendelLogData + "masterlog.log", 'a+') as f:
           f.write(logdata)
    f.close

###############################################################
def shutdownGrendel():
    debugBreakPoint("in shutdownGrendel", "grendelconfig.py")
    makeMsg("shutdown","shutdown","1","all","all","NONE")

###############################################################
class message():
    indexNumber = 0

    def __init__(self):
        debugBreakPoint("in message init", "grendelconfig.py")
        self.indexNumber = message.indexNumber
        self.timeStamp = ""
        self.title = ""
        self.text = ""
        self.primeRecipient = ""
        self.priority = ""
        self.sender = ""
        self.otherRecipients = ""
        self.files = ""
        message.indexNumber = message.indexNumber + 1

    #######################################
    def saveMessageNumber(self):
       debugBreakPoint("in saveMessageNumber", "grendelconfig.py")
       mydata = [message.indexNumber]
       jsonData = json.dumps(mydata, sort_keys = True,  indent = 4, separators = (",", ": "))
       with open("currentMessageNumber", 'w') as f:
           f.write(jsonData)

    ##############################################

    def loadMessageNumber (self):
        pass

    ###############################################

    def write(self, timeStamp, title, text, sender , priority, primeRecipient , otherRecipients, files ):
        debugBreakPoint("in messageWrite", "grendelconfig.py")
        debugBreakPoint(timeStamp, "grendelconfig.py")

        myCurrentDir = os.getcwd()
        mydata = [timeStamp, title, text, sender, priority, primeRecipient, otherRecipients, files, self.indexNumber]
        debugBreakPoint(mydata, "grendelconfig.py")

        jsonData = json.dumps(str(mydata), sort_keys = True,  indent = 4, separators = (",", ": "))
        debugBreakPoint(jsonData, "grendelconfig.py")
        debugBreakPoint(primeRecipient,"grendelconfig.py")
        filename = str(timeStamp)+sender
        if primeRecipient == "AI":
            os.chdir(msgPathAI)
        elif primeRecipient == "PY":
            os.chdir(msgPathPY)
        elif primeRecipient == "OT":
            os.chdir(msgPathOT)
        elif primeRecipient == "all":
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
    def read(self,timeStamp,program):
        debugBreakPoint("message.read we are here", "grendelconfig.py")
        myCurrentDir = os.getcwd()
        filename = timeStamp
        if program == "AI":
            os.chdir(msgPathAI)
        elif program == "PY":
            os.chdir(msgPathPY)
        elif program == "OT":
            os.chdir(msgPathOT)
        with open(filename, "r") as content:
            print("now trying to read json data")
            datastuff = json.load(content)

            print(datastuff)

            #self.timeStamp = datastuff[0]
            #self.title
            return datastuff
        os.chdir(myCurrentDir)

####################################################################