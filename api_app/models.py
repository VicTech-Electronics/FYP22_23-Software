from rest_framework.serializers import ModelSerializer
from main_app.models import Notification

# Create your models here.
class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = ['customer', 'title', 'detail']