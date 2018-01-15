import json
import logging
import requests
import traceback
from application.serializers import OrderSerializer, ApiSerializer
from django.conf import settings
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.test import Client
from rest_framework import status
from rest_framework.decorators import api_view

# initiate logging
log = logging.getLogger('django.server')
# initiate API key
api_key = settings.WORLDPAY_API_KEY


@api_view(['GET', 'POST', 'PUT'])
def get_payment(request, id):
    try:
            # Remove testMode when you want to go live
            header = {'content-type': 'application/json', 'Authorization': api_key}
            response = requests.get("https://api.worldpay.com/v1/orders/" + id + '?testMode=100', headers=header)
            returned_json = json.loads(response.text)

            # Pruning fields we do not need
            del returned_json['token']
            del returned_json['environment']

            try:
                status = returned_json['httpStatusCode']
                return JsonResponse({"message": returned_json}, status=status)
            except Exception:
                return JsonResponse({"message": returned_json}, status=200)
    except Exception as ex:
        exception_data = traceback.format_exc().splitlines()
        exception_array = [exception_data[-3:]]
        log.error(exception_array)
        return JsonResponse(ex.__dict__, status=500)


@api_view(['POST'])
def place_order(request):
    # This method places an order via WorldPay API- this is almost all error handling and logging
    try:
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            return order_request(serializer.data)
        err = format_error(serializer.errors)
        log.error("Django serialization error: " + err[0] + err[1])
        return JsonResponse({"message": err[0] + err[1], "error": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        exception_data = traceback.format_exc().splitlines()
        exception_array = [exception_data[-3:]]
        log.error(exception_array)
        return JsonResponse(ex.__dict__, status=500)


@api_view(['PUT'])
def change_api_key(request):
    # Change API Key, this is the exact same as the Notify version
    try:
        serializer = ApiSerializer(data=request.data)
        if serializer.is_valid():
            # API key set
            global api_key
            api_key = request.data['api_key']
            return JsonResponse({"message": "Api key successfully updated"}, status=200)
        err = format_error(serializer.errors)
        log.error("Django serialization error: " + err[0] + err[1])
        return JsonResponse({"message": err[0] + err[1], "error": "Bad Request", }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        exception_data = traceback.format_exc().splitlines()
        exception_array = [exception_data[-3:]]
        log.error(exception_array)
        return JsonResponse(ex.__dict__, status=500)


def order_request(data):
    # this is just setting the post request for creating the worldpay order
    payload = {
        "paymentMethod": {
            "name": data['card_holder_name'],
            "expiryMonth": data['expiry_month'],
            "expiryYear": data['expiry_year'],
            "cardNumber": data['card_number'],
            "type": "Card",
            "cvc": data['cvc']
        },
        "amount": data['amount'],
        "currencyCode": data['currency_code'],
        "orderDescription": data['order_description'],
        "customerOrderCode": data['customer_order_code']
    }
    headers = {"content-type": "application/json", "Authorization": api_key}
    response = requests.post("https://api.worldpay.com/v1/orders", data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
        return JsonResponse(json.loads(response.text), status=201)
    else:
        return JsonResponse(json.loads(response.text), status=response.status_code)

def paypal_order_request(request):

    return True

def format_error(ex):
    # Formatting default Django error messages
    err = str(ex).split(":", 1)
    err[0] = err[0].strip('{')
    err[1] = err[1].strip('}')
    err[1] = err[1].replace('[', '')
    err[1] = err[1].replace(']', '')
    return err
