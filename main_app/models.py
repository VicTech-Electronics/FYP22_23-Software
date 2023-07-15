from django.db import models

class Information(models.Model):
    vehicle_number = models.CharField(max_length=10)
    latitude = models.FloatField()
    longitude = models.FloatField()
    description = models.TextField()
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)

    def __str__(self):
        return self.vehicle_number
