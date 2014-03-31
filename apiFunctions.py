__author__ = 'Laptop Miguel'

import xively
import Logs

api = xively.XivelyAPIClient('a9KrKo29wXCznae6xgGhVX7sGS1Q8E809vFAKWPoFU5g4RQy')
feed = api.feeds.get(1129833362)


def send_moisture_data(moisture_log_1=Logs.MoistureLog, moisture_log_2=Logs.MoistureLog):
    feed.datastreams = [
        xively.Datastream('HM1_S1', current_value=moisture_log_1.moisture1),
        xively.Datastream('HM2_S1', current_value=moisture_log_1.moisture2),
        xively.Datastream('HM3_S1', current_value=moisture_log_1.moisture3),
        xively.Datastream('HM1_S2', current_value=moisture_log_2.moisture1),
        xively.Datastream('HM2_S2', current_value=moisture_log_2.moisture2),
        xively.Datastream('HM3_S2', current_value=moisture_log_2.moisture1)
    ]
    feed.update()


def send_weather_data(weather_log=Logs.WeatherLog):
    feed.datastreams = [
        xively.Datastream('Atm_Humidity', current_value=weather_log.atmospheric_humidity),
        xively.Datastream('Atm_Temperature', current_value=weather_log.atmospheric_temperature),
        xively.Datastream('Radiation', current_value=weather_log.radiation),
        xively.Datastream('Wind_Speed', current_value=weather_log.wind_speed)
    ]
    feed.update()


def send_pump_data(pump_log=Logs.PumpLog):
    feed.datastreams = [
        xively.Datastream('Pump_State', current_value=pump_log.relay_status),
        xively.Datastream('Water_Flow', current_value=pump_log.pulse_count)
    ]
    feed.update()


def send_consolidate_data(timeout_log=Logs.TimeoutLog):
    feed.datastreams = [
        xively.Datastream('Cons_Humidity', current_value=timeout_log.consolidate)
    ]
    feed.update()