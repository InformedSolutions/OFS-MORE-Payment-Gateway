from .base import *

#WORLDPAY_API_KEY = os.environ.get('WORLDPAY_API_KEY')

DEBUG = True

#TEST_MODE = True
#DEV_MODE = True

ALLOWED_HOSTS = ['*']
PUBLIC_APPLICATION_URL = 'http://localhost:8000/payment-service'
INTERNAL_IPS = "127.0.0.1"

DEV_APPS = [
  'debug_toolbar'
]

MIDDLEWARE_DEV = [
  'debug_toolbar.middleware.DebugToolbarMiddleware'
]

MIDDLEWARE = MIDDLEWARE + MIDDLEWARE_DEV
INSTALLED_APPS = BUILTIN_APPS + THIRD_PARTY_APPS + DEV_APPS + PROJECT_APPS

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'oc960$rkfa@wulw4yjseyyoz=!3wwn5z!+v%ps9*3twq2c6p=e'
