
# This file is part of Libreosteo.
#
# Libreosteo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Libreosteo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Libreosteo.  If not, see <http://www.gnu.org/licenses/>.
# Monkey Patch for django translation from 1.8 version
# when frozen on application.

import sys, os

import logging

logger = logging.getLogger("patch")

if getattr(sys, 'frozen', False):

    from django.utils.translation.trans_real import DjangoTranslation
    DATA_FOLDER = os.path.dirname(sys.executable)
    from django.conf import settings

    def new_init_translation_catalog(self):
        """Creates a base catalog using global django translations."""
        localedir = os.path.join(os.path.join(os.path.join(DATA_FOLDER, 'django'), 'conf'), 'locale')
        use_null_fallback = True
        if self.language() == settings.LANGUAGE_CODE:
            # default lang should be present and parseable, if not
            # gettext will raise an IOError (refs #18192).
            use_null_fallback = False
        translation = self._new_gnu_trans(localedir, use_null_fallback)
        self.plural = translation.plural
        self._info = translation._info.copy()
        self._catalog = translation._catalog.copy()

    original_init_translation_catalog = DjangoTranslation._init_translation_catalog
    DjangoTranslation._init_translation_catalog = new_init_translation_catalog

def wr_long(f, x):
    f.write(bytes([x & 0xff, (x >> 8) & 0xff,
        (x >> 16) & 0xff,
        (x >> 24) & 0xff ]))

def patch_file(module_name, file_name, patch_function, path_prefix):
    import pkgutil
    import imp
    import time
    import marshal
    import glob, struct
    import builtins
    import importlib
    loader = pkgutil.get_loader(module_name)
    loader_file = glob.glob(path_prefix + file_name)[0]
    if sys.version_info.major >= 3 :
        source = patch_function(loader.get_source(module_name))
        source_stats = loader.path_stats(loader.path)
        code = loader.source_to_code(source, '<string>')
        bytecode = importlib._bootstrap_external._code_to_bytecode(code,
                source_stats['mtime'], source_stats['size'])
        importlib._bootstrap_external._write_atomic(loader_file, bytecode)
    else :
        code = compile(patch_function(loader.get_source()), "<string>", "<exec>")
        timestamp = time.time()
        try :
            f = open(loader_file, 'wb')
            f.write(b'\0\0\0\0')
            wr_long(f, timestamp)
            marshal.dump(code, f)
            f.flush()
            f.seek(0, 0)
            f.write(imp.get_magic())
            f.close()
        except IOError:
            print("Cannot patch file %s" % file_name)


def patch_django_loader_pyc(path_prefix):
    patch_file('django.db.migrations.loader', 'lib/django/db/migrations/loader.pyc', lambda src : src.replace('".py"', '".pyc"'),
          path_prefix) 
    
