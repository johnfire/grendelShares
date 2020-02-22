
import os
import json


msgPath = "/media/grendelData102/GrendelData/grendelMsgs/"
msgPathAI = "/media/grendelData102/GrendelData/grendelMsgs/AI"
msgPathPY = "/media/grendelData102/GrendelData/grendelMsgs/PY"
msgPathOT = "/media/grendelData102/GrendelData/grendelMsgs/OT"
fotoPath = "/media/grendelData102/GrendelData/grendelFotos/"
audioPath = "/media/grendelData102/GrendelData/grendellAudio/"
grendelOtherData = "/media/grendelData102/GrendelData/grendelOtherData/"
grendelPeopleData = "/media/grendelData102/GrendelData/grendelPeopleData/"
processFotoPath ="/media/grendelData102/lowLevelPrograms/processFoto.py "

class message():

    def write(timeStamp, title, text, primeRecipient, priority, sender, otherRecipients, files ):
        print(timeStamp)

        myCurrentDir = os.getcwd()
        mydata = [timeStamp, title, text, primeRecipient, priority, sender, otherRecipients, files]
        jsonData = json.dumps(mydata, sort_keys = True,  indent = 4, separators = (",", ": "))
        filename = str(timeStamp)
        if primeRecipient == "AI":
            os.chdir(msgPathAI)
        elif primeRecipient == "PY":
            os.chdir(msgPathPY)
        elif primeRecipient == "OT":
            os.chdir(msgPathOT)
        with open(filename, 'w') as f:
             f.write(jsonData)
        os.chdir(myCurrentDir)


    def read(timeStamp, program):
        myCurrentDir = os.getcwd()
        filename = timeStamp
        if program == "AI":
            os.chdir(msgPathAI)
        elif program == "PY":
            os.chdir(msgPathPY)
        elif program == "OT":
            os.chdir(msgPathOT)
        with open(filename, "r") as content:
            datastuff = json.load(content)
            return datastuff
        os.chdir(myCurrentDir)



