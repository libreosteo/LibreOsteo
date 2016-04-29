from django.test import TestCase

from libreosteoweb.api.filter import get_name_filters

class TestFilter(TestCase):
	def test_initialize_filter(self):
		filter_chain = get_name_filters()
		self.assertIsNotNone(filter_chain)

	def test_capitalize(self):
		filter_chain = get_name_filters()
		text = 'test test'
		self.assertEquals('Test-Test', filter_chain.filter(text))

	def test_capitalize_none(self):
		filter_chain = get_name_filters()
		text = None 
		self.assertIsNone(filter_chain.filter(text))

	def test_capitalize_one_word(self):
		filter_chain = get_name_filters()
		text = 'test'
		self.assertEquals('Test', filter_chain.filter(text))

	def test_capitalize_nothing(self):
		filter_chain = get_name_filters()
		text = 'Test'
		self.assertEquals(text, filter_chain.filter(text))

	def test_capitalize_empty(self):
		filter_chain = get_name_filters()
		text = ''
		self.assertEquals(text, filter_chain.filter(text))

	def test_capitalize_composed_name(self):
		filter_chain = get_name_filters()
		text = 'jean-charles'
		self.assertEquals('Jean-Charles', filter_chain.filter(text))

	def test_capitalize_upper_name(self):
		filter_chain = get_name_filters()
		text = 'DUPOND'
		self.assertEquals('Dupond', filter_chain.filter(text))