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

    def test_order_request(self):
        # test successful order- this is the same as the swagger docs
        self.client = Client()
        header = {'content-type': 'application/json', 'Authorization': 'T_S_affb6e01-fd4e-42e4-bed6-5cc45e38ed57'}
        input = {
            "amount": 50000,
            "card_holder_name": "Mr Example Cardholder",
            "card_number": 5454545454545454,
            "cvc": 353,
            "expiry_month": 6,
            "expiry_year": 2018,
            "currency_code": "GBP",
            "customer_order_code": "OFS-MORE-162738",
            "order_description": "Childminder Registration Fee"
        }
        response = self.client.post('/payment-gateway/api/v1/payments/card/', json.dumps(input), 'application/json',
                                    header=header)
        self.assertEqual(response.status_code, 201)

    def test_worldpay_error(self):
        # Test worldpay error
        self.client = Client()
        header = {'content-type': 'application/json', 'Authorization': 'T_S_affb6e01-fd4e-42e4-bed6-5cc45e38ed57'}
        input = {
            "amount": 50000,
            "card_holder_name": "Mr Example Cardholder",
            "card_number": 5454545454545454,
            "cvc": 77353,
            "expiry_month": 6,
            "expiry_year": 2018,
            "currency_code": "GBP",
            "customer_order_code": "OFS-MORE-162738",
            "order_description": "Childminder Registration Fee"
        }
        response = self.client.post('/payment-gateway/api/v1/payments/card/', json.dumps(input), 'application/json',
                                    header=header)
        self.assertEqual(response.status_code, 400)

    def test_serializer_error(self):
        # Test serializer error, missing field
        self.client = Client()
        header = {'content-type': 'application/json', 'Authorization': 'T_S_affb6e01-fd4e-42e4-bed6-5cc45e38ed57'}
        input = {
            "card_holder_name": "Mr Example Cardholder",
            "card_number": 5454545454545454,
            "cvc": 353,
            "expiry_month": 6,
            "expiry_year": 2018,
            "currency_code": "GBP",
            "customer_order_code": "OFS-MORE-162738",
            "order_description": "Childminder Registration Fee"
        }
        response = self.client.post('/payment-gateway/api/v1/payments/card/', json.dumps(input), 'application/json',
                                    header=header)
        self.assertEqual(response.status_code, 400)

    def test_set_api_key(self):
        # Test updating the APi Key
        self.client = Client()
        header = {'content-type': 'application/json'}
        input = {
            "api_key": "T_S_affb6e01-fd4e-42e4-bed6-5cc45e38ed57"
        }
        response = self.client.put('/payment-gateway/api/v1/payments/api-key/', json.dumps(input), 'application/json',
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

    def test_set_api_key(self):
        # Test updating the APi Key
        self.client = Client()
        header = {'content-type': 'application/json'}
        input = {
            "api_key": "dev_api-7c51af0f-8720-4315-9d67-b4f94d7531e0-df9b0c2e-6d50-4102-ae62-9a24cde656cc"
        }
        response = self.client.put('/payment-gateway/api/v1/payments/api-key/', json.dumps(input),
                                   'application/json', header=header)
        self.assertEqual(response.status_code, 200)

    def test_bad_set_api_key(self):
        # Update the API key, with an empty string
        self.client = Client()
        header = {'content-type': 'application/json'}
        input = {
            "api_key": ""
        }
        response = self.client.put('/payment-gateway/api/v1/payments/api-key/', json.dumps(input),
                                   'application/json', header=header)
        # This test is meant to fail
        self.assertEqual(response.status_code, 400)
