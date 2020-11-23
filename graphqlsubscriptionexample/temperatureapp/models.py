from django.db import models

# Create your models here.

class TemperatureMeasurement(models.Model):
    timestamp = models.DateTimeField()
    value = models.FloatField()

    def __str__(self):
        return f"{self.value} Degrees Celsius at {self.timestamp}"
