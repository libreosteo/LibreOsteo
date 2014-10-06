============
 LibreOsteo
============

(C) Jean-Baptiste Gury (garthylou) 2014

*LibreOsteo*

Libreosteo is a business application designed for osteopaths.

It manages patients, folder and runs as a work portal on a folder patient.

Contact
=======

Problems or questions contact me at github_

HOW-TO try it ?
===============

Requirements :
  - Python 2.7+ or Python 3.3+
  - pip installed
  - nodejs and bower installed

Retrieve the content of the project from Git repository.

Then retrieve the python requierements with ::

    pip install -r requirements.txt

Install Javascript dependencies with bower ::

    bower install

Initialize the database ::

    python manage.py syncdb
    
It should ask for the administrateur user.

Compile the translations ::

    python manage.py compilemessages

Now you can start the server with ::

python manage.py runserver

Point your browser on : http://localhost:8000/

You can add other user from the admin console : http://localhost:8000/admin

Have fun !

Contributors
============

The libreosteo team consist of:

  * garthylou_


.. _github : https://github.com/garthylou
.. _garthylou: https://github.com/garthylou
