__author__ = 'Adriana'

from time import strftime
import os

# Make file of data received ---------------------------------------
date = None

def setDate(exactTime):
   global date
   date = exactTime

def getDate():
    global date
    return date

def writeToFile(dataToWrite):
    if os.path.exists(os.path.abspath('dataLog.txt')):
        with open('dataLog.txt', 'a+') as file:
             print(dataToWrite)
             file.write(dataToWrite + "," + strftime("%Y-%m-%d %H:%M") + '\n')
    else:
        print('Log file created')
        with open("dataLog.txt", 'w') as file:
             print(dataToWrite)
             file.write(dataToWrite + "," + strftime("%Y-%m-%d %H:%M") + '\n')

    print("Data written successfully")
#-------------------------------------------------------------------