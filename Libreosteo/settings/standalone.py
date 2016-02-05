from .base import *

DEBUG = True
TEMPLATE_DEBUG = True

try :
	from .local import *
except ImportError:
	pass
