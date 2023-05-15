from rest_framework.serializers import ModelSerializer
from main_app.models import Informations

# Create your models here.
class InfoSerializer(ModelSerializer):
    class Meta:
        model = Informations
        fields = ['vehicle_number', 'latitude', 'longitude',  'description']
