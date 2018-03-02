
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
from rest_framework_csv import renderers
class PatientCSVRenderer(renderers.CSVRenderer):
    header = ['family_name', 'original_name', 'first_name', 'birth_date', 'sex',
    'address_street', 'address_complement', 'address_zipcode', 'address_city', 'email', 'phone', 'mobile_phone',
    'job', 'hobbies', 'smoker', 'laterality', 'important_info', 'current_treatment', 'surgical_history',
    'medical_history', 'family_history', 'trauma_history','medical_report']

class ExaminationCSVRenderer(renderers.CSVRenderer):
    header = ['patient_detail.first_name', 'patient_detail.family_name', 'patient_detail.birth_date', 'date', 'reason', 'reason_description', 'orl', 'visceral',
    'pulmo', 'uro_gyneco', 'periphery', 'general_state', 'medical_examination', 'diagnosis', 'treatments', 'conclusion','therapeut_detail.first_name', 'therapeut_detail.last_name']


class InvoiceCSVRenderer(renderers.CSVRenderer):
    pass
