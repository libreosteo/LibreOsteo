
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
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)

class UniqueTogetherIgnoreCaseValidator(UniqueTogetherValidator):
    ignore_case = False

    def __init__(self, queryset, fields, message=None, ignore_case=False):
        super(UniqueTogetherIgnoreCaseValidator, self).__init__(queryset, fields, message)
        self.ignore_case = ignore_case

    def filter_queryset(self, attrs, queryset):
        """
        Filter the queryset to all instances matching the given attributes.
        """
        # If this is an update, then any unprovided field should
        # have it's value set based on the existing instance attribute.
        if self.instance is not None:
            for field_name in self.fields:
                if field_name not in attrs:
                    attrs[field_name] = getattr(self.instance, field_name)
        # Determine the filter keyword arguments and filter the queryset.
        filter_kwargs = {}
        for field_name in self.fields :
            if self.__is_str(attrs[field_name]):
                filter_kwargs[field_name+'__iexact']=attrs[field_name].lower()
            else:
                filter_kwargs[field_name]=attrs[field_name]
        return queryset.filter(**filter_kwargs)

    def __call__(self, attrs):
        self.enforce_required_fields(attrs)
        queryset = self.queryset
        queryset = self.filter_queryset(attrs, queryset)
        queryset = self.exclude_current_instance(attrs, queryset)

        # Ignore validation if any field is None
        checked_values = [
            value.lower() if (self.__is_str(value)) else value for field, value in attrs.items() if field in self.fields
        ]


        if None not in checked_values and queryset.exists():
            field_names = ', '.join(self.fields)
            raise ValidationError(self.message.format(field_names=field_names))

    def __is_str(self, value):
        is_str = type(value) is str
        try :
            is_str = is_str or type(value) is unicode
        except NameError:
            pass
        return is_str
