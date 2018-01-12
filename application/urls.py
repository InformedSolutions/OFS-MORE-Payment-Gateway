import re
from application.views import place_order, get_payment, change_api_key
from django.conf.urls import url

from django.conf import settings

urlpatterns = [
    # See swagger documentation, there are three RESTful URL's
    url(r'^api/v1/payments/(?P<id>[\w-]+)/$', get_payment),
]

if settings.URL_PREFIX:
    prefixed_url_pattern = []
    for pat in urlpatterns:
        pat.regex = re.compile(r"^%s/%s" % (settings.URL_PREFIX[1:], pat.regex.pattern[1:]))
        prefixed_url_pattern.append(pat)
    urlpatterns = prefixed_url_pattern
