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
import itertools

DEBUG = True

msgPathBase = "mnt/grendelShares"

msgPath = msgPathBase + "/GrendelData/grendelMsgs/"
msgPathAI = msgPathBase + "/GrendelData/grendelMsgs/AI"
msgPathPY = msgPathBase + "/GrendelData/grendelMsgs/PY"
msgPathOT = msgPathBase + "/GrendelData/grendelMsgs/OT"

fotoPath = msgPathBase + "/GrendelData/grendelFotos/"
audioPath = msgPathBase + "/GrendelData/grendellAudio/"

grendelOtherData = msgPathBase + "/GrendelData/grendelOtherData/"
grendelWorldData = msgPathBase + "/GrendelData/grendelWorldData/"
processFotoPath = msgPathBase + "/lowLevelPrograms/processFoto.py"
grendelLogData = msgPathBase + "/grendelLogs/"

programPath = msgPathBase + "/grendelProject/"

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
    mytime = str(time.time())
    mymessage = message(mytime, sender, title, text, priority, reciever, otherRecievers, files)
    mymessage.write()


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

    id_generator = itertools.count(1)

    def __init__(self, timeStamp=".", sender=".", title=".", text=".", priority=".", Recipient=".", otherRecipients=".", files="."):
        """initialises a message object, requires null values for initialiation if object is being created to take data from a .json file.
        the message.read loads the actual data to the instance of the message
        """
        logging.debug('In message init')
        self.indexNumber = next(self.id_generator)
        self.timeStamp = timeStamp
        self.sender = sender
        self.title = title
        self.text = text
        self.priority = priority
        self.Recipient = Recipient
        self.otherRecipients = otherRecipients
        self.files = files


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

    def write(self):
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
        mydata = [self.timeStamp,
                  self.sender,
                  self.title,
                  self.text,
                  self.priority,
                  self.Recipient,
                  self.otherRecipients,
                  self.files,
                  self.indexNumber]
        jsonData = json.dumps(mydata,
                              sort_keys=True,
                              indent=4,
                              separators=(",", ": "))
        # filename = str(timeStamp) + sender + ".json"
        filename = str(self.indexNumber) + self.sender + ".json"
        if self.Recipient == "AI":
            os.chdir(msgPathAI)
        elif self.Recipient == "PY":
            os.chdir(msgPathPY)
        elif self.Recipient == "OT":
            os.chdir(msgPathOT)
        elif self.Recipient == "ALL":
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
            self.Recipient = datastuff[5]
            self.otherRecipients = datastuff[6]
            self.files = datastuff[7]
            self.indexNumber = datastuff[8]

            return datastuff
        os.chdir(myCurrentDir)
