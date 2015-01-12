from django.apps import AppConfig

class LibreosteoConfig(AppConfig):
    name = 'libreosteoweb'
    verbose_name = "Libreosteo WebApp"

    def ready(self):
    	import api.receivers