from .base import *

WORLDPAY_API_KEY = os.environ.get('WORLDPAY_API_KEY')

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

# Automatic Django logging at the INFO level (i.e everything the comes to the console when ran locally)
LOGGING = {
  'version': 1,
  'disable_existing_loggers': False,
  'formatters': {
    'console': {
            # exact format is not important, this is the minimum information
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
        },
  'handlers': {
    'django.server': {
        'level': 'INFO',
        'class': 'logging.handlers.RotatingFileHandler',
        'maxBytes': 1 * 1024 * 1024,
        'filename': 'logs/output.log',
        'formatter': 'console',
        'maxBytes': 1 * 1024 * 1024,
        'backupCount': 30
    },
   },
  'loggers': {
     'django.server': {
       'handlers': ['django.server'],
         'level': 'INFO',
           'propagate': True,
      },
    },
}