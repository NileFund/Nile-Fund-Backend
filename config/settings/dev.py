from .base import *  
from decouple import config
import os

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
INSTALLED_APPS += [
   
]

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': config('CLOUDINARY_API_KEY'),
    'API_SECRET': config('CLOUDINARY_API_SECRET'),
}

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

PASSWORD_RESET_TIMEOUT = 86400  # 24 hours in seconds

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Pull the URL from .env, but default to localhost just in case
FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:5173')
