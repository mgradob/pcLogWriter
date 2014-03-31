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

    handshakeLog = Logs.HandshakeLog
    moistureLog1 = Logs.MoistureLog
    moistureLog2 = Logs.MoistureLog
    weatherLog = Logs.WeatherLog
    pumpLog = Logs.PumpLog
    timeoutLog = Logs.TimeoutLog

    try:
    # First Protocol, reading shit tons of data, from tons of
    # sensors and stuff.

        # Get SOH
        handshakeLog.soh = str(dataIn[15])
        # Get the EOT
        handshakeLog.eot = str(dataIn[51])

        # Get Node1
        moistureLog1.node_id = str(dataIn[16])
        # Set height1
        moistureLog1.height1 = 1
        # Get moistures1
        moistureLog1.moisture1 = str(dataIn[17]) + '.' + str(dataIn[18])
        # Set height2
        moistureLog1.height2 = 2
        # Get moistures2
        moistureLog1.moisture2 = str(dataIn[19]) + '.' + str(dataIn[20])
        # Set height3
        moistureLog1.height3 = 3
        # Get moistures3
        moistureLog1.moisture3 = str(dataIn[21]) + '.' + str(dataIn[22])

        # Get Node2
        moistureLog2.node_id = str(dataIn[23])
        # Set height1
        moistureLog2.height1 = 1
        # Get moistures1
        moistureLog2.moisture1 = str(dataIn[24]) + '.' + str(dataIn[25])
        # Set height2
        moistureLog2.height = 2
        # Get moistures2
        moistureLog2.moisture2 = str(dataIn[26]) + '.' + str(dataIn[27])
        # Set height3
        moistureLog2.height3 = 3
        # Get moistures3
        moistureLog2.moisture3 = str(dataIn[28]) + '.' + str(dataIn[29])

        # Get Climate Node
        weatherLog.node_id = str(dataIn[30])
        # Get radiation
        weatherLog.radiation = str((dataIn[31] << 8) | dataIn[32])
        # Get atmospheric humidity
        weatherLog.atmospheric_humidity = str(dataIn[33]) + '.' + str(dataIn[34])
        # Get atmospheric temperature
        weatherLog.atmospheric_temperature = str(dataIn[35]) + '.' + str(dataIn[36])
        # Get wind speed
        weatherLog.wind_speed = str(dataIn[37]) + '.' + str(dataIn[38])

        # Get Pump
        pumpLog.node_id = str(dataIn[39])
        pumpLog.relay_status = str(dataIn[40])
        pumpLog.pulse_count = str((dataIn[41] << 8) | dataIn[42])

        # Get Timeouts
        timeoutLog.consolidate = str(dataIn[44]) + '.' + str(dataIn[45])
        timeoutLog.timeout_DAAD = str(dataIn[46])
        timeoutLog.timeout_DA55 = str(dataIn[47])
        timeoutLog.timeout_c = str(dataIn[48])
        timeoutLog.timeout_climate_node = str(dataIn[49])
        timeoutLog.timeout_pump_node = str(dataIn[50])

    # Second protocol, reading only 6 bytes, 3 pairs of humidity
    #     # Get moisture higher byte, "xx.__"
    #     moistureLog["moistureHB1"] = str(dataIn[15])
    #     # Get moisture lower byte, "__.xx"
    #     moistureLog["moistureLB1"] = str(dataIn[16])
    #     # Get moisture higher byte, "xx.__"
    #     moistureLog["moistureHB2"] = str(dataIn[17])
    #     # Get moisture lower byte, "__.xx"
    #     moistureLog["moistureLB2"] = str(dataIn[18])
    #     # Get moisture higher byte, "xx.__"
    #     moistureLog["moistureHB3"] = str(dataIn[19])
    #     # Get moisture lower byte, "__.xx"
    #     moistureLog["moistureLB3"] = str(dataIn[20])
    #     # Get moisture higher byte, "xx.__"
    #     moistureLog["moistureHB4"] = str(dataIn[21])
    #     # Get moisture lower byte, "__.xx"
    #     moistureLog["moistureLB4"] = str(dataIn[22])
    #     # Get moisture higher byte, "xx.__"
    #     moistureLog["moistureHB5"] = str(dataIn[23])
    #     # Get moisture lower byte, "__.xx"
    #     moistureLog["moistureLB5"] = str(dataIn[24])
    #     # Get moisture higher byte, "xx.__"
    #     moistureLog["moistureHB6"] = str(dataIn[25])
    #     # Get moisture lower byte, "__.xx"
    #     moistureLog["moistureLB6"] = str(dataIn[26])

        formattedData = moistureLog1.moisture1 + ',' + moistureLog1.moisture2 + ',' + moistureLog1.moisture3 + ',' + \
                        moistureLog2.moisture1 + ',' + moistureLog2.moisture2 + ',' + moistureLog2.moisture3

        # Send data to Xively API
        now = datetime.datetime.utcnow()
        apiFunctions.send_moisture_data(moistureLog1, moistureLog2, now)
        apiFunctions.send_weather_data(weatherLog, now)
        apiFunctions.send_pump_data(pumpLog, now)
        apiFunctions.send_consolidate_data(timeoutLog, now)

    except Exception:
        formattedData = "Timeout received"
        pass

    return formattedData

    # Generic stuff, for all protocols
    # Get date value
    #date = datetime.datetime.now('%Y-%m-%d %H:%M')
    #date = strftime("%Y-%m-%d %H:%M")
    #moistureLog["date"] = str(date)

    #if moistureLog["timeout"] == "1":
    #    formattedData = "Timeout received, %s" % ([moistureLog["date"]])
    #    return formattedData
    # if handshakeLog.soh != "1" or handshakeLog.eot != "4":
    #     formattedData = ["Message corrupted"]
    #     return formattedData
    # else:
            # dataHeight1 = "%s,%s,%s.%s,%s,%s,%s" % (moistureLog["area_id"], moistureLog["height1"], moistureLog["moistureHB1"], moistureLog["moistureLB1"],
            #                                              moistureLog["min"], moistureLog["max"], moistureLog["date"])
            # dataHeight2 = "%s,%s,%s.%s,%s,%s,%s" % (moistureLog["area_id"], moistureLog["height2"], moistureLog["moistureHB2"], moistureLog["moistureLB2"],
            #                                              moistureLog["min"], moistureLog["max"], moistureLog["date"])
            # dataHeight3 = "%s,%s,%s.%s,%s,%s,%s" % (moistureLog["area_id"], moistureLog["height3"], moistureLog["moistureHB3"], moistureLog["moistureLB3"],
            #                                              moistureLog["min"], moistureLog["max"], moistureLog["date"])

            #dataHeight1 = "Altura 1: %s.%s\t %s" % (moistureLog["moistureHB1"], moistureLog["moistureLB1"], moistureLog["date"])
            #dataHeight2 = "Altura 2: %s.%s\t %s" % (moistureLog["moistureHB2"], moistureLog["moistureLB2"], moistureLog["date"])
            #dataHeight3 = "Altura 3: %s.%s\t %s" % (moistureLog["moistureHB3"], moistureLog["moistureLB3"], moistureLog["date"])

        # dataToWrite = "%s.%s,%s.%s,%s.%s,%s.%s,%s.%s,%s.%s,%s,%s,%s" % \
        #                   (moistureLog["moistureHB1"], moistureLog["moistureLB1"],
        #                    moistureLog["moistureHB2"], moistureLog["moistureLB2"],
        #                    moistureLog["moistureHB3"], moistureLog["moistureLB3"],
        #                    moistureLog["moistureHB4"], moistureLog["moistureLB4"],
        #                    moistureLog["moistureHB5"], moistureLog["moistureLB5"],
        #                    moistureLog["moistureHB6"], moistureLog["moistureLB6"],
        #                    moistureLog["timeout1"], moistureLog["timeout2"],
        #                    moistureLog["date"])

    #return formattedData

#-------------------------------------------------------------------
