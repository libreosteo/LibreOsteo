
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
from django.template.base import Origin


from django.template.loaders.base import Loader as BaseLoader



class Loader(BaseLoader):
    
    def __init(self, engine) :
        self.templates_dict = {}
        super().__init__(engine)

    def get_contents(self, origin) :
        try :
            return self.templates_dict[origin.name]._content
        except KeyError:
            raise TemplateDoesNotExist(origin)


    def get_template_sources(self, template_name, template_dirs=None):
        "Template loader that loads templates from a ZIP file."

        template_zipfiles = getattr(settings, "TEMPLATE_ZIP_FILES", ['library.zip'])

        try :
            yield self.templates_dict[template_name]._origin
        except KeyError:
            # Try each ZIP file in TEMPLATE_ZIP_FILES.
            for fname in template_zipfiles:
                try:
                    z = zipfile.ZipFile(fname)
                    source = z.read('templates/%s' % (template_name))
                except (IOError, KeyError):
                    continue
                z.close()
                origin = Origin(name=template_name, template_name=template_name, loader=self)
                self.templates_dict[template_name]= EntryLoaderCache(origin=origin, content=source)
                yield origin

class EntryLoaderCache:

    def __init__(self, origin, content):
        self._origin = origin
        self._content = content
