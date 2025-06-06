import os
import dj_database_url
from .settings import *
from .settings import BASE_DIR

ALLOWED_HOSTS = [
    'tiffin-application.onrender.com',
    os.environ.get('RENDER_EXTERNAL_HOSTNAME')
]

CORS_ALLOWED_ORIGINS = ['https://tiffin-application-frontend.onrender.com']

CSRF_TRUSTED_ORIGINS = [
    'https://tiffin-application.onrender.com',
    'https://' + os.environ.get('RENDER_EXTERNAL_HOSTNAME', '')
]

DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY')

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
   
]




DATABASES = {
    'default':dj_database_url.config(
        default=os.environ['DATABASE_URL'],
        conn_max_age=600
    )
}

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
