import os
import sys

# imports for logging
import logging
import logging.handlers
import structlog
from pythonjsonlogger import jsonlogger

# env parsing
import envparse

'''
Most of the installs in requirement.txt are tailored made for Heroku setup
1. whitenoise

TODO
1.create an env for [dev, qa, sandbox, and production]
and convert the SECURITY WARNING into an actionable request
2. Move static folder under templates
3. Swap the database to noSQL
4. Understand the importance of swagger
5. Work on log rotation

import envparse will check if .env exists in the home folder
https://django-environ.readthedocs.io/en/latest/
Step 1: setting checks if .env file exists DJANGO_READ_DOT_ENV_FILE
Step 2: if exists, read .env file
Step 3: check for DEBUG flag.
    If DEBUG = 1 debug is on
    Else DEBUG is off
Step 4: similarily check for TESTING (*note it is not setup in .env)
Step 5: if DEBUG is set to TRUE (1)
    Logs information
Step 6: Assign BASE_DIR and set APP_DIR to config folder
Step 7: Add 'rest_framework','rest_framework_swagger','django_extensions'
to INSTALLED APPS
Step 8: Add our apps to INSTALLED_APPS
Step 9: Add Whitenoise to MIDDLEWARE, out-of-the-box helps with compression
Step 10: set config.urls as default urlhandler
Step 11: default template is set to root folder /templates
    Static files are moved to root folder /static/
    [TODO] move the static file in templates folder
Step 12: [TODO] Only default database is setup,
Postgres but needs to be NoSQL - Mongo
Step 13: [In production] set up AUTH_PASSWORD_VALIDATORS
Step 14: [In lower environment] session management
Step 15: [TODO] Why - Setup SWAGGER setting
Step 16: Logging - structlog?
Step 17: logging is set by default to logging.INFO and says logs in python.log
    [TODO] Log rotation
'''

env = envparse.Env()

READ_DOT_ENV_FILE = env.bool(
        'DJANGO_READ_DOT_ENV_FILE', default=False
    )

if READ_DOT_ENV_FILE:
    env.read_envfile()
    print('[+] The .env file has been loaded.See base.py for more information')

'''
SECURITY WARNING
Don't run with debug turned on in production!
'''

DEBUG = env(
        'DEBUG', cast=bool, default=False
        )

'''
NOTE: Determine if we're in testing or not.
'''

TESTING = env(
        'TESTING', cast=bool, default=False
        )

if DEBUG:
    lh = logging.StreamHandler(sys.stderr)
    envparse.logger.addHandler(lh)
    envparse.logger.setLevel(logging.DEBUG)

'''
Build paths inside the project like this
os.path.join(BASE_DIR, ...)
'''

BASE_DIR = os.path.dirname(
                    os.path.dirname(
                        os.path.abspath(__file__)
                        )
                    )

# Unused: ROOT_DIR = BASE_DIR

APPS_DIR = os.path.join(
            BASE_DIR, 'config'
            )

'''
SECURITY WARNING
Ensure secrecy of the secret key atleast when deploying
in production, or when externally facing
'''

SECRET_KEY = env('SECRET_KEY')

host_names = env(
            'ALLOWED_HOSTS', default='localhost'
            )

host_list = host_names.split(',')

ALLOWED_HOSTS = [
    el.strip() for el in host_list
]

# Default setting
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Third-party apps
INSTALLED_APPS += [
    'rest_framework',
    'rest_framework_swagger',
    'django_extensions',
    'djongo'
]

# Our Apps
INSTALLED_APPS += [
    'api.apps.ApiConfig',
]

# Default Setting
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

'''
These are necessary to turn on Whitenoise
which will serve our static files while doing local development
'''
if DEBUG:
    MIDDLEWARE.append('whitenoise.middleware.WhiteNoiseMiddleware')
    WHITENOISE_USE_FINDERS = True
    WHITENOISE_AUTOREFRESH = True

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, "templates"),
        ],
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

''' Static files (CSS, JavaScript, Images)
https://docs.djangoproject.com/en/1.10/howto/static-files/
'''
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Unused STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
   'default' : {
      'ENGINE' : 'djongo',
      'NAME' : env('MONGODB_NAME'),
      'HOST': env('MONGODB_NAME'),
      'PORT': int(env("MONGODB_PORT")),
      'USER': env('MONGODB_USER'),
      'PASSWORD': 'password',
   }
}

REDIS_HOST = env('REDIS_HOST', default="redis")

'''
SECURITY WARNING:
We recommend using password validation in production
https://docs.djangoproject.com/en/2.1/topics/auth/passwords/
'''
AUTH_PASSWORD_VALIDATORS = []

# Testing values
if TESTING:
    PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ]

''' Next few block of lines are about session management
[SECURITY WARNING]
Give each project like 'api'? their own session cookie name
to avoid local development login conflicts

In dev and qa environment - increase default cookie age
from 2 to 12 weeks (which is static 60*60*24*7*12)
#SESSION_COOKIE_AGE = 60*60*24*7*12
'''

SESSION_COOKIE_NAME = "config-sessionid"
SESSION_COOKIE_AGE = 7257600

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Swagger Settings
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
    },
}

'''
We are setting up logging setup for following
Configure struct log
'''
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.render_to_log_kwargs,
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

# Configure Python logging
root = logging.getLogger()
root.setLevel(logging.INFO)

handler = logging.FileHandler('./python.log')
handler.setFormatter(
        jsonlogger.JsonFormatter()
    )

root.addHandler(handler)
