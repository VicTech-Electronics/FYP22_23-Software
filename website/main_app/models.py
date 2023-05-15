from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Nurse(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    contacts = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username


class Device(models.Model):
    device_id = models.CharField(max_length=100)
    ward_name = models.CharField(max_length=100)
    bed_number = models.PositiveIntegerField()

    def __str__(self):
        return self.device_id


class Request(models.Model):
    device = models.ForeignKey(Device, null=False, on_delete=models.CASCADE)
    request_time = models.DateTimeField(auto_now=True)
    response_time = models.DateTimeField(auto_now_add=True)

    def responded(self):
        return self.request_time == self.response_time

    def __str__(self):
        return self.device.device_id


class Attendence(models.Model):
    nurse = models.ForeignKey(Nurse, null=False, on_delete=models.CASCADE)
    time_in = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nurse.user.username



class WeekDay(models.Model):
    day = models.CharField(max_length=50)

    def __str__(self):
        return self.day
    


class TimeTable(models.Model):
    day = models.ForeignKey(WeekDay, null=True, on_delete=models.SET_NULL)
    nurse = models.ManyToManyField(Nurse)
    
    def __str__(self):
        return self.day.day
