import os
import environ


env = environ.Env(
    DEBUG=(bool, False)
)
if os.path.isfile('.env'):
    environ.Env.read_env(env_file='.env')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = env("DEBUG")

SECRET_KEY = env("SECRET_KEY")

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',

    'booksandreaders.library',
]

if DEBUG:
    INSTALLED_APPS += [
        'django.contrib.admin',
        'django_extensions',
    ]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}

if DEBUG:
    REST_FRAMEWORK = {

    }

ROOT_URLCONF = 'booksandreaders.urls'

WSGI_APPLICATION = 'booksandreaders.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime} [{levelname:3.3s}] <{module}> {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        }
    },
    'loggers': {
        'django.db': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'faker': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    }
}


DATABASES = {
    'default': env.db('MASTER_URL'),
    'slave': env.db('SLAVE_URL'),
}

for db in DATABASES.values():
    db['OPTIONS'] = {
        'connect_timeout': 1,
    }

DATABASE_ROUTERS = ['booksandreaders.core.routers.LoadBalanceRouter', ]

DATABASE_ROUTER_CACHE_KEY = 'database-router-cache'
DATABASE_ROUTER_CACHE_TIMEOUT = 30

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

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'default-cache-snowflake',
        'TIMEOUT ': DATABASE_ROUTER_CACHE_TIMEOUT,
    },
    DATABASE_ROUTER_CACHE_KEY: {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': f'{DATABASE_ROUTER_CACHE_KEY}-snowflake',
        'TIMEOUT ': DATABASE_ROUTER_CACHE_TIMEOUT,
    },
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
