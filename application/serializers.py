from rest_framework import serializers
from application.models import OrderRequest, Key

#Serializers read request data and validate it against the respective model
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderRequest
        fields = ('amount', 'cardHolderName', 'cardNumber', 'cvc','expiryMonth','expiryYear','currencyCode','customerOrderCode','orderDescription')
class APISerializer(serializers.ModelSerializer):
    class Meta:
        model = Key
        fields = ('apiKey', 'name')