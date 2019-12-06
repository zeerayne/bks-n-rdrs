from booksandreaders.settings import *

DATABASES = {
    'default': {'ENGINE': 'django.db.backends.sqlite3', }
}

LOGGING['loggers']['booksandreaders.core'] = {
        'handlers': ['console'],
        'level': 'INFO',
    }
