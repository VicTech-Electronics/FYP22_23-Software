from django.db import models

class Driver(models.Model):
    username = models.CharField(max_length=200)
    vehicle_number = models.CharField(max_length=10)
    email = models.EmailField()
    contact = models.CharField(max_length=15)

    def __str__(self):
        return self.username


class Case(models.Model):
    driver = models.ForeignKey(Driver, null=False, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)
    payment = models.BooleanField(default=False)

    def __str__(self):
        return self.driver.username + ' > ' + self.driver.vehicle_number
