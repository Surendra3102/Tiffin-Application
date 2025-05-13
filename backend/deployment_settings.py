import os
import dj_database_url
from .settings import *
from .settings import BASE_DIR

hostname = os.environ.get('RENDER_EXTERNAL_HOSTNAME')

ALLOWED_HOSTS = ['tiffin-application.onrender.com']
if hostname:
    ALLOWED_HOSTS.append(hostname)

CSRF_TRUSTED_ORIGINS = [f'https://{hostname}'] if hostname else ['https://tiffin-application.onrender.com']
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


STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
        'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    }
}

DATABASES = {
    'default':dj_database_url.config(
        default=os.environ['DATABASE_URL'],
        conn_max_age=600
    )
}