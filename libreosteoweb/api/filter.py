

def get_name_filters():
	filterChain = FilterManager()
	filterChain.add(CapitalizeNameFilter())
	filterChain.add(CapitalizeComposedNameFilter())
	return filterChain

class FilterException(Exception):
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return repr(self.value)

class FilterManager(object):
	def __init__(self):
		self._chain = None

	def add(self, filter):
		if self._chain is None:
			self._chain = filter
		else :
			self._chain.get_last().set_next(filter)

	def filter(self, text=None):
		if text and self._chain:
			return self._chain.filter(text)
		return text



class AbstractFilter(object):
	def __init__(self, next=None):
		self._next = next
	def set_next(self, filter=None):
		self._next = filter
	def next(self):
		return self._next
	def get_last(self):
		last = self
		while last.next() is not None:
			last = last.next()
		return last
	def filter(self, text=None):
		if self.next() is not None:
			return self.next().filter(text)
		else :
			return text


class CapitalizeNameFilter(AbstractFilter):
	def __init__(self, next=None):
		super(CapitalizeNameFilter, self).__init__(next)

	def filter(self, text=None):
		filtered_text = super(CapitalizeNameFilter, self).filter(text)
		if filtered_text:
			text_list = filtered_text.split(' ')
			return '-'.join([self._capitalize_word(t) for t in text_list])
		return filtered_text
			
	def _capitalize_word(self, word=None):
		if word and len(word) > 0:
			return word[0].upper() + word[1:]
		return word

class CapitalizeComposedNameFilter(CapitalizeNameFilter):
	def __init__(self, next=None):
		super(CapitalizeComposedNameFilter, self).__init__(next)

	def filter(self, text=None):
		filtered_text = super(CapitalizeComposedNameFilter, self).filter(text)
		if filtered_text:
			text_list = filtered_text.split('-')
			return '-'.join([self._capitalize_word(t) for t in text_list])
		return filtered_text
