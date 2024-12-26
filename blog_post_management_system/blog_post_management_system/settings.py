"""
Django settings for blog_post_management_system project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-z*8za1q^prl46iyc^^^i6oy$ep3-5q0^vkja_!sim3ehv3+@jc"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


LOGIN_REDIRECT_URL = '/blogs/'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap5',
    'minio_storage',
    'storage',
]

EXTERNAL_APPS = [
    'accounts','blogs','comments','likes',
]

INSTALLED_APPS += EXTERNAL_APPS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CUSTOM_MIDDLEWARE = ['blog_post_management_system.middleware.NoCacheMiddleware',]

MIDDLEWARE += CUSTOM_MIDDLEWARE

ROOT_URLCONF = 'blog_post_management_system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'blog_post_management_system.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        # 'ENGINE': 'django.db.backends.postgresql',
        # 'NAME': 'blog_post_database',
        # 'USER': 'postgres',
        # 'PASSWORD': 'vivek',
        # 'HOST': '127.0.0.1',
        # 'PORT': '5433',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",  # Root-level static folder
]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = '/images/'
MEDIA_ROOT = BASE_DIR/ 'static'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email Serivice Settings

EMAIL_BACKEND = os.getenv("EMAIL_BACKEND")
EMAIL_HOST= os.getenv("EMAIL_HOST")
EMAIL_PORT= os.getenv("EMAIL_PORT")
EMAIL_USE_TLS= os.getenv("EMAIL_USE_TLS")
EMAIL_HOST_USER= os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD= os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL= os.getenv("DEFAULT_FROM_EMAIL")
TEMPLATE_ID= os.getenv("TEMPLATE_ID")


# ## MinIo settings for s3boto3 script

# # MinIO Storage Configuration
# DEFAULT_FILE_STORAGE=os.getenv("DEFAULT_FILE_STORAGE")
# # STATICFILES_STORAGE=os.getenv("STATICFILES_STORAGE")

# # MinIO Server Details
# MINIO_STORAGE_ENDPOINT=os.getenv("MINIO_STORAGE_ENDPOINT")
# MINIO_STORAGE_ACCESS_KEY=os.getenv("MINIO_STORAGE_ACCESS_KEY")
# MINIO_STORAGE_SECRET_KEY=os.getenv("MINIO_STORAGE_SECRET_KEY")
# MINIO_STORAGE_USE_HTTPS=os.getenv("MINIO_STORAGE_USE_HTTPS")

# # MinIO Media Storage Settings
# MINIO_STORAGE_MEDIA_BUCKET_NAME=os.getenv("MINIO_STORAGE_MEDIA_BUCKET_NAME")
# MINIO_STORAGE_AUTO_CREATE_MEDIA_BUCKET=os.getenv("MINIO_STORAGE_AUTO_CREATE_MEDIA_BUCKET")

# MINIO_STORAGE_MEDIA_URL=os.getenv("MINIO_STORAGE_MEDIA_URL")




# MinIO Configuration
# Default File Storage for MinIO django connect with minio backend
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_ACCESS_KEY_ID = os.getenv("MINIO_STORAGE_ACCESS_KEY", "default_access_key")
AWS_SECRET_ACCESS_KEY = os.getenv("MINIO_STORAGE_SECRET_KEY", "default_secret_key")
AWS_STORAGE_BUCKET_NAME = os.getenv("MINIO_STORAGE_MEDIA_BUCKET_NAME", "default_bucket_name")
TEMP = os.getenv("MINIO_STORAGE_ENDPOINT")
AWS_S3_ENDPOINT_URL = f"http://{TEMP}"  

AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = "public-read"  







