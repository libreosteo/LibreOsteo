============
 LibreOsteo
============

.. image:: https://github.com/libreosteo/LibreOsteo/actions/workflows/main.yml/badge.svg?branch=develop
   :alt: ci-status-develop

© Jean-Baptiste Gury 2014-2021

© The LibreOsteo Development Team 2014-2021

*LibreOsteo*

LibreOsteo is a business application designed for osteopaths.

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
  - Python 3.6+
  - pip
  - nodejs
  - yarn
  - virtualenv
  - nodejs
  - if on linux system, you need linux-headers package.

Install system dependencies, for example, on Debian-like sytem, that would be ::

    sudo apt install python3-pip python3-venv nodejs linux-headers-$(uname -r) curl git

For yarnpkg, the last version contains a bug with one of dependency (see https://github.com/yarnpkg/yarn/issues/7890 ).
Install yarnpkg by a manual installation of explicit version ::

  curl -o- -L https://yarnpkg.com/install.sh | bash -s -- --version 1.21.1

Retrieve the content of the project from Git repository ::

    git clone https://github.com/libreosteo/LibreOsteo.git

Enter the cloned folder ::

    cd LibreOsteo

Create a virtualenv ::

  python3 -m venv venv

Then retrieve the python requirements ::

    ./venv/bin/pip install -r requirements/requirements.txt

Install Javascript dependencies ::

    yarn

Initialize the database ::

    ./venv/bin/python manage.py migrate

Fetch the french postcodes for zipcode completion ::

   ./venv/bin/python manage.py import_zipcodes

Now you can start the server with ::

    ./venv/bin/python manage.py runserver

Point your browser on : http://localhost:8000/ it will guide you towards creating the first admin user.

Have fun !

With Docker
===========

- Copy this repository in your local environment.
- Ensure you have docker installed on your machine ::

    make build
    make run

Point your browser on : http://localhost:8085/ it will guide you towards creating the first admin user.

- To use PostgreSQL with your Docker container, you have to define into your .env file these values ::

    LIBREOSTEO_DB_STORAGE=volumes/libreosteo-db-storage
    DATA=volumes/data
    SETTINGS=settings
    LIBREOSTEO_BAK_STORAGE=volumes/libreosteo-backup
    POSTGRES_USER=libreosteo
    POSTGRES_PASSWORD=libreosteo

Then ::

    make run-pg

- LIBREOSTEO_DB_STORAGE define the postgresql storage
- DATA define the volume where the data will be stored : index of the database and uploaded documents
- SETTINGS define the directory which contains settings into __init__.py file
- LIBREOSTEO_BAK_STORAGE define the volume where you can backup your database in PostgreSQL dump format.
- POSTGRES_USER and POSTGRES_PASSWORD defines the credential required for your PostgreSQL database


into your __init__.py file for settings you can have ::

  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'libreosteo',
        'USER': 'PUT_YOUR_POSTGRES_USER_HERE',
        'PASSWORD': 'PUT_YOUR_POSTGRES_PASSWORD_HERE',
        'HOST': 'pg_1',
        'PORT': '5432',
    }
  }

Use it in production
====================
You can use the software in production by changing some settings.

Settings are in the folder
::

   LibreOsteo/settings/

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

Docker images are provided with uwsgi as provider of the webapp. Libreosteo-sock provides an execution on uwsgi with serving on sock and allow to bind with NGinx for distributing the app.

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

.. _base : LibreOsteo/settings/base.py
.. _standalone : LibreOsteo/settings/standalone.py
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
.. _pull requests: https://github.com/libreosteo/LibreOsteo/pulls
.. _CONTRIBUTING.md: CONTRIBUTING.md
