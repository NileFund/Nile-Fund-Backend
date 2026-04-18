from .base import *  
from decouple import config
import os

SECRET_KEY = 'django-insecure-%dh*gef#-z6m^)jhy58(@7zlk)%91exs%4v*-o7u5@b5fcat(s'
DEBUG       = True
ALLOWED_HOSTS = ['*']

# local postgres
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}
INSTALLED_APPS += [
   
]

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

PASSWORD_RESET_TIMEOUT = 86400  # 24 hours in seconds

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# Email Configuration for Gmail SMTP

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587 
EMAIL_USE_TLS = True

EMAIL_HOST_USER = config('EMAIL_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_PASS')
DEFAULT_FROM_EMAIL = f'FundEgypt <{config("EMAIL_USER")}>'



CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = ["http://localhost:5173"]

FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:5173')

CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://localhost:3000',
]
