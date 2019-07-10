============
 LibreOsteo
============

.. image:: https://travis-ci.com/libreosteo/Libreosteo.svg?branch=develop
    :target: https://travis-ci.com/libreosteo/Libreosteo
© Jean-Baptiste Gury 2014-2018

*LibreOsteo*

Libreosteo is a business application designed for osteopaths.

It manages patients, folder and runs as a work portal on a folder patient.

Browser supported :
  - Google Chrome or Chromium
  - Firefox 

Please use the last version of these browsers.

You can try the online demo at http://garthylou.pythonanywhere.com
login : demo
password : demo

Contact
=======

Problems or questions contact me at github_

HOW-TO try it ?
===============

Requirements :
  - Python 2.7+ or Python 3.3+ (if you have no opinion, 2.7+ is the recommended choice for now)
  - pip 
  - nodejs
  - ~bower~ yarn
  - virtualenv
  - nodejs and npm (if on Debian, you will need `nodesource packages`_, official ones will not work)
  - bower
  - if on linux system, you need linux-headers package. On debian and derivated uses ::
  
    sudo apt install linux-headers-$(uname -r)

.. _nodesource packages: https://github.com/nodesource/distributions#debinstall

Install system dependencies, for example, on Debian-like sytem, that would **one of** those two lines:

Python 2.x ::

    sudo apt install python-pip python-virtualenv nodejs

Python 3.x ::

    sudo apt install python3-pip virtualenv nodejs

Retrieve the content of the project from Git repository ::

    git clone https://github.com/libreosteo/Libreosteo.git

Enter the cloned folder ::

    cd Libreosteo

Create a virtualenv with **one of those** two commands.

Python 2 ::

    virtualenv venv
    

Python 3 ::
    
    virtualenv --python /usr/bin/python3 venv

(at virtualenv creation you automatically entered the virtualenv, if you close the terminal, you will need to enter the virtualenv manually using ``source venv/bin/activate``).

Then retrieve the python requirements with **one of those**.

Python 2 ::

    pip install -r requirements/requ-py2.txt

Python 3 ::

    pip install -r requirements/requirements.txt

Install Javascript dependencies ::

    yarn

Initialize the database ::

    python manage.py migrate
    
Now you can start the server with ::

    python manage.py runserver

Point your browser on : http://localhost:8000/ it will guide you towards creating the first admin user.

Have fun !


Use it in production 
====================
You can use the software in production by changing some settings.

Settings are in the folder
::

   Libreosteo/settings/

There are some settings in this folder, the base_ settings is the main settings. All settings should
use this base settings as reference.
You can define your own base settings, but advice is to use standalone_ setting, and add a local.py file in this 
folder to define your own customization.

Setting to avoid debug trace
----------------------------
::

   DEBUG = False
   TEMPLATES[0]['OPTIONS']['debug'] = False

Setting for Database
--------------------
   
For example, to define postgresql as database backend instead of sqlite3 (the default), you can use this definition.
::

   DATABASES = {
      'default': {
               'ENGINE': 'django.db.backends.postgresql_psycopg2',
               'NAME': 'libreosteo',
               'USER': 'libreosteo',
               'PASSWORD': 'libreosteo',
               'HOST': '127.0.0.1',
               'PORT': '5432',
      }
   }

You have to adapt your value with your installation, and configuration of the database used.
But you can use other database backend, there is no specificity used in the software linked to the implementation of the database.

Setting for Cryptograhic key for CSRF_ 
--------------------------------------
In order to have protection against CSRF_, you have to override and change the value of SECRET_KEY, with a value computed by `this script for example`_
like this :
::

   SECRET_KEY = "T}wf)m[?494-xG?9oO7C#3|K$Ox^!:BEJ^g3S+:&t!@pvv1oR]"

.. _CSRF: https://en.wikipedia.org/wiki/Cross-site_request_forgery
.. _`this script for example`:  https://gist.github.com/mattseymour/9205591

Use Http Service to provide the web application
-----------------------------------------------

In order to have a compliant solution to serve libreosteo, you can use Apache HTTP Server or Nginx. Details for setting these http server
are not provided at this step, but you can inspire you with this `article <https://www.thecodeship.com/deployment/deploy-django-apache-virtualenv-and-mod_wsgi/>`_ or
this other `one <https://docs.nginx.com/nginx/admin-guide/web-server/app-gateway-uwsgi-django/>`_

With the software, a basic solution is provided with CherryPy_ which provides the ability to have Http server and WSGI implementation. 
Use the following script to start the server already configured to start as is.
You can encapsulate the call to this script into your boot manager. This script listen on all interfaces of the host to provide the web application.
The default configured port to provide the application is 8085.
::

   ./server.py


To change the default port of the server, write a file server.cfg like this  (to set to 9000 in this example)
::

   [server]
   server.port = 9000

.. _base : Libreosteo/settings/base.py
.. _standalone : Libreosteo/settings/standalone.py
.. _CherryPy : https://cherrypy.org/

Contributing code
=================

You are more than welcome ! Please read `CONTRIBUTING.md`_ and happy hacking !

Contributors
============

The libreosteo team consist of:

  * jbgury_
  * littlejo_
  * jocelynDelalande_


.. _github : https://github.com/jbgury
.. _jbgury: https://github.com/jbgury
.. _littlejo: https://github.com/littlejo
.. _jocelynDelalande: https://github.com/JocelynDelalande 
.. _pull requests: https://github.com/libreosteo/Libreosteo/pulls
.. _CONTRIBUTING.md: CONTRIBUTING.md
