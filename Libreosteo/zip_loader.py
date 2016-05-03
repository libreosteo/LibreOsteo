import os
from django.conf import settings
from django.template import TemplateDoesNotExist
import zipfile


from django.template.loaders.base import Loader as BaseLoader



class Loader(BaseLoader):
    is_usable = True

    def load_template_source(self, template_name, template_dirs=None):
        "Template loader that loads templates from a ZIP file."

        template_zipfiles = getattr(settings, "TEMPLATE_ZIP_FILES", ['library.zip'])

        # Try each ZIP file in TEMPLATE_ZIP_FILES.
        for fname in template_zipfiles:
            try:
                z = zipfile.ZipFile(fname)
                source = z.read('templates/%s' % (template_name))
            except (IOError, KeyError):
                continue
            z.close()
            # We found a template, so return the source.
            template_path = "%s:%s" % (fname, template_name)
            return (source, template_path)

        # If we reach here, the template couldn't be loaded
        raise TemplateDoesNotExist(template_name)

