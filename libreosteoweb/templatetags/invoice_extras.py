#Invoice Extras filter
from django import template
from django.utils.translation import to_locale, get_language
import locale

register = template.Library()

import re



@register.filter(name='templatize')
def templatize(value, obj):
	"""
	Replace all tag in the value by the field of the given object
	"""
	def replace(match):
		val = match.groups()[0]
		if val is not None :
			todisplay = getattr(obj, val)
			if type(todisplay) is float :
				locale_desc = to_locale(get_language())
				return unicode(locale.str(todisplay))
			else :
				return unicode(getattr(obj, val))
		return val
	p = re.compile(r'<(?P<tag>.*?)>')
	return p.sub(replace, value)

