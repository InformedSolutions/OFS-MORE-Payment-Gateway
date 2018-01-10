from django.contrib.postgres.fields.jsonb import JSONField
from django.db import models


class OrderRequest(models.Model):
    #Order Data validation rules
    amount = models.DecimalField(max_digits=10, decimal_places=0, blank=False)
    card_holder_name = models.CharField(max_length=100, blank=False)
    card_number = models.DecimalField(max_digits=18, decimal_places=0, blank=False)
    cvc = models.PositiveSmallIntegerField(blank=False)
    expiry_month = models.PositiveSmallIntegerField(blank=False)
    expiry_year = models.PositiveSmallIntegerField(blank=False)
    currency_code = models.CharField(max_length=4, blank=False)
    customer_order_code = models.CharField(max_length=100, blank=False)
    order_description = models.CharField(max_length=100, blank=False)


class Key(models.Model):
    #API key validation rules
    #Name is a placeholder as there needs to be more than one entry to execute without error
    api_key = models.CharField(max_length=100, blank=False)
    