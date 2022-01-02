from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []

ROOT_URLCONF = 'config.urls.production'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'digify',
        'USER': 'postgres',
        'PASSWORD': env('db_password'),
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}