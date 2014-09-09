from rest_framework import serializers
from libreosteoweb.models import Patient, Examination

class WithPkMixin(object):
    def get_pk_field(self, model_field):
        return self.get_field(model_field)


class PatientSerializer (WithPkMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Patient

class ExaminationSerializer(WithPkMixin, serializers.ModelSerializer):
    class Meta:
        model = Examination
        fields = ('id', 'reason', 'date', 'status', 'therapeut')


