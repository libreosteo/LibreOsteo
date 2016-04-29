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
            if type(attrs[field_name]) is str or type(attrs[field_name]) is unicode:
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
            value.lower() if (type(value) is str or type(value) is unicode) else value for field, value in attrs.items() if field in self.fields
        ]


        if None not in checked_values and queryset.exists():
            field_names = ', '.join(self.fields)
            raise ValidationError(self.message.format(field_names=field_names))