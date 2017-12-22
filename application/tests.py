import json
import sys
import unittest

from django.test import Client
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class TestApi(unittest.TestCase):
    def test_api(self):
        self.client = Client()
        header = {'content-type': 'application/json', 'Authorization':'T_S_affb6e01-fd4e-42e4-bed6-5cc45e38ed57'}
        input = {
  "amount": 50000,
  "cardHolderName": "Mr Example Cardholder",
  "cardNumber": 5454545454545454,
  "cvc": 35,
  "expiryMonth": 6,
  "expiryYear": 2017,
  "currencyCode": "GBP",
  "customerOrderCode": "OFS-MORE-162738",
  "orderDescription": "Childminder Registration Fee"
}
        response = self.client.post('/payment-gateway/api/v1/payments/card/' , json.dumps(input), 'application/json', header=header)
        self.assertEqual(response.status_code, 200)