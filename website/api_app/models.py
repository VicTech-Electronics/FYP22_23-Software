from dataclasses import field
from pyexpat import model
from rest_framework.serializers import ModelSerializer
from main_app.models import Report, Call, Message

# Create your models here.
class ReportSerializer(ModelSerializer):
    class Meta:
        model = Report
        fields = ['device', 'title', 'content', 'latitude', 'longitude']
    
class CallSerializer(ModelSerializer):
    class Meta:
        model = Call
        fields = ['device', 'phone', 'response']

class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = ['device', 'phone', 'content']
