"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
BACKEND SETTINGS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# from django.conf import settings
# os.path.join(settings.BASE_DIR, ...) ... must not start with /


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
APPLICATION CONFIGURATION
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

INSTALLED_APPS = [
    # django base
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # installed packages
    'django_extensions',
    'rest_framework',
    'corsheaders',
    'webpack_loader',
    # custom apps
    'movies',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',            # corsheaders requirement
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
                    os.path.join(BASE_DIR, os.path.join('app_proj', 'templates')),
                ],
        'APP_DIRS': True,       # needs this for admin templates
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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'localhost',
        'PORT': '',
        'NAME': 'movieDB',
        'USER': 'movieadmin',
        'PASSWORD': 'l9k7j5h3g1a2s4d6f8',
    }
}

ROOT_URLCONF = 'app_proj.urls'
STATIC_URL = '/static/'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
SITE_ID = 1


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
LIVE SERVER SETTINGS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

SECRET_KEY = '2wsrwy%9h)gwl-$6jkk&*@f$+qp0@8dim%rmvz3#qmmp%q#(0m'

DEBUG = True

ALLOWED_HOSTS = []

WSGI_APPLICATION = 'app_proj.setup.wsgi.application'


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
LOGGING 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# CRITICAL, ERROR, WARNING, INFO and DEBUG

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    
    'formatters': {
        'simple': { 
            '()': 'app_proj.utility.SimpleFmt'
        },
        'complete': {   
            '()': 'app_proj.utility.CompleteFmt'
        },
    },
    
    'handlers': {
        'console': {
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'console_error': {
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'complete'
        },
        'logfile': {
            'class': 'logging.FileHandler',
            'filename': 'logfile.log',
            'formatter': 'complete'
        }
    },
    
    'loggers': {
        'progress': {
            'handlers': ['console'],
            'level': 'DEBUG',
         },
        'exception': {
            'handlers': ['console_error', 'logfile'],
            'level': 'WARNING',
        },
        'filelogger': {
            'handlers': ['logfile'],
            'level': 'WARNING',
        }
    }
}


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
INSTALLED PACKAGES 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# REST API

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
        #'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000',
    'http://localhost:8000',
    'http://localhost:8080',
]

WEBPACK_LOADER = {
    'DEFAULT': {
            'BUNDLE_DIR_NAME': 'bundles/',
            'STATS_FILE': os.path.join(BASE_DIR, 'app_proj/setup/webpack-stats.dev.json'),
        }
}

