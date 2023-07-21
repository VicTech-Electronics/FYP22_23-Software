from django.contrib import admin
from .models import PlateNumber, CardNumber

# Register your models here.
admin.site.register(PlateNumber)
admin.site.register(CardNumber)