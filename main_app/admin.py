from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Device)
admin.site.register(Report)
admin.site.register(Call)
admin.site.register(Message)