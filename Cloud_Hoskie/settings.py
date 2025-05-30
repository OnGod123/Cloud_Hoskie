import os
from dotenv import load_dotenv
"""
Django settings for Cloud_Hoskie project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
from elasticsearch_dsl import connections
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-fddj0p!o507bt&ks!j3if344p5snrbi=n4*r9_)8)-=y$i8la('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver']
PAYSTACK_PUBLIC_KEY = "your_public_key_here"
PAYSTACK_SECRET_KEY = "your_secret_key_here"



# Application definition
load_dotenv()

# Your existing settings...

# Google API credentials
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

# Instagram API credentials
INSTAGRAM_APP_ID = os.getenv('INSTAGRAM_APP_ID')
INSTAGRAM_ACCESS_TOKEN = os.getenv('INSTAGRAM_ACCESS_TOKEN')

# Facebook API credentials
FACEBOOK_APP_ID = os.getenv('FACEBOOK_APP_ID')
FACEBOOK_BEARER_TOKEN = os.getenv('FACEBOOK_BEARER_TOKEN')


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # Corrected string
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'rest_framework',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.instagram',
    'django_elasticsearch_dsl',
    'myapp.profile',# Your other custom app
    'channels',
    'myapp.video_call',
    'myapp.chat',
    'myapp.voice_message',
    'myapp.file_upload',
    'myapp.go_live',
    'myapp.authentication',
    'myapp.wallet',
    'myapp.followers',
    'myapp.Userrs_like',
    'myapp.profile.tweet.mentions',
    'myapp.apps.MyAppConfig',
    'corsheaders', 
]


ASGI_APPLICATION = 'myapp.asgi.application'



SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)
LOGIN_URL = '/sign-in/'
LOGIN_REDIRECT_URL = '/home/'  # Redirect to home page after login
ACCOUNT_LOGOUT_REDIRECT_URL = '/'  # Redirect to home page after logout

ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Cloud_Hoskie.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                #'allauth.account.context_processors.account',
                #'allauth.socialaccount.context_processors.socialaccount',
            ],
        },
    },
]


WSGI_APPLICATION = 'Cloud_Hoskie.wsgi.application'
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}



SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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

SESSION_HISTORY_MAX_LENGTH = 20


if DEBUG:
    # Use Django's console email backend for development (emails are printed in the console)
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    # Use Gmail's SMTP server for production
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = 'fantasiaorg531@gmail.com'  # Replace with your actual email address
    EMAIL_HOST_PASSWORD = 'dmov yzic vbtl fkbo'  # Replace with your email password or app-specific password





LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'django_errors.log',  # Log file name
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'myapp': {  # Replace 'myapp' with the actual name of your app
            'handlers': ['console', 'file'],
            'level': 'ERROR',
        },
    },
}

SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'APP': {
            'client_id': os.getenv('FACEBOOK_APP_ID'),
            'secret': os.getenv('FACEBOOK_BEARER_TOKEN'),
            'key': ''
        },
        # Other configurations...
    },
    'google': {
        'APP': {
            'client_id': os.getenv('GOOGLE_CLIENT_ID'),
            'secret': os.getenv('GOOGLE_CLIENT_SECRET'),
            'key': ''
        },
    },
    'instagram': {
        'APP': {
            'client_id': os.getenv('INSTAGRAM_APP_ID'),
            'secret': os.getenv('INSTAGRAM_ACCESS_TOKEN'),
            'key': ''
        },
        'SCOPE': ['user_profile'],
    },
}


# Elasticsearch configuration
ELASTICSEARCH_DSL = {
     'default': {
        'hosts': ['http://127.0.0.1:9200'],  # Localhost and default Elasticsearch port
        'timeout': 60  # Optional timeout
    }
}

# Extra parameters (these are not part of the Elasticsearch connection, but can be used elsewhere)
ELASTICSEARCH_EXTRA_PARAMS = {}


connections.configure(
    default={
        'hosts': ['https://58749e6b2df24d64b31c5b1519e66fc0.us-central1.gcp.cloud.es.io:443'],  # Your Elasticsearch endpoint
        'http_auth': ('api_key', 'SzYwbEVaTUJUbk5HdjdMUFRWOU46bXRtUmI5MkdRcDZUeU9hcjk5V2pUQQ=='),  # New API key
        'timeout': 30  # Optional: increase timeout if necessary
    }
)


CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',  # Use InMemoryChannelLayer for in-memory storage
    },
}

# ASGI application (ensure it's set up for ASGI)
ASGI_APPLICATION = 'myapp.asgi.application'  # Replace with your project's ASGI application path
# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",  # Add the domains you want to allow
    "http://127.0.0.1:8000",
    "http://example.com",  # Add other domains as necessary
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

VIDEO_URL = '/video/'
VIDEO_ROOT = os.path.join(MEDIA_ROOT, 'videos')

IMAGE_URL = '/image/'
IMAGE_ROOT = os.path.join(MEDIA_ROOT, 'images')


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
