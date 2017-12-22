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



log = logging.getLogger('django.server')

# Create your views here.
@api_view(['GET'])
def get_payment(request, id):
    #print(id)
    print(request.path_info)
    header = {'content-type': 'application/json','Authorization':'T_S_affb6e01-fd4e-42e4-bed6-5cc45e38ed57'}
    url = "https://api.worldpay.com/v1/"
    #url+=id
    r = requests.get(url, headers=header)
    out = str(r.content)
    return JsonResponse({"Success":out},status=200)
@api_view(['POST'])
def place_order(request):
    try:
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            #call method to send email
            return order_request(serializer.data)
        err = formatError(serializer.errors)
        log.error("Django serialization error: " +err[0] + err[1])
        return JsonResponse({"message": err[0] + err[1], "error":"Bad Request"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        exceptiondata = traceback.format_exc().splitlines()
        exceptionarray = [exceptiondata[-3:]]
        log.error(exceptionarray)
        return JsonResponse(ex.__dict__, status=500)
def change_api_key(request):
    print("temp")    
def order_request(data):
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
    headers = {"content-type": "application/json", "Authorization":"T_S_affb6e01-fd4e-42e4-bed6-5cc45e38ed57"}


    r = requests.post("https://api.worldpay.com/v1/orders", data=json.dumps(payload), headers=headers)
    print(r.text)
    
    return JsonResponse({"messag":"working?"}, status=200)
def formatError(ex):
    #Formatting default Django error messages
    err = str(ex).split(":",1)
    err[0] = err[0].strip('{')
    err[1] = err[1].strip('}')
    err[1] = err[1].replace('[','')
    err[1] = err[1].replace(']','')
    return err