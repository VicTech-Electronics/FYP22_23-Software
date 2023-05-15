from django.db import models
from rest_framework import serializers
from user_management.models import Case

# Create your models here.
class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = '__all__'