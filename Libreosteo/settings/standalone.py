from .base import *

DEBUG = True
TEMPLATE_DEBUG = True
COMPRESS_ENABLED = True

try :
	from .local import *
except ImportError:
	pass
