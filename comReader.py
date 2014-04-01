import time

__author__ = 'Adriana'

import serial
import comFunctions
from writeToFile import *

print("Available ports:\n")

portList = comFunctions.getAvailablePorts()

if len(portList) < 1:
    print("No COM ports found")
else:
    print(portList)
    print("Select a COM port:\nCOM")
    selectedPort = int(input())-1

    while 1:
        serialPort = serial.Serial(selectedPort)

        startTime = time.clock()

        while serialPort.inWaiting() < 1:
            elapsedTime = time.clock() - startTime
            #print(elapsedTime)


            if elapsedTime > 360:
                print('Time limit elapsed')
                serialPort.close()
                break
            else:
                pass

        if serialPort.isOpen():
            dataIn = (serialPort.readline())

            formattedData = comFunctions.formatMoistureData(dataIn)

            print(formattedData)

            writeToFile(formattedData)

            serialPort.close()
        else:
            pass