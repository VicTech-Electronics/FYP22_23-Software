from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Vehicle(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    vehicle_number = models.CharField(max_length=15)
    phone1 = models.CharField(max_length=20)
    phone2 = models.CharField(max_length=20)

    def __str__(self):
        return self.vehicle_number
    

class Hospital(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    reg_number = models.CharField(max_length=500)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.user.username + ' Hospital'
    
class Accident(models.Model):
    vehicle = models.ForeignKey(Vehicle, null=False, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, null=False, on_delete=models.CASCADE)
    confidence = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    status = models.BooleanField(
        default=False,
        choices=[
            (False, 'New'),
            (True, 'Solved'),
        ]
    )

    def __str__(self):
        return self.vehicle.vehicle_number
    