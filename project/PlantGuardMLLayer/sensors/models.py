from django.db import models

class Pi(models.Model):
    pi_id = models.CharField(max_length=100)
    gas_resistance = models.FloatField()
    humidity = models.FloatField()
    lux = models.FloatField()
    pressure = models.FloatField()
    rawVal = models.FloatField()
    temperature = models.FloatField()
    timestamp = models.DateTimeField()
    volts = models.FloatField()
    



