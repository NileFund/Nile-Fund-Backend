from .base import *  
from decouple import config
#  Security 
SECRET_KEY = 'django-insecure-%dh*gef#-z6m^)jhy58(@7zlk)%91exs%4v*-o7u5@b5fcat(s'
DEBUG       = True
ALLOWED_HOSTS = ['*']

#  Database  PostgreSQL (local) 
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
# ── Email  print to console, no SMTP needed 
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
