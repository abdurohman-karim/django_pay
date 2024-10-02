from rest_framework import serializers
from .models import Transaction

class TransactionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['amount', 'description']

class TransactionConfirmSerializer(serializers.Serializer):
    transaction_id = serializers.IntegerField()
    otp = serializers.CharField(max_length=6)

class TransactionCancelSerializer(serializers.Serializer):
    transaction_id = serializers.IntegerField()

class TransactionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'description', 'status', 'created_at']
