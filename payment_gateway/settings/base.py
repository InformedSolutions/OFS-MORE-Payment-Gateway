import os

WORLDPAY_PAYMENT_ENDPOINT = os.environ.get('WORLDPAY_PAYMENT_ENDPOINT')
WORLDPAY_XML_USERNAME = os.environ.get('WORLDPAY_XML_USERNAME')
WORLDPAY_XML_PASSWORD = os.environ.get('WORLDPAY_XML_PASSWORD')
MERCHANT_CODE = os.environ.get('MERCHANT_CODE')

# HTTP timeout value for interfacing with external
REQUEST_TIMEOUT = os.environ.get('REQUEST_TIMEOUT', 60)


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [],
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    # Parser classes priority-wise for Swagger
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.JSONParser',
    ],
}

# Application definition

BUILTIN_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
]

PROJECT_APPS = [
    'application',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'payment_gateway.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'payment_gateway.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

# No database is needed for the Payment Gateway
DATABASES = {}

LANGUAGE_CODE = 'en-GB'

TIME_ZONE = 'Europe/London'

USE_I18N = True

USE_L10N = True

USE_TZ = True

URL_PREFIX = '/payment-gateway'

STATIC_URL = '/payment-gateway/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Test outputs
TEST_RUNNER = 'xmlrunner.extra.djangotestrunner.XMLTestRunner'
TEST_OUTPUT_VERBOSE = True
TEST_OUTPUT_DESCRIPTIONS = True
TEST_OUTPUT_DIR = 'xmlrunner'

DEV_MODE = os.environ.get('DEV_MODE', False)

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
    'file': {
        'level': 'DEBUG',
        'class': 'logging.handlers.TimedRotatingFileHandler',
        'filename': 'logs/output.log',
        'formatter': 'console',
        'when': 'midnight',
        'backupCount': 10
    },
    'console': {
        'level': 'DEBUG',
        'class': 'logging.StreamHandler'
    },
   },
   'loggers': {
     '': {
       'handlers': ['file', 'console'],
         'level': 'DEBUG',
           'propagate': True,
      },
      'django.server': {
       'handlers': ['file', 'console'],
         'level': 'INFO',
           'propagate': True,
      },
    },
}
