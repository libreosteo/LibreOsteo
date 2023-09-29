# This file is part of LibreOsteo.
#
# LibreOsteo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# LibreOsteo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with LibreOsteo.  If not, see <http://www.gnu.org/licenses/>.
from rest_framework_csv import renderers


class PatientCSVRenderer(renderers.CSVRenderer):
    header = [
        'family_name', 'original_name', 'first_name', 'birth_date', 'sex',
        'address_street', 'address_complement', 'address_zipcode',
        'address_city', 'email', 'phone', 'mobile_phone', 'job', 'hobbies',
        'smoker', 'laterality', 'important_info', 'current_treatment',
        'surgical_history', 'medical_history', 'family_history',
        'trauma_history', 'medical_reports'
    ]


class ExaminationCSVRenderer(renderers.CSVRenderer):
    header = [
        'patient_detail.first_name', 'patient_detail.family_name',
        'patient_detail.birth_date', 'date', 'reason', 'reason_description',
        'orl', 'visceral', 'pulmo', 'uro_gyneco', 'periphery', 'general_state',
        'medical_examination', 'diagnosis', 'treatments', 'conclusion',
        'therapeut_detail.first_name', 'therapeut_detail.last_name'
    ]


class InvoiceCSVRenderer(renderers.CSVRenderer):
    labels = {
        'amount': 'montant',
        'currency': 'devise',
        'paiment_mode': 'code mode de paiement',
        'paiment_mode_text': 'mode de paiement',
        'header': 'entête',
        'therapeut_name': 'Nom du thérapeute',
        'therapeut_first_name': 'Prénom du thérapeute',
        'quality': 'En qualité de',
        'adeli': 'ADELI',
        'location': 'lieu',
        'number': 'Numéro',
        'patient_family_name': 'Nom d\'usage du patient',
        'patient_original_name': 'Nom du patient',
        'patient_first_name': 'Prénom du patient',
        'patient_address_street': 'Rue',
        'patient_address_complement': 'Complément d\'adresse',
        'patient_address_zipcode': 'Code postal',
        'patient_address_city': 'Ville',
        'content_invoice': 'contenu de facture',
        'footer': 'pied de page',
        'office_siret': 'SIRET',
        'office_address_street': 'Rue du cabinet',
        'office_address_complement': 'Complément d\'adresse',
        'office_address_city': 'Ville',
        'office_address_zipcode': 'Code postal',
        'office_phone': 'Téléphone',
        'status': 'Etat (1=En attente de paiement,2=Payé)',
        'therapeut_id': 'Identifiant interne thérapeute',
        'canceled_by': 'Annulée par',
        'replace': 'Remplacée par',
        'officesettings_id': 'Identifiant interne cabinet',
        'office_name': 'Nom d\'établissement'
    }
