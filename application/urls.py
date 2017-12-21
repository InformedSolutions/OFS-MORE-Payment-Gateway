from django.conf.urls import url
from application.views import place_order, get_payment, change_api_key

urlpatterns = [
    #Send Email URL
    url(r'^payment-gateway/api/v1/payments/$', get_payment),
    url(r'^payment-gateway/api/v1/payments/card/$', place_order),
    url(r'^payment-gateway/api/v1/notifications/api-key/$', change_api_key),

]