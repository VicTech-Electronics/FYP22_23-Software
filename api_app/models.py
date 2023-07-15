from rest_framework.serializers import ModelSerializer
from main_app.models import Information

# Create your models here.
class InfoSerializer(ModelSerializer):
    class Meta:
        model = Information
        fields = ['vehicle_number', 'latitude', 'longitude',  'description']
