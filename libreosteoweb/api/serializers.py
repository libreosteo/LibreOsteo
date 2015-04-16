from rest_framework import serializers
from libreosteoweb.models import Patient, Examination, OfficeEvent, TherapeutSettings, OfficeSettings, ExaminationComment
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
    comments = serializers.SerializerMethodField('get_nb_comments')
    class Meta:
        model = Examination
        fields = ('id', 'reason', 'date', 'status', 'therapeut', 'type', 'comments')
        depth = 1

    def get_nb_comments(self, obj):
        return ExaminationComment.objects.filter(examination__exact=obj.id).count()         


class CheckSerializer(serializers.Serializer):
    bank = serializers.CharField(required=False)
    payer = serializers.CharField(required=False)
    number = serializers.CharField(required=False)

class ExaminationInvoicingSerializer(serializers.Serializer):
    status = serializers.CharField(required=True)
    reason = serializers.CharField(required=False)
    paiment_mode = serializers.CharField(required=False)
    amount = serializers.FloatField(required=False)
    check = CheckSerializer()

    def validate(self, attrs):
        """
        Check that the invoicing is consistent
        """
        if attrs['status'] == 'notinvoiced':
            if attrs['reason'] is None or len(attrs['reason'].strip()) == 0:
                raise serializers.ValidationError(_("Reason is mandatory when the examination is not invoiced"))
        if attrs['status'] == 'invoiced':
            if attrs['amount'] is None or attrs['amount'] <= 0:
                raise serializers.ValidationError(_("Amount is invalid"))
            if attrs['paiment_mode'] is None or len(attrs['paiment_mode'].strip()) == 0 or attrs['paiment_mode'] not in ['check', 'cash', 'notpaid']:
                raise serializers.ValidationError(_("Paiment mode is mandatory when the examination is invoiced"))
            if attrs['paiment_mode'] == 'check':
                if attrs['check'] is None :
                    raise serializers.ValidationError(_("Check information is missing"))
                #if attrs['check']['bank'] is None or len(attrs['check']['bank'].strip()) == 0:
                #    raise serializers.ValidationError(_("Bank information is missing about the check paiment"))
                #if attrs['check']['payer'] is None or len(attrs['check']['payer'].strip()) == 0:
                #    raise serializers.ValidationError(_("Payer information is missing about the check paiment"))
                #if attrs['check']['number'] is None or len(attrs['check']['number'].strip()) == 0:
                #    raise serializers.ValidationError(_("Number information is missing about the check paiment"))
        return attrs


class ExaminationCommentSerializer(WithPkMixin, serializers.ModelSerializer):
    user_info = UserInfoSerializer(source="user", required=False)
    class Meta:
        model = ExaminationComment

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


class TherapeutSettingsSerializer(WithPkMixin, serializers.ModelSerializer):
    class Meta:
        model = TherapeutSettings

class OfficeSettingsSerializer(WithPkMixin, serializers.ModelSerializer):
    class Meta:
        model = OfficeSettings
