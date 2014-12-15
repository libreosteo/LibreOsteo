from rest_framework import serializers
from libreosteoweb.models import Patient, Examination
from django.contrib.auth.models import User


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


