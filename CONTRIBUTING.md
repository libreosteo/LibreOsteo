Contributing code to Libreosteo
===============================

Libreosteo is using AngularJS + Django. You can contribute to it via `pull
requests`_ .

**Please target the** ``develop`` **branch with your pull requests**
(``master`` points to the latest release).

Internationalization
====================

Libreosteo code and strings are written in *English*
Language. Internationalization is used to provide a full translation in
French. If you need it in another language, please contribute your translations
:-).

Django side
-----------

We are using
[standard Django gettext-based stuff](https://docs.djangoproject.com/en/2.0/topics/i18n/translation/).
In a nutshell:

1. Wrap your string with gettext markers:
  - `_('my string')` in *.py* files
  - `{% trans 'my string' %}` in *.html* files

2. Collect new marked strings for translations into *django.po*:
```
./manage.py makemessages --no-location
```
3. Translate new strings by editing *django.po*
4. Compile them to `.mo files`. with:
```
./manage.py compilemessages
```

Please **do commit** your updated `.mo`.

AngularJS side
------------

*angular-i18n* is **not** used. Instead, we use
Django
[JS-dedicated mechanisms](https://docs.djangoproject.com/en/2.0/topics/i18n/translation/#internationalization-in-javascript-code). So:

1. Wrap your strings with gettext markers:
   - `gettext('my string')` in *.js* files
   - problem is not solved yet for *.html* (feel free to suggest a solution)
2. Collect new marked strings for translations into *djangojs.po*:
```
./manage.py makemessages --no-location -d djangojs
```
3. Translate new strings by editing *djangojs.po*
4. Compile them to `.mo files`. with:
```
./manage.py compilemessages
```

Please **do commit** your updated `.mo`.


Testing
=======

Testing is a full subject. There is lot of lack into the project to covert all the code. But some actions are in progress to raise the coverage.
When developing a new functionality, the requirement is to add some tests (unit tests is mandatory), but also Functional Tests to demonstrate the functionality.
Even if first functionalities were not developed with a lack of tests, nothing is to late to change it !

1. Write the unit test for REST Api see [Django Rest Framework Testing](http://www.django-rest-framework.org/api-guide/testing/)
2. Write the functional test to ensure that the UI behaviors is the right expected see [Robotframework](http://robotframework.org/)

Running unit tests
------------------

You have to run tests before developing any functionality. To run theses tests:
```
./manage.py test
```

Running functional tests
------------------------

1. Ensure you have all requirements :
```
pip install -r requirements/requ-testing.txt
```

1. Ensure you have Firefox with French support language. You can download it with an url like https://download.mozilla.org/?product=firefox-latest&lang=fr&os=linux64

2. Download and install geckodriver into your PATH:
```
wget https://github.com/mozilla/geckodriver/releases/download/v0.21.0/geckodriver-v0.21.0-linux64.tar.gz -O /tmp/geckodriver.tar.gz
tar -xvf /tmp/geckodriver.tar.gz
export PATH=$PATH:$PWD
```

3. Be sure that your static are up to date:
```
./manage.py collectstatic --no-input
```

4. Launch the server instance:
```
  python ./server.py
```

5. Execute tests suite:
```
  robot tests
```
