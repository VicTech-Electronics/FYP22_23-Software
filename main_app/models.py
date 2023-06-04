from django.db import models

# Create your models here.
class BreakerState(models.Model):
    state = models.CharField(max_length=10)

    def __str__(self):
        return self.state