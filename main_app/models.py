from pyexpat import model
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=10)
    amount = models.FloatField(default=0.0)

    def __str__(self):
        return self.user.username

class Transaction(models.Model):
    customer = models.ForeignKey(Customer, null=False, on_delete=models.CASCADE)
    details = models.CharField(
        max_length=10,
        choices=[
            ('urination', 'Urination'),
            ('defecation', 'Defecation'),
            ('shower', 'Shower')
        ]
    )
    amount = models.FloatField()
    date_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer.user.username

class Expenses(models.Model):
    details = models.TextField()
    amount = models.FloatField()
    date_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.details