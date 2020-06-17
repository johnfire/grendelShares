"""

# this is a set up and config file for the other programs.

# also all code that is used by multiple programs goes here.
# christopher rehm  15 jan 2020
#
"""

import os
import time
import json
import logging

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

programPath = "/media/grendelData102/grendelProject/"


###############################################################
def makeMsg(sender, title, text, priority, reciever, otherRecievers, files):
    """Make a message to send.

    Parameters
    ----------
    sender : TYPE
        DESCRIPTION.
    title : TYPE
        DESCRIPTION.
    text : TYPE
        DESCRIPTION.
    priority : TYPE
        DESCRIPTION.
    reciever : TYPE
        DESCRIPTION.
    otherRecievers : TYPE
        DESCRIPTION.
    files : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    logging.debug('Entering makeMsg')
    mymessage = message()
    mytime = str(time.time())
    mymessage.write(mytime, sender, title, text, priority,
                    reciever, otherRecievers, files)


################################################################
def debugBreakPoint(message, location, stopBreak=False):
    """Create a debug break point.

    Parameters
    ----------
    message : TYPE
        DESCRIPTION.
    location : TYPE
        DESCRIPTION.
    stopBreak : TYPE, optional
        DESCRIPTION. The default is False.

    Returns
    -------
    None.

    """
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
    """Grendel shutdown message.

    Returns
    -------
    None.

    """
    logging.debug('In shutdownGrendel')
    makeMsg("zero", "shutdown", "shutdown", "1", "ALL", "ALL", "NONE")


###############################################################
class message():
    """Set up a message."""

    indexNumber = 0

    def __init__(self):
        logging.debug('In message init')
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
        """Save a message by number.

        Returns
        -------
        None.

        """
        logging.debug('In saveMessageNumber')
        mydata = [message.indexNumber]
        jsonData = json.dumps(mydata, sort_keys=True,  indent=4, separators=(",", ": "))
        with open("currentMessageNumber", 'w') as f:
            f.write(jsonData)

##########################################

    def loadMessageNumber(self):
        """Load a message by number.

        Returns
        -------
        None.

        """
        logging.debug('in loadMessageNumber')
        pass

###############################################

    def write(self, timeStamp, title, text, sender, priority, primeRecipient, otherRecipients, files):
        """In write a message function.

        Parameters
        ----------
        timeStamp : TYPE
            DESCRIPTION.
        title : TYPE
            DESCRIPTION.
        text : TYPE
            DESCRIPTION.
        sender : TYPE
            DESCRIPTION.
        priority : TYPE
            DESCRIPTION.
        primeRecipient : TYPE
            DESCRIPTION.
        otherRecipients : TYPE
            DESCRIPTION.
        files : TYPE
            DESCRIPTION.

        Returns
        -------
        str
            DESCRIPTION.

        """
        logging.debug('In message Write')
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
        jsonData = json.dumps(mydata,
                              sort_keys=True,
                              indent=4,
                              separators=(",", ": "))
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
        """Read a message.

        Parameters
        ----------
        msgStamp : TYPE
            DESCRIPTION.
        program : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        myCurrentDir = os.getcwd()
        filename = msgStamp
        if program == "AI":
            os.chdir(msgPathAI)
        elif program == "PY":
            os.chdir(msgPathPY)
        elif program == "OT":
            os.chdir(msgPathOT)
        with open(filename, "r") as content:
            logging.debug('now trying to read json data')
            datastuff = json.load(content)
            self.timeStamp = datastuff[0]
            logging.debug(self.timeStamp)
            self.title = datastuff[1]
            logging.debug(self.title)
            self.text = datastuff[2]
            self.sender = datastuff[3]
            self.priority = datastuff[4]
            self.primeRecipient = datastuff[5]
            self.otherRecipients = datastuff[6]
            self.files = datastuff[7]
            self.indexNumber = datastuff[8]

            return datastuff
        os.chdir(myCurrentDir)
