from django.conf.urls import url, include

urlpatterns = [
    # Copy URL patterns from application/urls.py
    url(r'^', include('application.urls')),
]

