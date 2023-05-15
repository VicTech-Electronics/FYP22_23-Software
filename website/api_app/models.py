from rest_framework.serializers import ModelSerializer
from classifier_app.models import AccidentIndicator

# Create your models here.
class IndicatorSerializer(ModelSerializer):
    class Meta:
        model = AccidentIndicator
        fields = '__all__'
