from .base import *
import os

DEMONSTRATION = True

DEBUG = False
TEMPLATES[0]['OPTIONS']['debug'] = False

DATABASES['default']['NAME'] = os.path.join(DATA_FOLDER, '../db.sqlite3')
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = ('rest_framework.renderers.JSONRenderer',)
HAYSTACK_CONNECTIONS['default']['PATH'] = os.path.join(DATA_FOLDER, '../whoosh_index')


try :
	from .local import *
except ImportError:
	pass
