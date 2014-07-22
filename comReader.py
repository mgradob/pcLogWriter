__author__ = 'Adriana'

import serial
import comFunctions
import writeToFile
import datetime
import time

com_functions = comFunctions.ComFunctions()

print("Available ports:\n")
portList = com_functions.getAvailablePorts()
if len(portList) < 1:
    print("No COM ports found")
else:
    print(portList)
    print("Select a COM port:\nCOM")
    selectedPort = 3
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

            formattedData = com_functions.formatMoistureData(dataIn)

            print(str(datetime.datetime.now()) + ': ' + formattedData)

            writeToFile.writeToFile(formattedData)

            serialPort.close()

        else:
            writeToFile.writeToFile(formattedData)
