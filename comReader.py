__author__ = 'Adriana'

import serial
import comFunctions
import writeToFile
import datetime
import time
import Logs
import grapher

graph_data_list = []

print("Available ports:\n")

com_handler = comFunctions.ComFunctions()
portList = com_handler.getAvailablePorts()

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

            formattedData = com_handler.formatMoistureData(dataIn)

            print(str(datetime.datetime.now()) + ': ' + formattedData)

            writeToFile(formattedData)

            serialPort.close()

            if graph_data_list.count() < 10100:
                graph_data_list.append(com_handler.graph_data)
            else:
                for item in graph_data_list:
                    graph_data_list.remove(item)

        else:
            writeToFile(formattedData)
