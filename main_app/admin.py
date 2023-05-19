from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Nurse)
admin.site.register(Device)
admin.site.register(Request)
admin.site.register(Attendence)
admin.site.register(TimeTable)
