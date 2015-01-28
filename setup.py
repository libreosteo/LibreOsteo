import sys, glob
from cx_Freeze import setup, Executable

# GUI applications require a different base on Windows (the default is for a
# console application).
base=None

import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name = "Libreosteo",
    version = "0.1",
    author = "Jean-Baptiste Gury",
    author_email = "libreosteo@gmail.com",
    description = ("Software suite for osteopaths"),
    license = "GNU/GPL v3",
    keywords = "osteopathy software patient manager",
    url = "http://libreosteo.olympe.in/",
    packages=['Libreosteo', 'libreosteoweb'],
    long_description=read('README.rst'),
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU License",
    ],
    install_requires=[
    'django',
    'whoosh',
    'django-angular',
    'django-haystack',
    'django-statici18n',
    'djangorestframework',
    'cherrypy',]
)


# Build on Windows.
if sys.platform in ['win32']:

    def get_djangolocale():
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Libreosteo.settings")
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
                if (filename.endswith('.py')):
                    migration_files.append(directory.replace('/', '.') + filename[0:len(filename)-3])
        return migration_files

    from cx_Freeze import setup, Executable
    copyDependentFiles = True
    includes = [
        'django.template.loader_tags',
        'django.core.management',
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
        'email.mime.image',
        "django.contrib.admin.migrations.0001_initial",
        "django.contrib.auth.migrations.0001_initial",
        "django.contrib.contenttypes.migrations.0001_initial",
        "django.contrib.sessions.migrations.0001_initial",
    ] + include_migration_files('libreosteoweb/migrations')
    
    include_files = get_filepaths('static') + get_filepaths('locale') +get_djangolocale()
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
        version = "0.1",
        description = "Libreosteo, suite for osteopaths",
        options = {"build_exe": build_exe_options},
        executables = [Executable("server.py", base=base,targetName="Libreosteo.exe"),
                       Executable("manager.py", base=base)])

    # Remove init.py into locale directory
    # Create a web shorcut link
    shortlink = open("build/exe.win32-2.7/Libreosteo.url","w")
    shortlink.write("[InternetShortcut]\n")
    shortlink.write("URL=http://localhost/\n")
    shortlink.write("\n")
    shortlink.write("\n")
