from .base import *

WORLDPAY_API_KEY = 'T_S_affb6e01-fd4e-42e4-bed6-5cc45e38ed57'

DEBUG = True

TEST_MODE = True

ALLOWED_HOSTS = ['*']
PUBLIC_APPLICATION_URL = 'http://localhost:8000/payment-service'

INSTALLED_APPS = BUILTIN_APPS + THIRD_PARTY_APPS + PROJECT_APPS

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-m*c=fbc#x&@3-ezm+sfh3w+h#y9-qog(jk$i+c5)rgk=b2fzh'
