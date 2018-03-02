from django.conf import settings
from django.conf.urls import url, include

urlpatterns = [
    # Copy URL patterns from application/urls.py
    url(r'^', include('application.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
