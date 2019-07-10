
# This file is part of Libreosteo.
#
# Libreosteo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Libreosteo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Libreosteo.  If not, see <http://www.gnu.org/licenses/>.
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
    logger = logging.getLogger(__name__)
    logger.info("Frozen with attribute value %s" % (getattr(sys, 'frozen', False)))
    logger.info("Real path of the start : %s " % (os.path.realpath(__file__)))
    SITE_ROOT = os.path.split(os.path.split(os.path.split(os.path.dirname(os.path.realpath(__file__)))[0])[0])[0]
    logger.info("SITE_ROOT = %s" % SITE_ROOT)
    if (getattr(sys, 'frozen', False)) :
        SITE_ROOT = os.path.split(SITE_ROOT)[0]
    DATA_FOLDER = SITE_ROOT
    if (getattr(sys, 'frozen', False) == 'macosx_app'):
    	DATA_FOLDER = os.path.join( os.path.join( os.path.join( os.environ['HOME'], 'Library'), 'Application Support' ), 'Libreosteo')
    	SITE_ROOT = os.path.join( os.path.split(SITE_ROOT)[0], 'Resources')
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

ALLOWED_HOSTS = ['*']

LOCALE_PATHS = ('locale', os.path.join(SITE_ROOT, 'django', 'conf', 'locale'), os.path.join(SITE_ROOT, 'locale'))

APPEND_SLASH = False

DEMONSTRATION = False

COMPRESS_ENABLED=True

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
    'compressor'
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

STATIC_ROOT = os.path.join(SITE_ROOT, "static/")

MEDIA_ROOT = os.path.join(DATA_FOLDER, "media/")

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(SITE_ROOT, 'templates'),
            os.path.join(SITE_ROOT, 'static'),
        ],
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                #'Libreosteo.zip_loader.Loader',
            ]
        },       
    },
]


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
'compressor.finders.CompressorFinder',
# 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(DATA_FOLDER, 'db.sqlite3'),
        #'ATOMIC_REQUESTS' : True,
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

MEDIA_URL = '/files/'


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

    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',)
}



LOGIN_URL = 'accounts/login'
LOGIN_URL_NAME = 'login'
LOGOUT_URL_NAME = 'logout'
LOGIN_REDIRECT_URL= '/'
INITIALIZE_ADMIN_URL_NAME = 'install'
NO_REROUTE_PATTERN_URL = [ r'^accounts/create-admin/$', r'^internal/restore', r'^jsi18n', r'^web-view/partials/restore', r'^web-view/partials/register' ]





LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
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
        'django.server': {
            'handlers': ['console'],
            'level': 'INFO',
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

COMPRESS_CSS_FILTERS = ['compressor.filters.css_default.CssAbsoluteFilter','compressor.filters.cssmin.rCSSMinFilter']

DISPLAY_SERVICE_NET_HELPER=True
