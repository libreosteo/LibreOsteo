import sys, glob, os
import shutil
import libreosteoweb

version = libreosteoweb.__version__



# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def remove_useless_files(directory, keepfiles_list, keepdir_list):
    keep_path_list = []
    for root,directories,files in os.walk(directory):
        for d in directories :
            if d in keepdir_list or root in keep_path_list:
                keep_path_list.append(os.path.join(root,d))
        for f in files :
            if root not in keep_path_list and f not in keepfiles_list:
                os.remove(os.path.join(root,f))
        for d in directories:
            if os.path.join(root,d) not in keep_path_list:
                shutil.rmtree(os.path.join(root,d))

def collectstatic():
    from subprocess import call
    call(["python", "manage.py", "collectstatic", "--noinput"])

def compress():
    from subprocess import call
    call(["python", "manage.py", "compress", "--force"])

def purge_static():
    purge_dir = ['bower_components']
    keep_path = ['bower_components/webshim']
    to_remove_list = []
    # For each dir in purge dir from static : 
    # delete each files
    for root, directories, files in os.walk('static'):
        for p in purge_dir:
            for d in directories:
                if root == os.path.join('static', p):
                    for a in keep_path:
                        if d not in os.path.split(a):
                            shutil.rmtree(os.path.join(root,d))



                

# Build on Windows.
#
# usage :
#     python setup.py build_exe 
#
if sys.platform in ['win32']:

    # before all of things : collectstatic
    collectstatic()

    compress()

    from cx_Freeze import setup, Executable
    # GUI applications require a different base on Windows (the default is for a
    # console application).
    base='Console'
    def get_djangolocale():
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Libreosteo.settings.standalone")
        import django
        directory = os.path.join(django.__path__[0], 'conf', 'locale')
        return [(directory, 'django/conf/locale')]
    
    

    def get_filepaths(directory):
        """
        This function will generate the file names in a directory 
        tree by walking the tree either top-down or bottom-up. For each 
        directory in the tree rooted at directory top (including top itself), 
        it yields a 3-tuple (dirpath, dirnames, filenames).
        """
        file_paths = []  # List which will store all of the full filepaths.

        # Walk the tree.
        for root, directories, files in os.walk(directory):
            for filename in files:
                # Join the two strings in order to form the full filepath.
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)  # Add it to the list.

        return file_paths  # Self-explanatory.
        
    def include_migration_files(directory):
        """
        This function will generate the include from the list of python
        migration files in the directory
        """
        migration_files = [] 
        for root, directories, files in os.walk(directory):
            for filename in files :
                if (filename.endswith('.py'))  and not (filename.startswith('__')):
                    migration_files.append(directory.replace('/', '.') + '.' + filename[0:len(filename)-3])
        return migration_files                

    from cx_Freeze import setup, Executable
    copyDependentFiles = True
    includes = [
        'cherrypy',
        'win32serviceutil', 'win32service', 'win32event', 'servicemanager','win32timezone',
        'django.template.loader_tags',
        'django.core.management',
        'Libreosteo',
        'Libreosteo.urls',
        'Libreosteo.settings',
        'Libreosteo.wsgi',
        'Libreosteo.zip_loader',
        'libreosteoweb',
        'libreosteoweb.admin',
        'libreosteoweb.middleware',
        'libreosteoweb.models',
        'libreosteoweb.search_indexes',
        'libreosteoweb.api',
        'libreosteoweb.apps',
        'libreosteoweb.templatetags.invoice_extras',
        'email.mime.image',
        "django.contrib.admin.migrations.0001_initial",
        "django.contrib.auth.migrations.0001_initial",
        "django.contrib.auth.migrations.0002_alter_permission_name_max_length",
        "django.contrib.auth.migrations.0003_alter_user_email_max_length",
        "django.contrib.auth.migrations.0004_alter_user_username_opts",
        "django.contrib.auth.migrations.0005_alter_user_last_login_null",
        "django.contrib.auth.migrations.0006_require_contenttypes_0002",
        "django.contrib.contenttypes.migrations.0001_initial",
        "django.contrib.contenttypes.migrations.0002_remove_content_type_name",
        "django.contrib.sessions.migrations.0001_initial",
    ] + include_migration_files('libreosteoweb/migrations')
    
    include_files = get_filepaths('static') + get_filepaths('locale') + get_djangolocale() + get_filepaths('media')
    zip_includes = get_filepaths('templates')
    packages = [
        "os",
        "django",
        "htmlentitydefs",
        "HTMLParser",
        "Cookie",
        "rest_framework",
        "haystack",
        "sqlite3",
        "statici18n",
        "email",
        "Libreosteo",
        
        
    ]
    build_exe_options = {
        "packages": packages,
        "includes": includes,
        "include_files": include_files,
        "zip_includes" : zip_includes,
        "excludes" : ['cStringIO','tcl','Tkinter'],
        "compressed" : True,
        "create_shared_zip": True,
        "append_script_to_exe": True,
        "include_in_shared_zip" : True,
        "optimize" : 2,
        "include_msvcr" : True,
    }

    setup(  name = "libreosteo",
        version = version,
        description = "Libreosteo, suite for osteopaths",
        options = {"build_exe": build_exe_options},
        executables = [Executable("winserver.py", base=base,targetName="Libreosteo.exe"),
                       Executable("manager.py", base=base)])


    # Create a web shorcut link
    shortlink = open("build/exe.win32-2.7/Libreosteo.url","w")
    shortlink.write("[InternetShortcut]\n")
    shortlink.write("URL=http://localhost:8085/\n")
    shortlink.write("\n")
    shortlink.write("\n")

    ##Remove useless locales
    remove_useless_files("build/exe.win32-2.7/django/conf/locale", [], ["fr","en"])
    remove_useless_files("build/exe.win32-2.7/static/bower_components/angular-i18n", ["angular-locale_en.js", "angular-locale_en-us.js", "angular-locale_fr.js", "angular-locale_fr-fr.js"], [])











#### MACOS X build
#
# Usage:
#        python setup.py py2app

if sys.platform in ['darwin']:
    from setuptools import setup

    # before all of things : collectstatic
    collectstatic()

    compress()

    APP = ['application.py']

    DATA_FILES = ['static', 'locale','templates', 'macos', 'media']

    OPTIONS = {'argv_emulation': True,
        'includes' : [
            'HTMLParser',
        ],
        'packages' : ["django","Libreosteo", "libreosteoweb","rest_framework",
            "haystack","sqlite3","statici18n", "email"
        ],
        'plist' : {
            'LSBackgroundOnly' : True,
            'CFBundleIdentifier' : 'org.libreosteo.macos.libreosteo',
            'CFBundleGetInfoString' : 'Libreosteo',
            'CFBundleDisplayName' : 'Libreosteo',
            'CFBundleName' : 'Libreosteo',
            'CFBundleShortVersionString' : version,
            'CFBundleVersion' : version,
        },
        'extra_scripts': ['server.py','manage.py'],
        'optimize' : True,
        'iconfile' : 'libreosteoweb/static/images/favicon.icns',
    }
    setup(
        app=APP,
        data_files=DATA_FILES,
        options={'py2app': OPTIONS},
        setup_requires=['py2app'],
    )
    remove_useless_files("build/exe.win32-2.7/static/bower_components/angular-i18n", ["angular-locale_en.js", "angular-locale_en-us.js", "angular-locale_fr.js", "angular-locale_fr-fr.js"], [])
else:
    from setuptools import setup

    collectstatic()

    compress()
    purge_static()

    setup(
        name='Libreosteo',
        version=version,
        description='Open source software and free software for osteopaths',
        author='Jean-Baptiste Gury',
        url='https://libreosteo.github.io',
        packages=['Libreosteo','libreosteoweb'],
        )

