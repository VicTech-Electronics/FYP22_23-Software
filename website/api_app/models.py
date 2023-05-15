from rest_framework.serializers import ModelSerializer
from main_app.models import Request

# Create your models here.
class RequestSerializer(ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'