__author__ = 'Adriana'

import serial
import comFunctions
from writeToFile import *
import datetime
import time

print("Available ports:\n")

portList = comFunctions.getAvailablePorts()

if len(portList) < 1:
    print("No COM ports found")
else:
    print(portList)
    print("Select a COM port:\nCOM")
    selectedPort = int(input())-1
    formattedData = ''

    while 1:
        serialPort = serial.Serial(selectedPort, 9600, timeout=90)
        startTime = time.clock()

        while serialPort.inWaiting() < 1:
            elapsedTime = time.clock() - startTime

            if elapsedTime > 180:
                print(str(datetime.datetime.now()) + ': Time limit elapsed')
                formattedData = 't,t,t,t,t,t,t,t,t,t,t,t,t,t,t'
                serialPort.close()
                break
            else:
                pass

        if serialPort.isOpen():
            dataIn = (serialPort.read(size=55))

            formattedData = comFunctions.formatMoistureData(dataIn)

            print(str(datetime.datetime.now()) + ': ' + formattedData)

            writeToFile(formattedData)

            serialPort.close()

        else:
            writeToFile(formattedData)
