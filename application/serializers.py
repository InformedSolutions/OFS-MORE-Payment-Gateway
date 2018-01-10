from application.models import OrderRequest, Key
from rest_framework import serializers


# Serializers read request data and validate it against the respective model
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderRequest
        fields = ('amount', 'card_holder_name', 'card_number', 'cvc', 'expiry_month', 'expiry_year', 'currency_code',
                  'customer_order_code', 'order_description')


class ApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Key
        fields = ('api_key',)
