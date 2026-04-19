import os
from .base import *
from decouple import config
import dj_database_url


# =========================
# SECURITY
# =========================
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
DEBUG = False

ALLOWED_HOSTS = [
    ".railway.app",
    ".up.railway.app",
    "localhost",
]


# =========================
# DATABASE (Supabase)
# =========================
DATABASES = {
    'default': dj_database_url.parse(
        os.environ["DATABASE_URL"],
        conn_max_age=600,
        ssl_require=True
    )
}


# =========================
# CORS / CSRF
# =========================
FRONTEND_URL = os.environ.get(
    "FRONTEND_URL",
    "https://fundegypt.vercel.app"
)

CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOWED_ORIGINS = [
    FRONTEND_URL,
]

CSRF_TRUSTED_ORIGINS = [
    FRONTEND_URL,
]


# =========================
# EMAIL (Gmail SMTP)
# =========================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp-relay.brevo.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = os.environ['EMAIL_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_PASS']
DEFAULT_FROM_EMAIL = f'FundEgypt <{EMAIL_HOST_USER}>'


# =========================
# SECURITY HEADERS
# =========================
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# =========================
# STATIC FILES
# =========================
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')