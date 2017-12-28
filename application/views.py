from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from application.serializers import OrderSerializer, APISerializer
import requests
import json
import logging
import traceback 
from rest_framework.decorators import api_view
from django.conf import settings
from rest_framework import status
from django.test import Client
from django.conf import settings

#initiate logging
log = logging.getLogger('django.server')
#initiate API key
apiKey = settings.WORLDPAY_API

@api_view(['GET'])
def get_payment(request, id):
    #This method doesn't work, URL doesn't match swagger documentation
    header = {'content-type': 'application/json','Authorization':apiKey}
    url = "https://api.worldpay.com/v1/"
    r = requests.get(url, headers=header)
    out = str(r.content)
    return JsonResponse({"Success":out},status=200)
    JsonResponse({"Error":"didn't work- put real error message"})
@api_view(['POST'])
def place_order(request):
    #This method places an order via WorldPay API- this is almost all error handling and logging
    try:
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            return order_request(serializer.data)
        err = formatError(serializer.errors)
        log.error("Django serialization error: " +err[0] + err[1])
        return JsonResponse({"message": err[0] + err[1], "error":"Bad Request"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        exceptiondata = traceback.format_exc().splitlines()
        exceptionarray = [exceptiondata[-3:]]
        log.error(exceptionarray)
        return JsonResponse(ex.__dict__, status=500)
@api_view(['PUT'])
def change_api_key(request):
    #Change API Key, this is the exact same as the Notify version
    try:
        serializer = APISerializer(data=request.data)
        if serializer.is_valid():
            #API key set
            global apiKey
            apiKey = request.data['apiKey']
            return JsonResponse({"message":"Api key successfully updated"}, status=200)
        err = formatError(serializer.errors)
        log.error("Django serialization error: " +err[0] + err[1])
        return JsonResponse({"message": err[0] + err[1], "error":"Bad Request",}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        exceptiondata = traceback.format_exc().splitlines()
        exceptionarray = [exceptiondata[-3:]]
        log.error(exceptionarray)
        return JsonResponse(ex.__dict__, status=500)   
def order_request(data):
    #this is just setting the post request for creating the worldpay order
    payload = {
    "paymentMethod": {
        "name": data['cardHolderName'],
        "expiryMonth": data['expiryMonth'],
        "expiryYear": data['expiryYear'],
        "cardNumber": data['cardNumber'],
        "type": "Card",
        "cvc": data['cvc']
    },
    "amount": data['amount'],
    "currencyCode": data['currencyCode'],
    "orderDescription": data['orderDescription'],
    "customerOrderCode": data['customerOrderCode']
    }
    headers = {"content-type": "application/json", "Authorization":apiKey}
    r = requests.post("https://api.worldpay.com/v1/orders", data=json.dumps(payload), headers=headers)
    return JsonResponse(json.loads(r.text), status=r.status_code)

def formatError(ex):
    #Formatting default Django error messages
    err = str(ex).split(":",1)
    err[0] = err[0].strip('{')
    err[1] = err[1].strip('}')
    err[1] = err[1].replace('[','')
    err[1] = err[1].replace(']','')
    return err