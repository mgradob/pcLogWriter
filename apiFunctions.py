__author__ = 'Laptop Miguel'

import xively
import Logs
import datetime

api = xively.XivelyAPIClient('a9KrKo29wXCznae6xgGhVX7sGS1Q8E809vFAKWPoFU5g4RQy')
feed = api.feeds.get(1129833362)


def send_moisture_data(moisture_log_1=Logs.MoistureLog, moisture_log_2=Logs.MoistureLog, now=datetime):
    now = datetime.datetime.utcnow()
    feed.datastreams = [
        xively.Datastream('HM1_S1', current_value=moisture_log_1.moisture1, at=now),
        xively.Datastream('HM2_S1', current_value=moisture_log_1.moisture2, at=now),
        xively.Datastream('HM3_S1', current_value=moisture_log_1.moisture3, at=now),
        xively.Datastream('HM1_S2', current_value=moisture_log_2.moisture1, at=now),
        xively.Datastream('HM2_S2', current_value=moisture_log_2.moisture2, at=now),
        xively.Datastream('HM3_S2', current_value=moisture_log_2.moisture3, at=now)
    ]
    feed.update()


def send_weather_data(weather_log=Logs.WeatherLog, now=datetime):
    feed.datastreams = [
        xively.Datastream('Atm_Humidity', current_value=weather_log.atmospheric_humidity, at=now),
        xively.Datastream('Atm_Temperature', current_value=weather_log.atmospheric_temperature, at=now),
        xively.Datastream('Radiation', current_value=weather_log.radiation, at=now),
        xively.Datastream('Wind_Speed', current_value=weather_log.wind_speed, at=now),
        xively.Datastream('Evapotranspiration', current_value=weather_log.evapotranspiration, at=now)
    ]
    feed.update()


def send_pump_data(pump_log=Logs.PumpLog, now=datetime):
    feed.datastreams = [
        xively.Datastream('Pump_State', current_value=pump_log.relay_status, at=now),
        xively.Datastream('Water_Flow', current_value=pump_log.water_flow, at=now)
    ]
    feed.update()


def send_consolidate_data(timeout_log=Logs.TimeoutLog, now=datetime):
    feed.datastreams = [
        xively.Datastream('Cons_Humidity', current_value=timeout_log.consolidate, at=now)
    ]
    feed.update()