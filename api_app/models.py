from rest_framework.serializers import ModelSerializer
from main_app.models import Transaction

# Create your models here.
class TransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['customer', 'details', 'amount']

