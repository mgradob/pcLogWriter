import sys

__author__ = 'Adriana'

import serial
import datetime
import Logs
import apiFunctions
import writeToFile

class ComFunctions():
    def __init__(self):
        pass

    def get_graph_data(self):
        return self.graph_data

    # Get a list of available COM ports in the system ------------------
    def getAvailablePorts(self):
        comInSystem = []
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
    def formatMoistureData(self, dataIn):

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
            handshakeLog.eot = str(int(dataIn[53]))

            # Get Node1
            moistureLog1.node_id = str(int(dataIn[16]))
            # Set height1
            moistureLog1.height1 = 1
            # Get moistures1
            moistureLog1.moisture1 = str(dataIn[17] + dataIn[18]/100)
            # Set height2
            moistureLog1.height2 = 2
            # Get moistures2
            moistureLog1.moisture2 = str(dataIn[19] + dataIn[20]/100)
            # Set height3
            moistureLog1.height3 = 3
            # Get moistures3
            moistureLog1.moisture3 = str(dataIn[21] + dataIn[22]/100)

            # Get Node2
            moistureLog2.node_id = str(int(dataIn[23]))
            # Set height1
            moistureLog2.height1 = 1
            # Get moistures1
            moistureLog2.moisture1 = str(dataIn[24] + dataIn[25]/100)
            # Set height2
            moistureLog2.height = 2
            # Get moistures2
            moistureLog2.moisture2 = str(dataIn[26] + dataIn[27]/100)
            # Set height3
            moistureLog2.height3 = 3
            # Get moistures3
            moistureLog2.moisture3 = str(dataIn[28] + dataIn[29]/100)

            # Get Climate Node
            weatherLog.node_id = str(int(dataIn[30]))
            # Get radiation
            weatherLog.radiation = str(int((dataIn[31] << 8) | dataIn[32]))
            # Get atmospheric humidity
            weatherLog.atmospheric_humidity = str(dataIn[33] + dataIn[34]/100)
            # Get atmospheric temperature
            weatherLog.atmospheric_temperature = str(dataIn[35] + dataIn[36]/100)
            # Get wind speed
            weatherLog.wind_speed = str(dataIn[37] + dataIn[38]/100)
            # Get evapotranspiration
            weatherLog.evapotranspiration = str(dataIn[39] + dataIn[40]/100)

            # Get Pump
            pumpLog.node_id = str(int(dataIn[41]))
            pumpLog.relay_status = str(int(dataIn[42]))
            pumpLog.water_flow = str(dataIn[43] + dataIn[44]/100)

            # Get Timeouts
            timeoutLog.consolidate = str(dataIn[46] + dataIn[47]/100)
            timeoutLog.timeout_DAAD = str(int(dataIn[48]))
            timeoutLog.timeout_DA55 = str(int(dataIn[49]))
            timeoutLog.timeout_c = str(int(dataIn[50]))
            timeoutLog.timeout_climate_node = str(int(dataIn[51]))
            timeoutLog.timeout_pump_node = str(int(dataIn[52]))

            formattedData = timeoutLog.consolidate + ',' + moistureLog1.moisture1 + ',' + moistureLog1.moisture2 + ',' + \
                            moistureLog1.moisture3 + ',' + moistureLog2.moisture1 + ',' + moistureLog2.moisture2 + ',' + \
                            moistureLog2.moisture3 + ',' + weatherLog.radiation + ',' + weatherLog.atmospheric_humidity +\
                            ',' + weatherLog.atmospheric_temperature + ',' + weatherLog.wind_speed + ',' + \
                            weatherLog.evapotranspiration + ',' + pumpLog.relay_status + ',' + pumpLog.water_flow + ',' \
                            + timeoutLog.timeout_DAAD + ',' + timeoutLog.timeout_DA55 + ',' + timeoutLog.timeout_c + ',' \
                            + timeoutLog.timeout_climate_node + ',' + timeoutLog.timeout_pump_node
        except Exception:
            print(sys.exc_info())
            print(str(datetime.datetime.now()) + ': Exception, invalid data received')
            formattedData = 'i,i,i,i,i,i,i,i,i,i,i,i,i,i,i'

        # Send data to Xively API
        try:
            now = datetime.datetime.utcnow()
            apiFunctions.send_moisture_data(moistureLog1, moistureLog2, now)
            apiFunctions.send_weather_data(weatherLog, now)
            apiFunctions.send_pump_data(pumpLog, now)
            apiFunctions.send_consolidate_data(timeoutLog, now)
        except Exception:
            print(str(datetime.datetime.now()) + ': Exception, did not send data to Xively')

        writeToFile.write_graph_file(str(weatherLog.evapotranspiration))

        try:
            return formattedData
        except Exception:
            print(str(datetime.datetime.now()) + ': Exception, incorrect data received')
            return 'i,i,i,i,i,i,i,i,i,i,i,i,i,i,i'