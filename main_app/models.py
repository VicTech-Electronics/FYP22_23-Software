from django.db import models
from django.contrib.auth.models import User

class Device(models.Model):
    device_user = models.OneToOneField(User, null=False, on_delete=models.CASCADE)
    device_number = models.CharField(max_length=50)
    contacts = models.CharField(max_length=20)

    def __str__(self):
        return self.device_number
    
class Request(models.Model):
    device = models.ForeignKey(Device, null=False, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    heart_rate = models.FloatField()
    body_temperature = models.FloatField()

    def __str__(self):
        return self.device.device_user.username