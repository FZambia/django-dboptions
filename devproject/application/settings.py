import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

sys.path.insert(1, BASE_DIR + '/..')

SECRET_KEY = '($7wfk^1hd5+i-2j1k^h$v^-r-7r$47f@2-9&_%5tlk^9wwfi6'

DEBUG = True

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'dboptions',
    'core'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'application.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

DBOPTIONS = [
    {
        "name": "DEFAULT_CACHE_INTERVAL",
        "default": 60,
        "description": "sets default cache interval in seconds",
        "cast": int
    },
    {
        "name": "NOTIFICATIONS_ENABLED",
        "default": True,
        "description": "allows to enable/disable notifications on site",
        "cast": "bool"
    }
]
