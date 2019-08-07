
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
# Python stdlib imports
import sys
import logging
import os, os.path

# Third-party imports
import cherrypy
from cherrypy.process import wspbus, plugins
from cherrypy import _cplogging, _cperror
from django.conf import settings
from Libreosteo.standalone import application
from django.http import HttpResponseServerError
try:
    import ConfigParser
except:
    import configparser as ConfigParser

# For modulegraph import auto detect
import rcssmin
import rjsmin

SERVER_PORT = 8085

logger = logging.getLogger(__name__)

config = ConfigParser.SafeConfigParser({'server.port' : '%s' % SERVER_PORT})
config.read('server.cfg')

if config.has_option('server', 'server.port'):
    SERVER_PORT = config.getint('server', 'server.port')

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
        except Exception as e :
            logger.exception("Exception when starting server")


        if callback :
            callback()

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
        if hasattr(response, 'streaming_content'):
            resp_len = 0
        else:
            resp_len = len(response.content)
        atoms = {'h': environ.get('REMOTE_ADDR', ''),
                 'l': '-',
                 'u': "-",
                 't': self.time(),
                 'r': "%s %s %s" % (environ['REQUEST_METHOD'], environ['REQUEST_URI'], environ['SERVER_PROTOCOL']),
                 's': response.status_code,
                 'b': str(resp_len),
                 'f': environ.get('HTTP_REFERER', ''),
                 'a': environ.get('HTTP_USER_AGENT', ''),
                 }
        for k, v in atoms.items():
            try :
                if isinstance(v, unicode):
                    v = v.encode('utf8')
            except NameError:
                pass
            if not isinstance(v, str):
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

if __name__ == '__main__':
    if "__file__" :
        DATA_FOLDER = os.path.dirname("__file__")
    else :
        DATA_FOLDER = os.path.dirname(sys.argv[0])
    if getattr(sys, 'frozen', False):
        SITE_ROOT = os.path.split(os.path.split(os.path.split(os.path.dirname(os.path.realpath("__file__")))[0])[0])[0]
        DATA_FOLDER = SITE_ROOT
        if (getattr(sys, 'frozen', False) == 'macosx_app'):
    	    DATA_FOLDER = os.path.join( os.path.join( os.path.join( os.environ['HOME'], 'Library'), 'Application Support' ), 'Libreosteo')
    	    SITE_ROOT = os.path.split(SITE_ROOT)[0]
    	    if not os.path.exists(DATA_FOLDER):
    	        os.makedirs(DATA_FOLDER)
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
                'console' : {
                    'level':'INFO',
                    'class':'logging.handlers.RotatingFileHandler',
                    'formatter': 'standard',
                    'filename':os.path.join(DATA_FOLDER, 'console.log'),
                    'maxBytes':10485760,
                    'backupCount':20,
                    'encoding':'utf8'
                    },
	    },
	    'loggers': {
	        '': {
	            'handlers': ['console'],
	            'level': 'INFO'
	        },
	        'db': {
	            'handlers': ['console'],
	            'level': 'INFO' ,
	            'propagate':True
	        },
                'django': {
                    'handlers': ['console'],
                    'level': 'INFO',
                    'propagate' : True
                    },
                'rest_framework': {
                    'handlers': ['console'],
                    'level': 'INFO',
                    'propagate' : True
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
	    }
	}


    logging.config.dictConfig(LOG_CONF)

    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', SERVER_PORT))
    if result != 0:
        Server().run()
