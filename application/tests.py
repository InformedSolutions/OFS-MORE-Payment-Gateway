import json
import sys
import unittest
from django.conf import settings
from django.test import Client
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class TestApi(unittest.TestCase):
    
    def test_orderRequest(self):
        self.client = Client()
        header = {'content-type': 'application/json', 'Authorization':'T_S_affb6e01-fd4e-42e4-bed6-5cc45e38ed57'}
        input = {
  "amount": 50000,
  "cardHolderName": "Mr Example Cardholder",
  "cardNumber": 5454545454545454,
  "cvc": 353,
  "expiryMonth": 6,
  "expiryYear": 2018,
  "currencyCode": "GBP",
  "customerOrderCode": "OFS-MORE-162738",
  "orderDescription": "Childminder Registration Fee"
}
        response = self.client.post('/payment-gateway/api/v1/payments/card/' , json.dumps(input), 'application/json', header=header)
        self.assertEqual(response.status_code, 200)
    def test_badOrderRequest(self):
        #worldpay error
        self.client = Client()
        header = {'content-type': 'application/json', 'Authorization':'T_S_affb6e01-fd4e-42e4-bed6-5cc45e38ed57'}
        input = {
      "amount": -50000,
      "cardHolderName": "Mr Example Cardholder",
      "cardNumber": 5454545454545454,
      "cvc": 353,
      "expiryMonth": 6,
      "expiryYear": 2018,
      "currencyCode": "GBP",
      "customerOrderCode": "OFS-MORE-162738",
      "orderDescription": "Childminder Registration Fee"
        }
        response = self.client.post('/payment-gateway/api/v1/payments/card/' , json.dumps(input), 'application/json', header=header)
        self.assertEqual(response.status_code, 400)
        
    def test_badOrderRequest2(self):
        #serializer error, missing field
        self.client = Client()
        header = {'content-type': 'application/json', 'Authorization':'T_S_affb6e01-fd4e-42e4-bed6-5cc45e38ed57'}
        input = {
      "cardHolderName": "Mr Example Cardholder",
      "cardNumber": 5454545454545454,
      "cvc": 353,
      "expiryMonth": 6,
      "expiryYear": 2018,
      "currencyCode": "GBP",
      "customerOrderCode": "OFS-MORE-162738",
      "orderDescription": "Childminder Registration Fee"
        }
        response = self.client.post('/payment-gateway/api/v1/payments/card/' , json.dumps(input), 'application/json', header=header)
        self.assertEqual(response.status_code, 400)
    