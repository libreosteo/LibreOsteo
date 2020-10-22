"""
Settings suitable for appimage deployments

In that kind of deployments, read-only app data has to be separated from
read-write user data.

- readonly app data remain inside the .AppImage executable archive
- user data goes into ~/.local/share/libreosteo and ~/.cache/libreosteo
"""

from .base import *

DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = True

# Compression need write access, which cannot work within an appimage
COMPRESS_ENABLED = False

import os
import os.path

# Those are paths that are to be writable : they have to be outside the readonly AppImage
LIBREOSTEO_DATA_DIR = os.path.join(os.environ['HOME'], '.local/share/libreosteo')
LIBREOSTEO_CACHE_DIR = os.path.join(os.environ['HOME'], '.cache/libreosteo')
LIBREOSTEO_MEDIA_DIR = os.path.join(LIBREOSTEO_DATA_DIR, 'media')

os.makedirs(LIBREOSTEO_DATA_DIR, exist_ok=True)
os.makedirs(LIBREOSTEO_CACHE_DIR, exist_ok=True)
os.makedirs(LIBREOSTEO_MEDIA_DIR, exist_ok=True)

MEDIA_ROOT = LIBREOSTEO_MEDIA_DIR

HAYSTACK_CONNECTIONS['default']['PATH'] = os.path.join(
        LIBREOSTEO_CACHE_DIR,
        'whoosh_index',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(LIBREOSTEO_DATA_DIR, 'db.sqlite3'),
        #'ATOMIC_REQUESTS' : True,
    }
}
