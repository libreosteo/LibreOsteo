from haystack import indexes
from libreosteoweb import models

class PatientIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    family_name = indexes.CharField(model_attr='family_name')
    original_name = indexes.CharField(model_attr='original_name')
    first_name = indexes.CharField(model_attr='first_name')
    #birth_date = indexes.DateField(model_attr='birth_date')
    address_street = indexes.CharField(model_attr='address_street')
    address_complement = indexes.CharField(model_attr='address_complement')
    address_zipcode = indexes.CharField(model_attr='address_zipcode')
    address_city = indexes.CharField(model_attr='address_city')
    phone = indexes.CharField(model_attr='phone')
    mobile_phone = indexes.CharField(model_attr='mobile_phone')
    doctor = indexes.CharField(model_attr='doctor', null=True)
    #family_situation = Column(Integer)
    smoker = indexes.BooleanField(model_attr='smoker')
    important_info = indexes.CharField(model_attr='important_info')
    current_treatment = indexes.CharField(model_attr='current_treatment')
    surgical_history = indexes.CharField(model_attr='surgical_history')
    medical_history = indexes.CharField(model_attr='medical_history')
    family_history = indexes.CharField(model_attr='family_history')
    trauma_history = indexes.CharField(model_attr='trauma_history')
    medical_reports = indexes.CharField(model_attr='medical_reports')


    def get_model(self):
        return models.Patient

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects

class DocumentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    notes = indexes.CharField(model_attr='notes', null=True)
    date = indexes.CharField(model_attr='date',null=True)

    def get_model(self):
        return models.Document

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects

