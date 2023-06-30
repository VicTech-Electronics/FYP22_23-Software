from tkinter import CASCADE
from turtle import title
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Device(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    device_id = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username + ' (' + self.device_id + ')'

class Report(models.Model):
    device = models.ForeignKey(Device, null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=500)
    date_time = models.DateTimeField(auto_now=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.title

class Call(models.Model):
    device = models.ForeignKey(Device, null=False, on_delete=models.CASCADE)
    phone = models.IntegerField()
    date_time = models.DateTimeField(auto_now=True)
    response = models.BooleanField(
        choices=[
            (True, 'Accepted'),
            (False, 'Missed'),
        ]
    )

    def __str__(self):
        return str(self.phone)

class Message(models.Model):
    device = models.ForeignKey(Device, null=False, on_delete=models.CASCADE)
    phone = models.IntegerField()
    content = models.TextField()
    date_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.phone)