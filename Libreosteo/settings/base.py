"""
Django settings for Libreosteo project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os,sys,logging
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if getattr(sys, 'frozen', False):
    SITE_ROOT = os.path.split(os.path.split(os.path.split(os.path.dirname(os.path.realpath(__file__)))[0])[0])[0]
    DATA_FOLDER = SITE_ROOT
    if (getattr(sys, 'frozen', False) == 'macosx_app'):
    	DATA_FOLDER = os.path.join( os.path.join( os.path.join( os.environ['HOME'], 'Library'), 'Application Support' ), 'Libreosteo')
    	SITE_ROOT = os.path.split(SITE_ROOT)[0]
    	if not os.path.exists(DATA_FOLDER):
    	    os.makedirs(DATA_FOLDER)
else:
    SITE_ROOT = BASE_DIR
    DATA_FOLDER = SITE_ROOT

from django.utils.translation import ugettext_lazy as _

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8xmh#fjyiamw^-_ro9m29^6^81^kc!aiczp)gvb#7with$dzb6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

LOCALE_PATHS = ('locale', os.path.join(SITE_ROOT, 'django', 'conf', 'locale'), os.path.join(SITE_ROOT, 'locale'))

APPEND_SLASH = False

DEMONSTRATION = False


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'haystack',
    'libreosteoweb',
    'django_filters',
    'statici18n',
    'rest_framework',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'libreosteoweb.middleware.LoginRequiredMiddleware',
)

ROOT_URLCONF = 'Libreosteo.urls'

WSGI_APPLICATION = 'Libreosteo.wsgi.application'

STATIC_ROOT = "static/"

TEMPLATE_DIRS = (
    'templates',
    'static',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'Libreosteo.zip_loader.load_template_source'
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_ZIP_FILES = (
    'library.zip',
    )

# Additional locations of static files
#STATICFILES_DIRS = (
# Put strings here, like "/home/html/static" or "C:/www/django/static".
# Always use forward slashes, even on Windows.
# Don't forget to use absolute paths, not relative paths.
#    os.path.join(SITE_ROOT, 'static'),
#    )

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
'django.contrib.staticfiles.finders.FileSystemFinder',
'django.contrib.staticfiles.finders.AppDirectoriesFinder',
# 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


TEMPLATE_CONTEXT_PROCESSORS = (
"django.contrib.auth.context_processors.auth",
"django.core.context_processors.debug",
"django.core.context_processors.i18n",
"django.core.context_processors.media",
"django.core.context_processors.static",
"django.core.context_processors.tz",
"django.contrib.messages.context_processors.messages",
"django.core.context_processors.request",
)
# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(DATA_FOLDER, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'fr'

LANGUAGES = (
    ('fr', _('French')),
    ('en', _('English')),
    )

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        #'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.ModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],

    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',)
}



LOGIN_URL = 'accounts/login'
LOGIN_URL_NAME = 'accounts-login'
LOGOUT_URL_NAME = 'accounts-logout'
LOGIN_REDIRECT_URL= '/'
INITIALIZE_ADMIN_URL_NAME = 'accounts-create-admin'





LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'libreosteoweb': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'libreosteoweb.api':{
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
}

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(DATA_FOLDER, 'whoosh_index'),
    },
}

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
