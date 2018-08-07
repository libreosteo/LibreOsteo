
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


def patch_and_generate_compiled_file():
    import pkgutil
    import imp
    import time
    import marshal
    loader = pkgutil.get_loader('django.db.migrations.loader')
    code = compile(loader.get_source().replace('".py"', '".pyc"'), "<string>", "exec")
    open('/tmp/result.pyc', 'wb')
    f.write('\0\0\0\0')
    f.write(struct.pack('<I', time.time()))
    marshal.dump(code, f)
    f.flush()
    f.seek(0, 0)
    f.write(imp.get_magic())
    f.close()
