import datetime
import time

import pytz

from temperatureapp.models import TemperatureMeasurement
from temperatureapp.schema import schema
from temperatureapp.sensor import take_measurement_value

def test_sensor_take_measurement_value():
    for _ in range(1000):
        assert 0.0 <= take_measurement_value() <= 25.0

def test_schema_query(db):
    reused_query = """
        query{
            currentTemperature{
                timestamp
                value
                unit
            }
        }
    """

    # Querying before any measurements were recorded.
    result = schema.execute(reused_query)
    assert result.data == {"currentTemperature": None}

    # Adding a simple measurement, making sure it comes back.
    TemperatureMeasurement.objects.create(
        timestamp=datetime.datetime(2020, 11, 1, 0, 0, 0, tzinfo=pytz.UTC),
        value=24.0,
    )
    result = schema.execute(reused_query)
    inner_result = result.data["currentTemperature"]
    assert inner_result["timestamp"] == "2020-11-01T00:00:00+00:00"
    assert inner_result["value"] == 24.0
    assert inner_result["unit"] == "Degrees Celsius"

    # Adding a later measurement, it should take presedence.
    TemperatureMeasurement.objects.create(
        timestamp=datetime.datetime(2020, 11, 1, 0, 0, 1, tzinfo=pytz.UTC),
        value=23.0,
    )
    result = schema.execute(reused_query)
    inner_result = result.data["currentTemperature"]
    assert inner_result["timestamp"] == "2020-11-01T00:00:01+00:00"
    assert inner_result["value"] == 23.0
    assert inner_result["unit"] == "Degrees Celsius"

    # Adding historical data, it should not change latest reading.
    TemperatureMeasurement.objects.create(
        timestamp=datetime.datetime(2019, 11, 1, 0, 0, 1, tzinfo=pytz.UTC),
        value=22.0,
    )
    result = schema.execute(reused_query)
    inner_result = result.data["currentTemperature"]
    assert inner_result["timestamp"] == "2020-11-01T00:00:01+00:00"
    assert inner_result["value"] == 23.0
    assert inner_result["unit"] == "Degrees Celsius"

