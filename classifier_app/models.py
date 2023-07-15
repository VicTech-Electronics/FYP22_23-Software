from django.db import models
from main_app.models import Vehicle

# Create your models here.
class AccidentIndicator(models.Model):
    vehicle = models.ForeignKey(Vehicle, null=False, on_delete=models.CASCADE)
    flame = models.BooleanField()
    smoke = models.FloatField()
    vibration = models.FloatField()
    gyroscope = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    brake = models.BooleanField()
    
