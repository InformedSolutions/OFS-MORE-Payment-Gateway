from .base import *

WORLDPAY_API_KEY = 'T_S_affb6e01-fd4e-42e4-bed6-5cc45e38ed57'

DEBUG = False

TEST_MODE = False

ALLOWED_HOSTS = ['*']
PUBLIC_APPLICATION_URL = 'http://localhost:8000/payment-service'

PROD_APPS = [
    'whitenoise',
]

PROD_MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

INSTALLED_APPS = BUILTIN_APPS + THIRD_PARTY_APPS + PROD_APPS + PROJECT_APPS
MIDDLEWARE = MIDDLEWARE + PROD_MIDDLEWARE

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5xfw@*imgau)r!_h^i4p!gh0&e9s75!j6j3@g+7yri1jetk1%b'
