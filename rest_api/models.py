from rest_framework import serializers
from main.models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['customer', 'amount', 'details']