"""
OFS-MORE-CCN3: Apply to be a Childminder Beta
-- urls.py --

@author: Informed Solutions
"""

import re

from django.conf.urls import url, include
from django.conf import settings

from application.views import make_card_payment, make_paypal_payment, change_api_key, get_payment


urlpatterns = [
    # See swagger documentation, there are three RESTful URL's
    url(r'^api/v1/payments/card/$', make_card_payment),
    url(r'^api/v1/payments/paypal/$', make_paypal_payment),
    url(r'^api/v1/payments/api-key/$', change_api_key),

    # Below regex pulls out id to be used in request as id, see get_payment parameter
    url(r'^api/v1/payments/(?P<payment_id>[\w-]+)/$', get_payment),
]

if settings.URL_PREFIX:
    prefixed_url_pattern = []
    for pat in urlpatterns:
        pat.regex = re.compile(r"^%s/%s" % (settings.URL_PREFIX[1:], pat.regex.pattern[1:]))
        prefixed_url_pattern.append(pat)
    urlpatterns = prefixed_url_pattern

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
