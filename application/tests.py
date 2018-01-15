"""
OFS-MORE-CCN3: Apply to be a Childminder Beta
-- tests.py --

@author: Informed Solutions
"""

import json
import unittest

import requests
from django.conf import settings
from django.test import Client


class TestApi(unittest.TestCase):

    def test_order_request(self):
        # test successful order- this is the same as the swagger docs
        self.client = Client()
        header = {'content-type': 'application/json', 'Authorization': 'T_S_affb6e01-fd4e-42e4-bed6-5cc45e38ed57'}
        request = {
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
        response = self.client.post(settings.URL_PREFIX + '/api/v1/payments/card/', json.dumps(request), 'application/json',
                                    header=header)
        self.assertEqual(response.status_code, 201)

    def test_worldpay_error(self):
        # Test worldpay error
        self.client = Client()
        header = {'content-type': 'application/json', 'Authorization': 'T_S_affb6e01-fd4e-42e4-bed6-5cc45e38ed57'}
        request = {
            "amount": 50000,
            "cardHolderName": "Mr Example Cardholder",
            "cardNumber": 5454545454545454,
            "cvc": 77353,
            "expiryMonth": 6,
            "expiryYear": 2018,
            "currencyCode": "GBP",
            "customerOrderCode": "OFS-MORE-162738",
            "orderDescription": "Childminder Registration Fee"
        }
        response = self.client.post(settings.URL_PREFIX + '/api/v1/payments/card/', json.dumps(request), 'application/json',
                                    header=header)
        self.assertEqual(response.status_code, 400)

    def test_serializer_error(self):
        # Test serializer error, missing field
        self.client = Client()
        header = {'content-type': 'application/json', 'Authorization': 'T_S_affb6e01-fd4e-42e4-bed6-5cc45e38ed57'}
        request = {
            "cardHolderName": "Mr Example Cardholder",
            "cardNumber": 5454545454545454,
            "cvc": 353,
            "expiryMonth": 6,
            "expiryYear": 2018,
            "currencyCode": "GBP",
            "customerOrderCode": "OFS-MORE-162738",
            "orderDescription": "Childminder Registration Fee"
        }
        response = self.client.post(settings.URL_PREFIX + '/api/v1/payments/card/', json.dumps(request), 'application/json',
                                    header=header)
        self.assertEqual(response.status_code, 400)

    def test_set_apiKey(self):
        # Test updating the APi Key
        self.client = Client()
        header = {'content-type': 'application/json'}
        request = {
            "apiKey": "T_S_affb6e01-fd4e-42e4-bed6-5cc45e38ed57"
        }
        response = self.client.put(settings.URL_PREFIX + '/api/v1/payments/api-key/', json.dumps(request), 'application/json',
                                   header=header)
        self.assertEqual(response.status_code, 200)

    def test_get_order_info(self):
        # test get order info- note you will have to update the id if you change the api key
        id = "161dbaa0-a025-42fb-9e0d-c4597ac1c6b3"
        header = {'content-type': 'application/json', 'Authorization': 'T_S_affb6e01-fd4e-42e4-bed6-5cc45e38ed57'}
        response = requests.get("https://api.worldpay.com/v1/orders/" + id + '?testMode=100', headers=header)
        self.assertEqual(response.status_code, 200)

    def test_get_order_info_error(self):
        # test bad request
        id = "161dbaa0-a025-42fb-9e0d-c4597ac1c6b1"
        header = {'content-type': 'application/json', 'Authorization': 'T_S_affb6e01-fd4e-42e4-bed6-5cc45e38ed57'}
        response = requests.get("https://api.worldpay.com/v1/orders/" + id + '?testMode=100', headers=header)
        self.assertEqual(response.status_code, 404)

    def test_set_apiKey(self):
        # Test updating the APi Key
        self.client = Client()
        header = {'content-type': 'application/json'}
        request = {
            "apiKey": "dev_api-7c51af0f-8720-4315-9d67-b4f94d7531e0-df9b0c2e-6d50-4102-ae62-9a24cde656cc"
        }
        response = self.client.put(settings.URL_PREFIX + '/api/v1/payments/api-key/', json.dumps(request),
                                   'application/json', header=header)
        self.assertEqual(response.status_code, 200)

    def test_bad_set_apiKey(self):
        # Update the API key, with an empty string
        self.client = Client()
        header = {'content-type': 'application/json'}
        request = {
            "apiKey": ""
        }
        response = self.client.put(settings.URL_PREFIX + '/api/v1/payments/api-key/', json.dumps(request),
                                   'application/json', header=header)
        # This test is meant to fail
        self.assertEqual(response.status_code, 400)
