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
  - Python 2.7+ or Python 3.3+ (if you have no opinion, 2.7+ is the recommended choice for now)
  - pip 
  - virtualenv
  - nodejs and npm (if on Debian, you will need `nodesource packages`_, official ones will not work)
  - bower

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

Install bower ::

    sudo npm install -g bower

Install Javascript dependencies with bower ::

    bower install

Initialize the database ::

    python manage.py migrate
    
Now you can start the server with ::

    python manage.py runserver

Point your browser on : http://localhost:8000/ it will guide you towards creating the first admin user.

Have fun !

Contributing code
=================

You are more than welcome ! Please read `CONTRIBUTING.md`_ and happy hacking !

Contributors
============

The libreosteo team consist of:

  * jbgury_
  * littlejo_


.. _github : https://github.com/jbgury
.. _jbgury: https://github.com/jbgury
.. _littlejo: https://github.com/littlejo
.. _pull requests: https://github.com/libreosteo/Libreosteo/pulls
.. _CONTRIBUTING.md: CONTRIBUTING.md
