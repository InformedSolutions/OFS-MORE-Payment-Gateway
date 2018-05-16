"""
OFS-MORE-CCN3: Apply to be a Childminder Beta
-- serializers.py --

@author: Informed Solutions
"""

from rest_framework import serializers

from .models import CardPaymentRequest, ApiKey


class CardPaymentRequestSerializer(serializers.ModelSerializer):
    """
    Defines fields names and order for use in model serializers in models.py
    """
    class Meta:
        model = CardPaymentRequest
        fields = ('amount', 'card_holder_name', 'card_number', 'cvc', 'expiry_month', 'expiry_year', 'currency_code',
                  'customer_order_code', 'order_description',)


class ApiKeySerializer(serializers.ModelSerializer):
    """
    Defines fields names and order for use in model serializers in models.py
    """
    class Meta:
        model = ApiKey
        # Note this is still kept in tuple format whilst only containing one element, please keep this in a tuple
        fields = ('api_key',)
