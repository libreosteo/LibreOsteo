from rest_framework import serializers
from libreosteoweb.models import Patient

class WithPkMixin(object):
    def get_pk_field(self, model_field):
        return self.get_field(model_field)


class PatientSerializer (WithPkMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Patient

