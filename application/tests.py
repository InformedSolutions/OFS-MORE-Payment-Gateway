import json
import requests
import sys
import unittest
from django.conf import settings
from django.test import Client
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class TestApi(unittest.TestCase):

    def test_orderRequest(self):
        # test successful order- this is the same as the swagger docs
        self.client = Client()
        header = {'content-type': 'application/json', 'Authorization': 'T_S_affb6e01-fd4e-42e4-bed6-5cc45e38ed57'}
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
        response = self.client.post('/payment-gateway/api/v1/payments/card/', json.dumps(input), 'application/json',
                                    header=header)
        self.assertEqual(response.status_code, 201)

    def test_worldpayError(self):
        # Test worldpay error
        self.client = Client()
        header = {'content-type': 'application/json', 'Authorization': 'T_S_affb6e01-fd4e-42e4-bed6-5cc45e38ed57'}
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
        response = self.client.post('/payment-gateway/api/v1/payments/card/', json.dumps(input), 'application/json',
                                    header=header)
        self.assertEqual(response.status_code, 400)

    def test_serializerError(self):
        # Test serializer error, missing field
        self.client = Client()
        header = {'content-type': 'application/json', 'Authorization': 'T_S_affb6e01-fd4e-42e4-bed6-5cc45e38ed57'}
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
        response = self.client.post('/payment-gateway/api/v1/payments/card/', json.dumps(input), 'application/json',
                                    header=header)
        self.assertEqual(response.status_code, 400)

    def test_setApiKey(self):
        # Test updating the APi Key
        self.client = Client()
        header = {'content-type': 'application/json'}
        input = {
            "apiKey": "T_S_affb6e01-fd4e-42e4-bed6-5cc45e38ed57"
        }
        response = self.client.put('/payment-gateway/api/v1/payments/api-key/', json.dumps(input), 'application/json',
                                   header=header)
        self.assertEqual(response.status_code, 200)

    def test_getOrderInfo(self):
        # test get order info- note you will have to update the id if you change the api key
        id = "161dbaa0-a025-42fb-9e0d-c4597ac1c6b3"
        header = {'content-type': 'application/json', 'Authorization': 'T_S_affb6e01-fd4e-42e4-bed6-5cc45e38ed57'}
        response = requests.get("https://api.worldpay.com/v1/orders/" + id + '?testMode=100', headers=header)
        self.assertEqual(response.status_code, 200)

    def test_getOrderInfoError(self):
        # test bad request
        id = "161dbaa0-a025-42fb-9e0d-c4597ac1c6b1"
        header = {'content-type': 'application/json', 'Authorization': 'T_S_affb6e01-fd4e-42e4-bed6-5cc45e38ed57'}
        response = requests.get("https://api.worldpay.com/v1/orders/" + id + '?testMode=100', headers=header)
        self.assertEqual(response.status_code, 404)
