from django.apps import AppConfig
from sqlite3 import OperationalError
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class LibreosteoConfig(AppConfig):
    name = 'libreosteoweb'
    verbose_name = "Libreosteo WebApp"

    def ready(self):
    	import api.receivers
    	import models
        file_import_list = models.FileImport.objects.all()
    	try:
    		for f in file_import_list:
    		  f.delete()
    	except Exception:
    	   logger.debug("Exception when purging files at starting application")
        