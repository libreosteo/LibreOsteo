
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
from django.test import TestCase

from libreosteoweb.api.filter import get_firstname_filters, get_name_filters

class TestFilter(TestCase):
	def test_initialize_filter(self):
		filter_chain = get_firstname_filters()
		self.assertIsNotNone(filter_chain)

	def test_capitalize(self):
		filter_chain = get_firstname_filters()
		text = 'test test'
		self.assertEquals('Test-Test', filter_chain.filter(text))

	def test_capitalize_none(self):
		filter_chain = get_firstname_filters()
		text = None 
		self.assertIsNone(filter_chain.filter(text))

	def test_capitalize_one_word(self):
		filter_chain = get_firstname_filters()
		text = 'test'
		self.assertEquals('Test', filter_chain.filter(text))

	def test_capitalize_nothing(self):
		filter_chain = get_firstname_filters()
		text = 'Test'
		self.assertEquals(text, filter_chain.filter(text))

	def test_capitalize_empty(self):
		filter_chain = get_firstname_filters()
		text = ''
		self.assertEquals(text, filter_chain.filter(text))

	def test_capitalize_composed_name(self):
		filter_chain = get_firstname_filters()
		text = 'jean-charles'
		self.assertEquals('Jean-Charles', filter_chain.filter(text))

	def test_capitalize_upper_name(self):
		filter_chain = get_firstname_filters()
		text = 'DUPOND'
		self.assertEquals('Dupond', filter_chain.filter(text))

	def test_capitalize_name(self):
		filter_chain = get_name_filters()
		text = "de Moustier"
		self.assertEquals('De Moustier', filter_chain.filter(text))
