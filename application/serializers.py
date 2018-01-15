"""
OFS-MORE-CCN3: Apply to be a Childminder Beta
-- serializers.py --

@author: Informed Solutions
"""


from application.models import CardPaymentRequest, PaypalPaymentRequest, ApiKey
from rest_framework import serializers


class CardPaymentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardPaymentRequest
        fields = ('amount', 'card_holder_name', 'card_number', 'cvc', 'expiry_month', 'expiry_year', 'currency_code',
                  'customer_order_code', 'order_description',)


class PaypalPaymentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaypalPaymentRequest
        fields = ('amount', 'shopper_country_code', 'currency_code', 'customer_order_code', 'success_url', 'pending_url', 'failure_url',
                  'cancellation_url', 'order_description',)


class ApiKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiKey
        fields = ('api_key',)
