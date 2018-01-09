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
apiKey = settings.WORLDPAY_API_KEY

@api_view(['GET','POST','PUT'])
def get_payment(request, id):
    try:
        if "card" in id:
            return place_order(request)
        elif "api-key" in id:

            return change_api_key(request)
        else:
        #Remove testMode when you want to go live
            header = {'content-type': 'application/json','Authorization':apiKey}
            response = requests.get("https://api.worldpay.com/v1/orders/" +id +'?testMode=100',  headers=header)
            out = json.loads(response.text)
            try:
                status= out['httpStatusCode']
                return JsonResponse({"message":out},status=status)
            except Exception as ex:
                return JsonResponse({"message":out},status=200)
    except Exception as ex:
        exceptiondata = traceback.format_exc().splitlines()
        exceptionarray = [exceptiondata[-3:]]
        log.error(exceptionarray)
        return JsonResponse(ex.__dict__, status=500)
    
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
    response = requests.post("https://api.worldpay.com/v1/orders", data=json.dumps(payload), headers=headers)
    if response.status_code==200:
        return JsonResponse(json.loads(response.text), status=201)
    else:  
        return JsonResponse(json.loads(response.text), status=response.status_code)

def formatError(ex):
    #Formatting default Django error messages
    err = str(ex).split(":",1)
    err[0] = err[0].strip('{')
    err[1] = err[1].strip('}')
    err[1] = err[1].replace('[','')
    err[1] = err[1].replace(']','')
    return err