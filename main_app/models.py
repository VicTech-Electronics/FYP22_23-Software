from django.db import models

# Create your models here.
class PlateNumber(models.Model):
    number = models.CharField(max_length=20)

    def __str__(self):
        return self.number
    

class CardNumber(models.Model):
    number = models.CharField(max_length=20)

    def __str__(self):
        return self.number