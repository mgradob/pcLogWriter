__author__ = 'Adriana'

import datetime
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
    try:
        if os.path.exists(os.path.abspath('dataLog.txt')):
            with open('dataLog.txt', 'a+') as file:
                 #print(dataToWrite)
                 file.write(dataToWrite + "," + str(datetime.datetime.now()) + '\n')
        else:
            print('Log file created')
            with open("dataLog.txt", 'w') as file:
                 #print(dataToWrite)
                 file.write(dataToWrite + "," + str(datetime.datetime.now()) + '\n')
        print("Data file written successfully")

    except Exception:
        print("Cannot open data file, data not writen")


def write_graph_file(data_to_write):
    try:
        if os.path.exists(os.path.abspath('graphDataLog.txt')):
            with open('graphDataLog.txt', 'a+') as file:
                 #print(dataToWrite)
                 file.write(data_to_write + "," + str(datetime.datetime.now()) + '\n')
        else:
            print('Log file created')
            with open("graphDataLog.txt", 'w') as file:
                 #print(dataToWrite)
                 file.write(data_to_write + "," + str(datetime.datetime.now()) + '\n')

        print("Graph file written successfully")

    except Exception:
        print("Cannot open graph file, data not writen")
#-------------------------------------------------------------------