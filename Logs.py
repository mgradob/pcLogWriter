__author__ = 'Laptop Miguel'


# Generic handshake log ------------------------------------------------
class HandshakeLog:
    soh = ''
    eot = ''


# Generic moisture log -------------------------------------------------
class MoistureLog:
    node_id = ''
    height1 = ''
    height2 = ''
    height3 = ''
    moisture1 = ''
    moisture2 = ''
    moisture3 = ''


# Generic weather log --------------------------------------------------
class WeatherLog:
    node_id = ''
    radiation = ''
    atmospheric_humidity = ''
    atmospheric_temperature = ''
    wind_speed = ''


# Generic pump log -----------------------------------------------------
class PumpLog:
    node_id = ''
    relay_status = ''
    water_flow = ''


# Generic timeout log --------------------------------------------------
class TimeoutLog:
    consolidate = ''
    evapotraspiration = ''
    timeout_DAAD = ''
    timeout_DA55 = ''
    timeout_c = ''
    timeout_climate_node = ''
    timeout_pump_node = ''