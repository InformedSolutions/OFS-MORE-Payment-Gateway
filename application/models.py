from django.contrib.postgres.fields.jsonb import JSONField
from django.db import models


class OrderRequest(models.Model):
    #Order Data validation rules
    amount = models.DecimalField(max_digits=10, decimal_places=0, blank=False)
    cardHolderName = models.CharField(max_length=100, blank=False)
    cardNumber = models.DecimalField(max_digits=18, decimal_places=0, blank=False)
    cvc = models.PositiveSmallIntegerField(blank=False)
    expiryMonth = models.PositiveSmallIntegerField(blank=False)
    expiryYear = models.PositiveSmallIntegerField(blank=False)
    currencyCode = models.CharField(max_length=4, blank=False)
    customerOrderCode = models.CharField(max_length=100, blank=False)
    orderDescription = models.CharField(max_length=100, blank=False)


class Key(models.Model):
    #API key validation rules
    #Name is a placeholder as there needs to be more than one entry to execute without error
    name = models.CharField(max_length=100, blank=True)
    apiKey = models.CharField(max_length=100, blank=False)
    