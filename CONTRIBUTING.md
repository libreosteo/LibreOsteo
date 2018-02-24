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
