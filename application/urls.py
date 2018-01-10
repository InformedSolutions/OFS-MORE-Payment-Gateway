from application.views import place_order, get_payment, change_api_key
from django.conf.urls import url

urlpatterns = [
    # See swagger documentation, there are three RESTful URL's
    url(r'^payment-gateway/api/v1/payments/(?P<id>[\w-]+)/$', get_payment),
]
