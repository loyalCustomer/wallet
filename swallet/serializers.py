from rest_framework import serializers

from .models import SimpleWallet, Transaction



class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimpleWallet
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'    
        