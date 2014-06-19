__author__ = 'Adriana'

import serial
import datetime
from time import *
import Logs
import apiFunctions

# Get a list of available COM ports in the system ------------------
comInSystem = []

def getAvailablePorts():
    for i in range(0, 255):
        try:
            avPort = serial.Serial(i)
            comInSystem.append("COM" + str(i+1))
            avPort.close()
        except serial.SerialException:
            pass

    return comInSystem
#-------------------------------------------------------------------

# Format received string -------------------------------------------
def formatMoistureData(dataIn):

    handshakeLog = Logs.HandshakeLog()
    moistureLog1 = Logs.MoistureLog()
    moistureLog2 = Logs.MoistureLog()
    weatherLog = Logs.WeatherLog()
    pumpLog = Logs.PumpLog()
    timeoutLog = Logs.TimeoutLog()

    try:
    # First Protocol, reading shit tons of data, from tons of
    # sensors and stuff.

        # Get SOH
        handshakeLog.soh = str(int(dataIn[15]))
        # Get the EOT
        handshakeLog.eot = str(int(dataIn[51])) #53

        # Get Node1
        moistureLog1.node_id = str(int(dataIn[16]))
        # Set height1
        moistureLog1.height1 = 1
        # Get moistures1
        moistureLog1.moisture1 = str(int(dataIn[17])) + '.' + str(int(dataIn[18]))
        # Set height2
        moistureLog1.height2 = 2
        # Get moistures2
        moistureLog1.moisture2 = str(int(dataIn[19])) + '.' + str(int(dataIn[20]))
        # Set height3
        moistureLog1.height3 = 3
        # Get moistures3
        moistureLog1.moisture3 = str(int(dataIn[21])) + '.' + str(int(dataIn[22]))

        # Get Node2
        moistureLog2.node_id = str(int(dataIn[23]))
        # Set height1
        moistureLog2.height1 = 1
        # Get moistures1
        moistureLog2.moisture1 = str(int(dataIn[24])) + '.' + str(int(dataIn[25]))
        # Set height2
        moistureLog2.height = 2
        # Get moistures2
        moistureLog2.moisture2 = str(int(dataIn[26])) + '.' + str(int(dataIn[27]))
        # Set height3
        moistureLog2.height3 = 3
        # Get moistures3
        moistureLog2.moisture3 = str(int(dataIn[28])) + '.' + str(int(dataIn[29]))

        # Get Climate Node
        weatherLog.node_id = str(int(dataIn[30]))
        # Get radiation
        weatherLog.radiation = str(int((dataIn[31] << 8) | dataIn[32]))
        # Get atmospheric humidity
        weatherLog.atmospheric_humidity = str(int(dataIn[33])) + '.' + str(int(dataIn[34]))
        # Get atmospheric temperature
        weatherLog.atmospheric_temperature = str(int(dataIn[35])) + '.' + str(int(dataIn[36]))
        # Get wind speed
        weatherLog.wind_speed = str(int(dataIn[37])) + '.' + str(int(dataIn[38]))

        # Get Pump
        pumpLog.node_id = str(int(dataIn[39]))
        pumpLog.relay_status = str(int(dataIn[40]))
        pumpLog.water_flow = str(int((dataIn[41] << 8) | dataIn[42]))

        # Get Timeouts
        timeoutLog.consolidate = str(int(dataIn[44])) + '.' + str(int(dataIn[45]))
        #timeoutLog.evapotraspiration = str(int(dataIn[46])) + '.' + str(int(dataIn[4]))
        timeoutLog.timeout_DAAD = str(int(dataIn[46])) #48
        timeoutLog.timeout_DA55 = str(int(dataIn[47])) #49
        timeoutLog.timeout_c = str(int(dataIn[48])) #50
        timeoutLog.timeout_climate_node = str(int(dataIn[49]))  #51
        timeoutLog.timeout_pump_node = str(int(dataIn[50])) #52

        formattedData = timeoutLog.consolidate + ',' + moistureLog1.moisture1 + ',' + moistureLog1.moisture2 + ',' + \
                        moistureLog1.moisture3 + ',' + moistureLog2.moisture1 + ',' + moistureLog2.moisture2 + ',' + \
                        moistureLog2.moisture3 + ',' + weatherLog.radiation + ',' + weatherLog.atmospheric_humidity +\
                        "," + weatherLog.atmospheric_temperature + ',' + weatherLog.wind_speed + ',' +\
                        pumpLog.relay_status + ',' + timeoutLog.timeout_DAAD + ',' + timeoutLog.timeout_DA55 + ',' + \
                        timeoutLog.timeout_c

        # Send data to Xively API
        now = datetime.datetime.utcnow()
        apiFunctions.send_moisture_data(moistureLog1, moistureLog2, now)
        apiFunctions.send_weather_data(weatherLog, now)
        apiFunctions.send_pump_data(pumpLog, now)
        apiFunctions.send_consolidate_data(timeoutLog, now)

    except Exception:
        print(str(datetime.datetime.now()) + ': Exception, invalid data received')
        formattedData = 'i,i,i,i,i,i,i,i,i,i,i,i,i,i,i'

    try:
        return formattedData
    except Exception:
        print(str(datetime.datetime.now()) + ': Exception, incorrect data received')
        return 'i,i,i,i,i,i,i,i,i,i,i,i,i,i,i'