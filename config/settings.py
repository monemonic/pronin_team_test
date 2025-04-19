from datetime import timedelta
from os import getenv
from pathlib import Path

import django.core.management.utils
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = getenv('SECRET_KEY', django.core.management.utils.get_random_secret_key())

DEBUG = getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = getenv('ALLOWED_HOSTS', 'localhost').split()

CORS_ALLOWED_ORIGINS = getenv('CORS_ALLOWED_ORIGINS', 'http://localhost').split()
CORS_ALLOW_CREDENTIALS = getenv('CORS_ALLOW_CREDENTIALS', 'False') == 'True'
CSRF_TRUSTED_ORIGINS = getenv('CSRF_TRUSTED_ORIGINS', 'http://localhost').split()

AUTH_USER_MODEL = 'user_app.User'

CELERY_BROKER_URL = getenv('CELERY_BROKER', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = getenv('CELERY_BROKER', 'redis://redis:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework_simplejwt',
    'djoser',
    'drf_spectacular',

    'api',
    'user_app',
    'collect_app',
    'utils_app'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'config.middleware.query_logging.QueryLoggingMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

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

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(weeks=int(getenv('ACCESS_TOKEN_LIFETIME_MINUTES', 10))),
    'REFRESH_TOKEN_LIFETIME': timedelta(weeks=int(getenv('REFRESH_TOKEN_LIFETIME_DAYS', 10))),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = 'emails'
EMAIL_HOST_USER = getenv('EMAIL_HOST_USER')


if getenv('TEST_DATABASE', 'False') == 'True':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'HOST': getenv('DB_HOST', ''),
            'PORT': getenv('DB_PORT', '5432'),
            'NAME': getenv('POSTGRES_DB', 'django_db'),
            'USER': getenv('POSTGRES_USER', 'django_user'),
            'PASSWORD': getenv('POSTGRES_PASSWORD', ''),
        }
    }

if getenv('LOCAL', 'False') == 'True':
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': 'redis://127.0.0.1:6379/1',
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            }
        }
    }

else:
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': f'redis://{getenv('REDIS_HOST', 'localhost')}:{getenv('REDIS_PORT', '6379')}/1',
        }
    }

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message} {funcName}',
            'style': '{',
        },
    },
    'handlers': {
        'query_logging_file': {
            'class': 'logging.FileHandler',
            'filename': 'query_logs.log',
        },
    },
    'loggers': {
        'config.middleware.query_logging': {
            'level': 'DEBUG',
            'handlers': ['query_logging_file'],
            'propagate': False,
        },
    },
}

SPECTACULAR_SETTINGS = {
    'SWAGGER_UI_SETTINGS': {
        'filter': True
    },
    'TITLE': 'Документация для ProninTeam Test',
    'SORT_OPERATIONS': True,
}
