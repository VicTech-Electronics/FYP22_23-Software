from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    meter_number = models.CharField(max_length=100)
    amount = models.FloatField(default=0.0)
    units = models.FloatField(default=0.0)

    def __str__(self):
        return self.user.username

class Notification(models.Model):
    customer = models.ForeignKey(Customer, null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    detail = models.CharField(max_length=500)
    date_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer.user.username
    
class PaymentHistory(models.Model):
    customer = models.ForeignKey(Customer, null=False, on_delete=models.CASCADE)
    amount = models.FloatField(default=0.0)
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)

    def __str__(self):
        return self.customer.user.username