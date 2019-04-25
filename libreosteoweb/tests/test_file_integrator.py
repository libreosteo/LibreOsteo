
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
# -*- coding: utf-8 -*-
from django.test import TestCase
from libreosteoweb.api import file_integrator
try:
    from unittest.mock import mock_open
    from unittest.mock import patch
    from unittest.mock import MagicMock
    from unittest.mock import Mock
except ImportError:
    from mock import mock_open
    from mock import patch
    from mock import MagicMock
    from mock import Mock


class TestFileIntegrator(TestCase):
	def setUp(self):
		self.patcher = patch('libreosteoweb.api.file_integrator.open', mock_open(), create=True)
		self.patcher.start()

	def test_filecontentkey(self):
		f = 'file'
		t = 'test'
		key1 = file_integrator.FileContentKey(f, None)
		key2 = file_integrator.FileContentKey(f, None)

		key3 = file_integrator.FileContentKey(t, None)
		self.assertTrue(key1 == key2)
		self.assertFalse(key1 == key3)

	def test_file_content_proxy(self):
		f = MagicMock()
		f.read.return_value = 'Nom;Prenom;Nom de Famille;'
		proxy1 = file_integrator.FileContentProxy()
		proxy2 = file_integrator.FileContentProxy()

		c1 = proxy1.get_content(f)
		c2 = proxy2.get_content(f)

		self.assertTrue(c1 == c2)

		f.close()

	def test_file_content_proxy_not_the_same(self):
		f = MagicMock()
		f.read.return_value = 'Nom;Prenom;Nom de Famille;'
		f.__iter__.return_value = ['Nom;Prenom;Nom de Famille;',]

		f2 = MagicMock()
		f2.read.return_value = 'Nom de famille;Prenom'
		f2.__iter__.return_value = ['Nom de famille;Prenom',]
		
		proxy1 = file_integrator.FileContentProxy()
		proxy2 = file_integrator.FileContentProxy()

		c1 = proxy1.get_content(f)
		c2 = proxy2.get_content(f2)

		self.assertTrue(c1 != c2)


	def test_analyzertype(self):
		content = {}
		content['header'] = ['nom de famille', 'prenom', 'date de naissance']
		content['nb_row'] = 1
		content['content'] = ['test','test','test']

		a = file_integrator.AnalyzerPatientFile(content)
		self.assertTrue(a.is_instance())

	def test_analyze_handler(self):
                handler = file_integrator.AnalyzerHandler()
                header = u'Numero;Nom de Famille;Nom de jeune fille ou jeune homme;Prenom;Date de naissance (JJ MM AAAA);Sex (M F);Rue;Complement dadresse;code postal;ville;email;Telephone;Mobile;Profession;Loisirs;Fumeur (O/N);Lateralite;Informations importantes;Traitement en cours;Antecedents chirurgicaux;Antecedents medicaux;Antecedents familiaux;Antecedents traumatiques;CR medicaux'
                f = MagicMock()
                f.read.return_value = header
                f.__iter__.return_value = [header,]
                report = handler.analyze(f)
                self.assertTrue(report.is_empty)
                self.assertTrue(report.is_valid)
                self.assertEquals(file_integrator.FileCsvType.PATIENT, report.type)

	def test_analyze_handler_not_empty(self):
		handler = file_integrator.AnalyzerHandler()

		header = u'Numero;Nom de Famille;Nom de jeune fille/ou jeune homme;Prenom;Date de naissance (JJ/MM/AAAA);Sex (M/F);Rue;Complement dadresse;code postal;ville;email;Telephone;Mobile;Profession;Loisirs;Fumeur (O/N);Lateralite;Informations importantes;Traitement en cours;Antecedents chirurgicaux;Antecedents medicaux;Antecedents familiaux;Antecedents traumatiques;CR medicaux'
		value = u'Test;Test;Test'

		f = MagicMock()
		f.read.return_value = header
		f.__iter__.return_value = [header, value]

		report = handler.analyze(f)
		#self.assertFalse(report.is_empty)
		self.assertTrue(report.is_valid)
		self.assertEquals(file_integrator.FileCsvType.PATIENT, report.type)


	def test_file_content_adapter(self):
		header = 'Nom;Prenom;Nom de Famille'

		f = MagicMock()
		f.read.return_value = header
		f.__iter__.return_value = (header,)

		adapter = file_integrator.FileContentAdapter(f)
		result = adapter.get_content()
		self.assertEquals(1, result['nb_row'])
		self.assertEquals(['Nom', 'Prenom', 'Nom de Famille'], result['header'])
		self.assertEquals([], result['content'])


	def tearDown(self):
		self.patcher.stop()


