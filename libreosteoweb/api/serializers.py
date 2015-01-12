from rest_framework import serializers
from libreosteoweb.models import Patient, Examination, OfficeEvent
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class WithPkMixin(object):
    def get_pk_field(self, model_field):
        return self.get_field(model_field)


class PatientSerializer (WithPkMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Patient
    

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta :
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


    #def restore_object(self, attrs, instance=None):
        # call set_password on user object. Without this
        # the password will be stored in plain text.
        #user = super(UserSerializer, self).restore_object(attrs, instance)
        #if(attrs['password']):
        #    user.set_password(attrs['password'])
        #return user

class ExaminationSerializer(WithPkMixin, serializers.ModelSerializer):
    therapeut = UserInfoSerializer(source = 'therapeut')
    class Meta:
        model = Examination
        fields = ('id', 'reason', 'date', 'status', 'therapeut', 'type')
        depth = 1


class ExaminationInvoicingSerializer(serializers.Serializer):
    reason = serializers.CharField(required=False)
    paiment_mode = serializers.IntegerField(required=False)


class OfficeEventSerializer(WithPkMixin, serializers.ModelSerializer):

    class Meta:
        model = OfficeEvent

    patient_name = serializers.SerializerMethodField('get_patient_name')
    translated_comment = serializers.SerializerMethodField('get_translated_comment')
    therapeut_name = UserInfoSerializer(source = 'user')

    def get_patient_name(self, obj):
        if (obj.clazz == "Patient"):
            patient = Patient.objects.get(id = obj.reference)
            return "%s %s" % (patient.family_name, patient.first_name)
        if (obj.clazz == "Examination"):
            examination = Examination.objects.get(id=obj.reference)
            patient = examination.patient
            return "%s %s" % (patient.family_name, patient.first_name)
        return ""

    def get_translated_comment(self, obj):
        return _(obj.comment)


