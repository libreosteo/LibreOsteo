============
 LibreOsteo
============

&copy; Jean-Baptiste Gury (garthylou) 2014-2016

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
  - Python 2.7+ or Python 3.3+
  - pip 
  - nodejs
  - bower

Retrieve the content of the project from Git repository.

Then retrieve the python 2 requirements with ::

    pip install -r requirements/requ-py2.txt

or python 3 ::

    pip install -r requirements/requirements.txt

Install Javascript dependencies with bower ::

    bower install

Initialize the database ::

    python manage.py migrate
    
It should ask for the administrator user.

Now you can start the server with ::

python manage.py runserver

Point your browser on : http://localhost:8000/

You can add other user from the admin console : http://localhost:8000

Have fun !

Contributors
============

The libreosteo team consist of:

  * jbgury_
  * littlejo_


.. _github : https://github.com/garthylou
.. _jbgury: https://github.com/jbgury
.. _littlejo: https://github.com/littlejo
