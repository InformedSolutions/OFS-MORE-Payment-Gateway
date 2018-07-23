"""
OFS-MORE-CCN3: Apply to be a Childminder Beta
-- tests.py --

@author: Informed Solutions
"""

import json
import random
import string
import unittest

from django.conf import settings
from django.test import Client


class TestApi(unittest.TestCase):
    """
    A test class to test all methods in the payment gateway, configured to run with "manage.py tests"
    """
    def test_order_request(self):
        """
        A test for making a successful order request, as documented on the payment gateway swagger
        :return: a success or fail value to the test runner to be reported on completion (see assert on response code)
        """
        self.client = Client()
        header = {'content-type': 'application/json'}

        # Below sample card details are defined on WorldPay's sample card page, see below
        # http://support.worldpay.com/support/kb/bg/testandgolive/tgl5103.html
        request = {
            "amount": 50000,
            "cardHolderName": "AUTHORISED",
            "cardNumber": 5454545454545454,
            "cvc": 353,
            "expiryMonth": 6,
            "expiryYear": 2018,
            "currencyCode": "GBP",
            "customerOrderCode": 'OFS-MORE-TEST'.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5)),
            "orderDescription": "Childminder Registration Fee"
        }
        response = self.client.post(settings.URL_PREFIX + '/api/v1/payments/card/', json.dumps(request),
                                    'application/json', header=header)
        # Should return 201 as put request has been made
        self.assertEqual(response.status_code, 201)

    def test_worldpay_error(self):
        """
        A test for making a failed order request that fails once reaching the WorldPay API by sending an invalid cvc
        :return: a success or fail value to the test runner to be reported on completion (see assert on response code)
        """
        self.client = Client()
        header = {'content-type': 'application/json', 'Authorization': 'T_S_affb6e01-fd4e-42e4-bed6-5cc45e38ed57'}

        # Below "cvc" in request object has been made invalid, so will error when reaching worldpay
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
        response = self.client.post(settings.URL_PREFIX + '/api/v1/payments/card/', json.dumps(request),
                                    'application/json', header=header)

        # Response code for invalid JSON object (as specified above) should be 400
        self.assertEqual(response.status_code, 400)

    def test_serializer_error(self):
        """
        A test for sending an invalid JSON object to the card model serializer, specifically tere being no amount value
        in request
        :return: a success or fail value to the test runner to be reported on completion (see assert on response code)
        """
        self.client = Client()
        header = {'content-type': 'application/json', 'Authorization': 'T_S_affb6e01-fd4e-42e4-bed6-5cc45e38ed57'}
        # First value should be "amount", this does not exist so will fail on model serializer use
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
        response = self.client.post(settings.URL_PREFIX + '/api/v1/payments/card/', json.dumps(request),
                                    'application/json', header=header)

        self.assertEqual(response.status_code, 400)

    def test_set_apiKey(self):
        """
        A test for sending and processing a valid Api key
        :return: a success or fail value to the test runner to be reported on completion (see assert on response code)
        """
        self.client = Client()
        header = {'content-type': 'application/json'}
        request = {
            "apiKey": "T_S_affb6e01-fd4e-42e4-bed6-5cc45e38ed57"
        }
        response = self.client.put(settings.URL_PREFIX + '/api/v1/payments/api-key/', json.dumps(request),
                                   'application/json', header=header)

        # As this is a valid request, the response status code should be 200
        self.assertEqual(response.status_code, 200)

    def test_bad_set_apiKey(self):
        """
        A test for sending and processing an invalid (empty) API key, which should return a 400 response
        :return: a success or fail value to the test runner to be reported on completion (see assert on response code)
        """
        self.client = Client()
        header = {'content-type': 'application/json'}
        request = {
            "apiKey": ""
        }
        response = self.client.put(settings.URL_PREFIX + '/api/v1/payments/api-key/', json.dumps(request),
                                   'application/json', header=header)
        # This test is meant to fail
        self.assertEqual(response.status_code, 400)

