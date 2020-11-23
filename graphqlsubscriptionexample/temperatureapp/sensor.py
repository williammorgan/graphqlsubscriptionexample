import threading
import time
import random

import django.utils.timezone

from temperatureapp import schema
from temperatureapp.models import TemperatureMeasurement

SENSOR_WAIT_TIME = 1

def take_measurement_value():
    return round(random.random() * 25.0, 2)

def sensor_thread_entry_point():
    time.sleep(SENSOR_WAIT_TIME * 5)
    while True:
        time.sleep(SENSOR_WAIT_TIME)
        measurement = TemperatureMeasurement(
            timestamp=django.utils.timezone.now(),
            value=take_measurement_value(),
        )
        measurement.save()

        schema.CurrentTemperatureSubscription.broadcast(
            group="temperature_group",
            payload=measurement,
        )


def start():
    sensor_thread = threading.Thread(
        target=sensor_thread_entry_point
    )
    sensor_thread.daemon=True
    sensor_thread.start()
