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

