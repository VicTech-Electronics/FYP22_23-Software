from rest_framework.serializers import ModelSerializer
from main_app.models import BreakerState

class BreakerStateSerializer(ModelSerializer):
    class Meta:
        model = BreakerState
        fields = '__all__'