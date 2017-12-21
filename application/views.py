from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
import json



# Create your views here.
def get_payment(request):
    id =  request.GET.get()
    header = {'content-type': 'application/json','Authorization':'T_S_affb6e01-fd4e-42e4-bed6-5cc45e38ed57'}
    url = "https://api.worldpay.com/v1/"
    url+=id
    r = requests.get(url, headers=header)
    out = str(r.content)
    return JsonResponse({"Success":out},status=200)
def place_order(request):
    try:
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            #call method to send email
            return order_request(serializer.data)
        err = formatError(serializer.errors)
        log.error("Django serialization error: " +err[0] + err[1])
        return JsonResponse({"message": err[0] + err[1], "error":"Bad Request"}, status=status.HTTP_400_BAD_REQUEST)
    except HTTPError as ex:
        exceptiondata = traceback.format_exc().splitlines()
        exceptionarray = [exceptiondata[-3:]]
        log.error(exceptionarray)
        return JsonResponse(ex.message, status=ex.status_code, safe=False)
    except Exception as ex:
        exceptiondata = traceback.format_exc().splitlines()
        exceptionarray = [exceptiondata[-3:]]
        log.error(exceptionarray)
        return JsonResponse(ex.__dict__, status=500)
def change_api_key(request):
    print("temp")    
def order_request(data):
    print("temp")
