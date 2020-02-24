
import os
import json
import sys

msgPath = "/media/grendelData102/GrendelData/grendelMsgs/"
msgPathAI = "/media/grendelData102/GrendelData/grendelMsgs/AI"
msgPathPY = "/media/grendelData102/GrendelData/grendelMsgs/PY"
msgPathOT = "/media/grendelData102/GrendelData/grendelMsgs/OT"
fotoPath = "/media/grendelData102/GrendelData/grendelFotos/"
audioPath = "/media/grendelData102/GrendelData/grendellAudio/"
grendelOtherData = "/media/grendelData102/GrendelData/grendelOtherData/"
grendelWorldData = "/media/grendelData102/GrendelData/grendelWorldData/"
processFotoPath ="/media/grendelData102/lowLevelPrograms/processFoto.py "

#def makeMsg(title, text, priority, reciever, otherRecievers, files):
#    mytime = time.time()
#    mymessage = gc.message
#    mymessage.write(mytime, title, text, "AI", priority, reciever, otherRecievers, files)

################################################################
def debugBreakPoint(location):
    message ="any key to continue s stops program,at location "+ str(location)
    myanswer = input(message)
    if myanswer == "s":
        sys.exit()

###############################################################
###############################################################
class message():

    def __init__(self):
        self.timeStamp = ""
        self.title = ""
        self.text = ""
        self.primeRecipient = ""
        self.priority = ""
        self.sender = ""
        self.otherRecipients = ""
        self.files = ""

    #######################################

    def write(self,timeStamp, title, text, primeRecipient, priority, sender, otherRecipients, files ):

        print(timeStamp)

        myCurrentDir = os.getcwd()
        mydata = [str(timeStamp), title, text, primeRecipient, priority, sender, otherRecipients, files]
        jsonData = json.dumps(mydata, sort_keys = True,  indent = 4, separators = (",", ": "))
        filename = str(timeStamp)+sender
        if primeRecipient == "AI":
            os.chdir(msgPathAI)
        elif primeRecipient == "PY":
            os.chdir(msgPathPY)
        elif primeRecipient == "OT":
            os.chdir(msgPathOT)
        with open(filename, 'w') as f:
             f.write(jsonData)
        os.chdir(myCurrentDir)

    ##########################################################
    def read(self,timeStamp, program):
        myCurrentDir = os.getcwd()
        filename = timeStamp
        if program == "AI":
            os.chdir(msgPathAI)
        elif program == "PY":
            os.chdir(msgPathPY)
        elif program == "OT":
            os.chdir(msgPathOT)
        with open(filename, "r") as content:
            datastuff = json.loads(content)
            return datastuff
        os.chdir(myCurrentDir)

####################################################################