
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

