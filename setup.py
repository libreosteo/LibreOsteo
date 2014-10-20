import sys, glob
from cx_Freeze import setup, Executable

# GUI applications require a different base on Windows (the default is for a
# console application).
base=None

import os

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


# Build on Windows.
if sys.platform in ['win32']:
    from cx_Freeze import setup, Executable
    copyDependentFiles = True
    includes = [
        'django.template.loader_tags',
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
        'libreosteoweb.migrations',
        'email.mime.image',
    ]
    include_files = get_filepaths('static') + get_filepaths('locale')
    zip_includes = get_filepaths('templates')
    packages = [
        "os",
        "django",
        "htmlentitydefs",
        "HTMLParser",
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
        "optimize" : 2,
    }

setup(  name = "libreosteo",
        version = "0.1",
        description = "Libreosteo, suite for osteopaths",
        options = {"build_exe": build_exe_options},
        executables = [Executable("server.py", base=base,targetName="Libreosteo.exe"),
                       Executable("manage.py", base=base)])
