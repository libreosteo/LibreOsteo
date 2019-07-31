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
from Libreosteo.standalone import application
from django.http import HttpResponseServerError
import webbrowser
import patch


SERVER_PORT = 8085



def _exit(self):
    """Stop all services and prepare to exit the process."""
    exitstate = self.state
    try:
        self.stop()

        self.state = states.EXITING
        self.log('Bus EXITING')
        self.publish('exit')
        # This isn't strictly necessary, but it's better than seeing
        # "Waiting for child threads to terminate..." and then nothing.
        self.log('Bus EXITED')
    except:
        # This method is often called asynchronously (whether thread,
        # signal handler, console handler, or atexit handler), so we
        # can't just let exceptions propagate out unhandled.
        # Assume it's been logged and just die.
        return  # EX_SOFTWARE

    if exitstate == states.STARTING:
        # exit() was called before start() finished, possibly due to
        # Ctrl-C because a start listener got stuck. In this case,
        # we could get stuck in a loop where Ctrl-C never exits the
        # process, so we just call os.exit here.
        return

original_exit = cherrypy.process.wspbus.Bus.exit
cherrypy.process.wspbus.Bus.exit = _exit

class Server(object):
    def __init__(self):
        self.base_dir = os.path.abspath(os.getcwd())

        #conf_path = os.path.join(self.base_dir, ".", "server.cfg")
        #cherrypy.config.update(conf_path)

        # This registers a plugin to handle the Django app
        # with the CherryPy engine, meaning the app will
        # play nicely with the process bus that is the engine.
        DjangoAppPlugin(cherrypy.engine, self.base_dir).subscribe()

    def run(self, callback=None):
        engine = cherrypy.engine
        cherrypy.config.update({'server.socket_host': '0.0.0.0'})
        cherrypy.config.update({'server.socket_port': SERVER_PORT})

        engine.signal_handler.subscribe()

        if hasattr(engine, "console_control_handler"):
            engine.console_control_handler.subscribe()

        try :
            engine.start()
        except :
            pass


        if callback :
            callback()
        logging.info("From service : %s" , os.getcwd())
        if engine.state == cherrypy.engine.states.STARTED:
            engine.block()

class DjangoAppPlugin(plugins.SimplePlugin):
    def __init__(self, bus, base_dir):
        """
        CherryPy engine plugin to configure and mount
        the Django application onto the CherryPy server.
        """
        plugins.SimplePlugin.__init__(self, bus)
        self.base_dir = base_dir

    def start(self):
        self.bus.log("Configuring the Django application")

        # Well this isn't quite as clean as I'd like so
        # feel free to suggest something more appropriate
        #from Libreosteo.settings import *
        #app_settings = locals().copy()
        #del app_settings['self']
        #settings.configure(**app_settings)

        self.bus.log("Mounting the Django application")
        cherrypy.tree.graft(HTTPLogger(application), "/")

        self.bus.log("Setting up the static directory to be served")
        # We server static files through CherryPy directly
        # bypassing entirely Django
        static_handler = cherrypy.tools.staticdir.handler(section="/", dir="static",
                                                          root=self.base_dir)
        cherrypy.tree.mount(static_handler, '/static')

class HTTPLogger(_cplogging.LogManager):
    def __init__(self, app):
        _cplogging.LogManager.__init__(self, id(self), cherrypy.log.logger_root)
        self.app = app

    def __call__(self, environ, start_response):
        """
        Called as part of the WSGI stack to log the incoming request
        and its response using the common log format. If an error bubbles up
        to this middleware, we log it as such.
        """
        try:
            response = self.app(environ, start_response)
            self.access(environ, response)
            return response
        except:
            self.error(traceback=True)
            return HttpResponseServerError(_cperror.format_exc())

    def access(self, environ, response):
        """
        Special method that logs a request following the common
        log format. This is mostly taken from CherryPy and adapted
        to the WSGI's style of passing information.
        """
        atoms = {'h': environ.get('REMOTE_ADDR', ''),
                 'l': '-',
                 'u': "-",
                 't': self.time(),
                 'r': "%s %s %s" % (environ['REQUEST_METHOD'], environ['REQUEST_URI'], environ['SERVER_PROTOCOL']),
                 's': response.status_code,
                 'b': str(len(response.content)),
                 'f': environ.get('HTTP_REFERER', ''),
                 'a': environ.get('HTTP_USER_AGENT', ''),
                 }
        for k, v in atoms.items():
            try :
                if isinstance(v, unicode):
                    v = v.encode('utf8')
                elif not isinstance(v, str):
                    v = str(v)
            except NameError:
                v = str(v)
            # Fortunately, repr(str) escapes unprintable chars, \n, \t, etc
            # and backslash for us. All we have to do is strip the quotes.
            v = repr(v)[1:-1]
            # Escape double-quote.
            atoms[k] = v.replace('"', '\\"')

        try:
            self.access_log.log(logging.INFO, self.access_log_format % atoms)
        except:
            self.error(traceback=True)


class LibreosteoService(win32serviceutil.ServiceFramework):
    """Libreosteo NT Service."""

    _svc_name_ = "LibreosteoService"
    _svc_display_name_ = "Libreosteo Service"

    def SvcDoRun(self):
        server = Server()


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
                'log.error_file' : os.path.join(server.base_dir, 'libreosteo_error.log'),
                'tools.log_tracebacks.on' : True,
                'log.access_file' : os.path.join(server.base_dir, 'libreosteo_access.log'),
                'server.socket_port': SERVER_PORT,
                'server.socket_host': '0.0.0.0',
                }
            })
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_,'')
        )
        server.run()


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
