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
Requires Mark Hammond's pywin32 package.
"""

# Python stdlib imports
import sys
import logging
import os, os.path

if getattr(sys, 'frozen', False):
        # frozen
        dir = os.path.dirname(sys.executable)
        sys.path.append(dir)
        os.environ['PATH'] = (os.environ['PATH']+";").join(p+";" for p in sys.path)

# Win32 service imports
import win32serviceutil
import win32service
import servicemanager

# Third-party imports
import cherrypy
from cherrypy.process import wspbus, plugins
from cherrypy import _cplogging, _cperror
from django.conf import settings
from django.http import HttpResponseServerError
import webbrowser
import patch
import server

class LibreosteoService(win32serviceutil.ServiceFramework):
    """Libreosteo NT Service."""

    _svc_name_ = "LibreosteoService"
    _svc_display_name_ = "Libreosteo Service"

    def SvcDoRun(self):
        _srvr = Server()


        # in practice, you will want to specify a value for
        # log.error_file below or in your config file.  If you
        # use a config file, be sure to use an absolute path to
        # it, as you can't be assured what path your service
        # will run in.
        cherrypy.config.update({
            'global':{
                'log.screen': False,
                'engine.autoreload.on': False,
                'engine.SIGHUP': None,
                'engine.SIGTERM': None,
                'log.error_file' : os.path.join(_srvr_.base_dir, 'libreosteo_error.log'),
                'tools.log_tracebacks.on' : True,
                'log.access_file' : os.path.join(_srvr.base_dir, 'libreosteo_access.log'),
                'server.socket_port': server.SERVER_PORT,
                'server.socket_host': '0.0.0.0',
                }
            })
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_,'')
        )
        _srvr.run()


    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        cherrypy.engine.exit()

        self.ReportServiceStatus(win32service.SERVICE_STOPPED)
        # very important for use with py2exe
        # otherwise the Service Controller never knows that it is stopped !

if __name__ == '__main__':
    if getattr(sys, 'frozen', False):
        # frozen
        DATA_FOLDER = os.path.dirname(sys.executable)
    else:
        # unfrozen
        DATA_FOLDER = os.path.dirname(os.path.realpath(__file__))
    LOG_CONF = {
            'version': 1,

            'formatters': {
                'void': {
                    'format': ''
                },
                'standard': {
                    'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
                },
            },
            'handlers': {
                'default': {
                    'level':'INFO',
                    'class':'logging.StreamHandler',
                    'formatter': 'standard',
                    'stream': 'ext://sys.stdout'
                },
                'cherrypy_console': {
                    'level':'INFO',
                    'class':'logging.StreamHandler',
                    'formatter': 'void',
                    'stream': 'ext://sys.stdout'
                },
                'cherrypy_access': {
                    'level':'INFO',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'formatter': 'void',
                    'filename': os.path.join(DATA_FOLDER, 'access.log'),
                    'maxBytes': 10485760,
                    'backupCount': 20,
                    'encoding': 'utf8'
                },
                'cherrypy_error': {
                    'level':'INFO',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'formatter': 'void',
                    'filename': os.path.join(DATA_FOLDER, 'errors.log'),
                    'maxBytes': 10485760,
                    'backupCount': 20,
                    'encoding': 'utf8'
                },
            },
            'loggers': {
            'django.utils.translation': {
                    'handlers': ['default', 'cherrypy_error'],
                    'level': 'INFO'
                },
                '': {
                    'handlers': ['default', 'cherrypy_error'],
                    'level': 'INFO'
                },
                'db': {
                    'handlers': ['default'],
                    'level': 'INFO' ,
                    'propagate': False
                },
                'cherrypy.access': {
                    'handlers': ['cherrypy_access'],
                    'level': 'INFO',
                    'propagate': False
                },
                'cherrypy.error': {
                    'handlers': ['cherrypy_console', 'cherrypy_error'],
                    'level': 'INFO',
                    'propagate': False
                },
                'libreosteoweb.api' : {
                    'handlers': ['cherrypy_console', 'cherrypy_error'],
                    'level': 'INFO',
                    'propagate': False
                },
                'Libreosteo' : {
                    'handlers': ['cherrypy_console', 'cherrypy_error'],
                    'level': 'INFO',
                    'propagate': False
                },
            }
        }


    logging.config.dictConfig(LOG_CONF)
    os.chdir(DATA_FOLDER)
    logging.info(os.getcwd())
    logger = logging.getLogger(__name__)
    logger.info("Frozen with attribute value %s" % (getattr(sys, 'frozen', False)))
    if len(sys.argv) == 1:
        logging.info("Start service")
        logging.info("Handle starting of the service")
        try:
            servicemanager.Initialize()
            servicemanager.PrepareToHostSingle(LibreosteoService)
            servicemanager.StartServiceCtrlDispatcher()
        except Exception as e:
            logging.exception("Exception when starting service")
    else:
        logging.info("Start Controller")
        logging.info("Handle command line on service manager")
        try:
            win32serviceutil.HandleCommandLine(LibreosteoService)
        except Exception as e:
            logging.exception("Exception when starting service")
