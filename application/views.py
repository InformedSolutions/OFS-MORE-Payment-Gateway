"""
OFS-MORE-CCN3: Apply to be a Childminder Beta
-- views.py --

@author: Informed Solutions
"""

import json
import logging
import requests
import traceback

from django.conf import settings
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from application.serializers import CardPaymentRequestSerializer, PaypalPaymentRequestSerializer, ApiKeySerializer
from application.utilities import Utilities

# initiate logging
log = logging.getLogger('django.server')

# initiate API key
api_key = settings.WORLDPAY_API_KEY


@api_view(['GET'])
def get_payment(request, payment_id):
    """
    Function for retrieving a previously placed order
    :param request: a json request issued over http protocols, this must exist (like a class' self method)
    :param payment_id: the (WorldPay) identifier of the previously issued payment
    :return: a json representation of a previously lodged payment
    """
    try:
        # Remove testMode when you want to go live
        header = {'content-type': 'application/json', 'Authorization': api_key}
        response = requests.get("https://api.worldpay.com/v1/orders/" + payment_id + '?testMode=100', headers=header)
        print(response)
        returned_json = json.loads(response.text)

        # Pruning fields we do not need
        if response.status_code == 200:
            del returned_json['token']
            del returned_json['environment']

        try:
            status_code = returned_json['httpStatusCode']
            return JsonResponse({"message": returned_json}, status=status_code)
        except KeyError:
            return JsonResponse({"message": returned_json}, status=200)
    except Exception as ex:
        exception_data = traceback.format_exc().splitlines()
        exception_array = [exception_data[-3:]]
        log.error(exception_array)
        return JsonResponse(ex.__dict__, status=500)


@api_view(['POST'])
def make_card_payment(request):
    """
    Function for making a new card payment via the WorldPay payment processing platform
    :param request: a json object inclusive of details for a card payment to be taken
    :return: a success or failure response from the WorldPay payment processing platform
    """
    mapped_json_request = Utilities.convert_json_to_python_object(request.data)
    try:
        serializer = CardPaymentRequestSerializer(data=mapped_json_request)
        if serializer.is_valid():
            return __create_worldpay_card_order_request(serializer.data)
        err = __format_error(serializer.errors)
        log.error("Django serialization error: " + err[0] + err[1])
        return JsonResponse({"message": err[0] + err[1], "error": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        exception_data = traceback.format_exc().splitlines()
        exception_array = [exception_data[-3:]]
        log.error(exception_array)
        return JsonResponse(ex.__dict__, status=500)


@api_view(['POST'])
def make_paypal_payment(request):
    """
    Function for making a new Paypal payment via the WorldPay payment processing platform
    :param request: a json object inclusive of details for a paypal payment to be taken
    :return: a response inclusive of any URLs that a user should be redirected to (i.e. WorldPay paypal UIs) for making
    a Paypal payment
    """
    mapped_json_request = Utilities.convert_json_to_python_object(request.data)
    try:
        serializer = PaypalPaymentRequestSerializer(data=mapped_json_request)
        if serializer.is_valid():
            return __create_worldpay_paypal_order_request(serializer.data)
        err = __format_error(serializer.errors)
        log.error("Django serialization error: " + err[0] + err[1])
        return JsonResponse({"message": err[0] + err[1], "error": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        exception_data = traceback.format_exc().splitlines()
        exception_array = [exception_data[-3:]]
        log.error(exception_array)
        return JsonResponse(ex.__dict__, status=500)


@api_view(['PUT'])
def change_api_key(request):
    """
    Function for updating the Worldpay API key used by the payment gateway API
    :param request: a json request object detailing the new API key to be used
    :return: a success or failure indicator as to whether the Worldpay API key has been updated
    """
    # Change API Key, this is the exact same as the Notify version
    try:
        mapped_json_request = Utilities.convert_json_to_python_object(request.data)
        serializer = ApiKeySerializer(data=mapped_json_request)
        if serializer.is_valid():
            # API key set
            global api_key
            api_key = mapped_json_request['api_key']
            return JsonResponse({"message": "Api key successfully updated"}, status=200)
        err = __format_error(serializer.errors)
        log.error("Django serialization error: " + err[0] + err[1])
        return JsonResponse({"message": err[0] + err[1], "error": "Bad Request", }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        exception_data = traceback.format_exc().splitlines()
        exception_array = [exception_data[-3:]]
        log.error(exception_array)
        return JsonResponse(ex.__dict__, status=500)


def __create_worldpay_card_order_request(card_payment_request):
    """
    Helper method for creating a request object that can be consumed by the Worldpay API to take a card payment
    :param card_payment_request: a request object sent to the payment gateway API containing information for taking a
    card payment via Worldpay
    :return: a json request that can be consumed by the Worldpay API for making a card payment
    """
    payload = {
        "paymentMethod": {
            "name": card_payment_request['card_holder_name'],
            "expiryMonth": card_payment_request['expiry_month'],
            "expiryYear": card_payment_request['expiry_year'],
            "cardNumber": card_payment_request['card_number'],
            "type": "Card",
            "cvc": card_payment_request['cvc']
        },
        "amount": card_payment_request['amount'],
        "currencyCode": card_payment_request['currency_code'],
        "orderDescription": card_payment_request['order_description'],
        "customerOrderCode": card_payment_request['customer_order_code']
    }

    headers = {"content-type": "application/json", "Authorization": api_key}
    response = requests.post("https://api.worldpay.com/v1/orders", data=json.dumps(payload), headers=headers)

    if response.status_code == 200:
        return JsonResponse(json.loads(response.text), status=201)
    else:
        return JsonResponse(json.loads(response.text), status=response.status_code)


def __create_worldpay_paypal_order_request(paypal_payment_request):
    """
    Helper method for creating a request object that can be consumed by the Worldpay API to take a paypal payment
    :param paypal_payment_request: a request object sent to the payment gateway API containing information for taking a
    Paypal payment via Worldpay
    :return: a json request that can be consumed by the Worldpay API for making a Paypal payment
    """
    payload = {
        "paymentMethod": {
            "type": "APM",
            "apmName": "paypal",
            "shopperCountryCode": paypal_payment_request["shopper_country_code"]
        },
        "amount": paypal_payment_request["amount"],
        "currencyCode": paypal_payment_request["currency_code"],
        "orderDescription": paypal_payment_request["order_description"],
        "customerOrderCode": paypal_payment_request["customer_order_code"],
        "successUrl": paypal_payment_request["success_url"],
        "pendingUrl": paypal_payment_request["pending_url"],
        "failureUrl": paypal_payment_request["failure_url"],
        "cancelUrl": paypal_payment_request["cancellation_url"],
    }

    headers = {"content-type": "application/json", "Authorization": api_key}
    response = requests.post("https://api.worldpay.com/v1/orders", data=json.dumps(payload), headers=headers)

    if response.status_code == 200:
        return JsonResponse(json.loads(response.text), status=201)
    else:
        return JsonResponse(json.loads(response.text), status=response.status_code)


def __format_error(ex):
    """
    Helper function for formatting errors encountered when serializing Django requests
    :param ex: the exception encountered by a Django serializer
    :return: a json friendly response detailing an exception incurred whilst serializing a request
    """
    # Formatting default Django error messages
    err = str(ex).split(":", 1)
    err[0] = err[0].strip('{')
    err[1] = err[1].strip('}')
    err[1] = err[1].replace('[', '')
    err[1] = err[1].replace(']', '')
    return err
