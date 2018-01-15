import re
from application.views import place_order, paypal_order_request, change_api_key, get_payment
from django.conf.urls import url

from django.conf import settings

urlpatterns = [
    # See swagger documentation, there are three RESTful URL's
    url(r'^api/v1/payments/card/$', place_order),
    url(r'^api/v1/payments/paypal/$', paypal_order_request),
    url(r'^api/v1/payments/api-key/$', change_api_key),
    # Below regex pulls out id to be used in request as id, see gat_payment parameter
    url(r'^api/v1/payments/(?P<id>[\w-]+)/$', get_payment),
]

if settings.URL_PREFIX:
    prefixed_url_pattern = []
    for pat in urlpatterns:
        pat.regex = re.compile(r"^%s/%s" % (settings.URL_PREFIX[1:], pat.regex.pattern[1:]))
        prefixed_url_pattern.append(pat)
    urlpatterns = prefixed_url_pattern
