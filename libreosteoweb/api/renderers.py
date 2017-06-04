from rest_framework_csv import renderers
class PatientCSVRenderer(renderers.CSVRenderer):
	header = ['family_name', 'original_name', 'first_name', 'birth_date', 'sex',
	'address_street', 'address_complement', 'address_zipcode', 'address_city', 'email', 'phone', 'mobile_phone',
	'job', 'hobbies', 'smoker', 'laterality', 'important_info', 'current_treatment', 'surgical_history',
	'medical_history', 'family_history', 'trauma_history','medical_report']

class ExaminationCSVRenderer(renderers.CSVRenderer):
	header = ['patient_detail.first_name', 'patient_detail.family_name', 'patient_detail.birth_date', 'date', 'reason', 'reason_description', 'orl', 'visceral', 
	'pulmo', 'uro_gyneco', 'periphery', 'general_state', 'medical_examination', 'diagnosis', 'treatments', 'conclusion','therapeut_detail.first_name', 'therapeut_detail.last_name']
