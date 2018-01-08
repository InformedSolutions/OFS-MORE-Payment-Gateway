from django.conf.urls import url
from application.views import place_order, get_payment, change_api_key

urlpatterns = [
    #See swagger documentation, there are three RESTful URL's
    url(r'^payment-gateway/api/v1/payments/(?P<id>[\w-]+)/$', get_payment),
    #url(r'^payment-gateway/api/v1/payments/card/$', place_order),
    #url(r'^payment-gateway/api/v1/payments/api-key/$', change_api_key),
]