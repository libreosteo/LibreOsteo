from rest_framework import serializers
from libreosteoweb.models import Patient, Examination
from django.contrib.auth.models import User

class WithPkMixin(object):
    def get_pk_field(self, model_field):
        return self.get_field(model_field)


class PatientSerializer (WithPkMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Patient

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username')

class ExaminationSerializer(WithPkMixin, serializers.ModelSerializer):
    therapeut = UserSerializer(source = 'therapeut')
    class Meta:
        model = Examination
        fields = ('id', 'reason', 'date', 'status', 'therapeut', 'type')
        depth = 1



