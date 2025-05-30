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
from rest_framework import serializers
from libreosteoweb.models import *
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from datetime import date
from django.utils import timezone
from .validators import UniqueTogetherIgnoreCaseValidator
from .filter import get_name_filters, get_firstname_filters
from django.core.exceptions import ObjectDoesNotExist
from .file_integrator import Extractor
import logging
from django.conf import settings
from .utils import NetworkHelper
from django.db.models import Max
from .utils import convert_to_long
from django.utils.dateparse import parse_datetime
from libreosteoweb.api.utils import _unicode
from libreosteoweb.api.demonstration import get_demonstration_file
import re
import pytz

logger = logging.getLogger(__name__)


class WithPkMixin(object):

    def get_pk_field(self, model_field):
        return self.get_field(model_field)


def check_birth_date(value):
    if value > date.today():
        raise serializers.ValidationError(
            {'birth_date': _('Birth date is invalid')})


class PatientSerializer(serializers.ModelSerializer):
    current_user_operation = None
    birth_date = serializers.DateField(label=_('Birth date'),
                                       validators=[check_birth_date])
    consent_check = serializers.BooleanField(label=_('Consent'), default=False)

    def validate_family_name(self, value):
        return get_name_filters().filter(value)

    def validate_first_name(self, value):
        return get_firstname_filters().filter(value)

    def validate_original_name(self, value):
        return get_name_filters().filter(value)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['consent_check'] = bool(ret['consent'])
        return ret

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        if data['consent_check'] and not 'id' in data:
            ret['consent'] = timezone.now().date()
        else:
            if self.instance:
                ret['consent'] = self.instance.consent
            else:
                ret['consent'] = None
        ret.pop('consent_check')
        return ret

    class Meta:
        model = Patient
        fields = '__all__'
        validators = [
            UniqueTogetherIgnoreCaseValidator(
                queryset=Patient.objects.all(),
                fields=('family_name', 'first_name', 'birth_date'),
                message=_('This patient already exists'),
            )
        ]


class PatientExportSerializer(serializers.ModelSerializer):
    birth_date = serializers.DateField(label=_('Birth date'), )

    class Meta:
        model = Patient
        fields = ('family_name', 'first_name', 'original_name', 'birth_date')


class UserInfoSerializer(serializers.ModelSerializer):

    def validate_last_name(self, value):
        return get_name_filters().filter(value)

    def validate_first_name(self, value):
        return get_name_filters().filter(value)

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name')


class RegularDoctorSerializer(serializers.ModelSerializer):

    def validate_family_name(self, value):
        return get_name_filters().filter(value)

    def validate_first_name(self, value):
        return get_name_filters().filter(value)

    class Meta:
        model = RegularDoctor
        fields = '__all__'


class OfficeDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = OfficeSettings
        fields = ['office_name']


class ExaminationExtractSerializer(WithPkMixin, serializers.ModelSerializer):
    therapeut = UserInfoSerializer()
    comments = serializers.SerializerMethodField('get_nb_comments')
    office_detail = OfficeDetailSerializer(source='office')

    class Meta:
        model = Examination
        fields = ('id', 'reason', 'date', 'status', 'therapeut', 'type',
                  'comments', 'office', 'office_detail')
        depth = 1

    def get_nb_comments(self, obj):
        return ExaminationComment.objects.filter(
            examination__exact=obj.id).count()


class PaimentModeSerializer(serializers.Serializer):
    paiment_mode_text = serializers.SerializerMethodField()

    def get_paiment_mode_text(self, obj):
        if hasattr(obj, 'paiment_mode'):
            paiment_code = obj.paiment_mode
        else:
            paiment_code = obj.get('paiment_mode')
        paiment_mean = PaimentMean.objects.filter(code=paiment_code).first()
        if paiment_mean is not None:
            return paiment_mean.text
        return 'n/a'


class PaimentSerializer(PaimentModeSerializer):
    amount = serializers.FloatField(required=True)
    currency = serializers.CharField(required=True)
    date = serializers.DateField(required=True)
    paiment_mode = serializers.CharField(required=True)


class InvoiceSerializer(WithPkMixin, serializers.ModelSerializer,
                        PaimentModeSerializer):
    paiments_list = PaimentSerializer(many=True,
                                      read_only=True,
                                      allow_null=True,
                                      required=False)
    office_name = serializers.SerializerMethodField()

    def get_office_name(self, obj):
        office = OfficeSettings.objects.get(id=obj.officesettings_id)
        if office is not None:
            return office.office_name
        return 'n/a'

    class Meta:
        model = Invoice
        fields = '__all__'
        depth = 1


class ExaminationSerializer(serializers.ModelSerializer):
    invoice_number = serializers.CharField(source="get_invoice_number",
                                           required=False,
                                           allow_null=True,
                                           read_only=True)
    invoices_list = InvoiceSerializer(many=True,
                                      read_only=True,
                                      allow_null=True,
                                      required=False)
    last_invoice = InvoiceSerializer(read_only=True,
                                     allow_null=True,
                                     required=False)
    therapeut_detail = UserInfoSerializer(source="therapeut",
                                          required=False,
                                          allow_null=True,
                                          read_only=True)
    patient_detail = PatientExportSerializer(source="patient",
                                             required=False,
                                             allow_null=True,
                                             read_only=True)

    office_detail = OfficeDetailSerializer(source="office",
                                           required=False,
                                           allow_null=True,
                                           read_only=True)

    #date = serializers.DateTimeField(default_timezone=timezone.utc)

    class Meta:
        model = Examination
        fields = '__all__'

    def validate_date(self, value):
        to_validate = value
        if timezone.is_naive(value):
            to_validate = pytz.utc.localize(value)
        current = timezone.now()
        if timezone.is_naive(current):
            current = pytz.utc.localize(current)
        #if to_validate >= current:
        #    raise serializers.ValidationError(
        #        _('The examination date is not valid'))
        return to_validate


class CheckSerializer(serializers.Serializer):
    bank = serializers.CharField(required=False, allow_null=True)
    payer = serializers.CharField(required=False, allow_null=True)
    number = serializers.CharField(required=False, allow_null=True)


class ExaminationInvoicingSerializer(serializers.Serializer):
    status = serializers.CharField(required=True)
    reason = serializers.CharField(required=False, allow_null=True)
    paiment_mode = serializers.CharField(required=False, allow_null=True)
    amount = serializers.FloatField(required=False, allow_null=True)
    check = CheckSerializer()

    def validate(self, attrs):
        """
        Check that the invoicing is consistent
        """
        try:
            if attrs['status'] == 'notinvoiced':
                if attrs['reason'] is None or len(
                        attrs['reason'].strip()) == 0:
                    raise serializers.ValidationError(
                        _("Reason is mandatory when the examination is not invoiced"
                          ))
            if attrs['status'] == 'invoiced':
                if attrs['amount'] is None or attrs['amount'] <= 0:
                    raise serializers.ValidationError(_("Amount is invalid"))
                if attrs['paiment_mode'] is None or len(
                        attrs['paiment_mode'].strip()
                ) == 0 or attrs['paiment_mode'] not in [
                        p.code for p in PaimentMean.objects.filter(enable=True)
                ] + ['notpaid']:
                    raise serializers.ValidationError(
                        _("Paiment mode is mandatory when the examination is invoiced"
                          ))
                if attrs['paiment_mode'] == 'check':
                    if attrs['check'] is None:
                        raise serializers.ValidationError(
                            _("Check information is missing"))
                # if attrs['check']['bank'] is None or len(attrs['check']['bank'].strip()) == 0:
                #    raise serializers.ValidationError(_("Bank information is missing about the check paiment"))
                # if attrs['check']['payer'] is None or len(attrs['check']['payer'].strip()) == 0:
                #    raise serializers.ValidationError(_("Payer information is missing about the check paiment"))
                # if attrs['check']['number'] is None or len(attrs['check']['number'].strip()) == 0:
                #    raise serializers.ValidationError(_("Number information is missing about the check paiment"))
            return attrs
        except KeyError:
            raise serializers.ValidationError(_('Missing data to continue'))


class InvoiceCancelingWithCorrectiveInvoiceSerializer(serializers.Serializer):
    examination = ExaminationSerializer()
    corrective_invoice = ExaminationInvoicingSerializer()


class ExaminationCommentSerializer(WithPkMixin, serializers.ModelSerializer):
    user_info = UserInfoSerializer(source="user",
                                   required=False,
                                   read_only=True)

    class Meta:
        model = ExaminationComment
        fields = '__all__'


class OfficeEventSerializer(WithPkMixin, serializers.ModelSerializer):

    class Meta:
        model = OfficeEvent
        fields = '__all__'

    patient_name = serializers.SerializerMethodField()
    translated_comment = serializers.SerializerMethodField()
    therapeut_name = UserInfoSerializer(source='user')

    def get_patient_name(self, obj):
        if (obj.clazz == "Patient"):
            patient = Patient.objects.get(id=obj.reference)
            return "%s %s" % (patient.family_name, patient.first_name)
        if (obj.clazz == "Examination"):
            try:
                examination = Examination.objects.get(id=obj.reference)
                patient = examination.patient
                return "%s %s" % (patient.family_name, patient.first_name)
            except ObjectDoesNotExist:
                pass
        return ""

    def get_translated_comment(self, obj):
        return _(obj.comment)


class TherapeutSettingsSerializer(WithPkMixin, serializers.ModelSerializer):

    class Meta:
        model = TherapeutSettings
        fields = '__all__'


class OfficeSettingsSerializer(WithPkMixin, serializers.ModelSerializer):

    class Meta:
        model = OfficeSettings
        fields = '__all__'

    network_list = serializers.SerializerMethodField()
    invoice_min_sequence = serializers.SerializerMethodField()
    selected = serializers.SerializerMethodField()

    def validate(self, data):
        try:
            input_invoice_start_seq = data['invoice_start_sequence']
        except KeyError:
            input_invoice_start_seq = None
        try:
            input_invoice_prefix_seq = data['invoice_prefix_sequence']
        except KeyError:
            input_invoice_prefix_seq = None
        if input_invoice_start_seq is None or len(
                input_invoice_start_seq) <= 0:
            last_invoice_number = Invoice.objects.filter(
                officesettings_id=self.instance.id).aggregate(
                    Max('number'))['number__max']
            if last_invoice_number is not None:
                data['invoice_start_sequence'] = _unicode(last_invoice_number)
            else:
                data['invoice_start_sequence'] = _unicode(10000)
        if input_invoice_prefix_seq is not None:
            input_invoice_prefix_seq = input_invoice_prefix_seq.strip()
            if len(input_invoice_prefix_seq) > 3:
                raise serializers.ValidationError(
                    _('Prefix for invoicing sequence should have 3 char length maximum'
                      ))
            if len(input_invoice_prefix_seq) == 0:
                input_invoice_prefix_seq = None
            elif not re.match('^[A-Za-z]{1,3}$', input_invoice_prefix_seq):
                raise serializers.ValidationError(
                    _('Prefix could only contains alpha characters'))
            data['invoice_prefix_sequence'] = input_invoice_prefix_seq
        return data

    def get_network_list(self, obj):
        addresses = []
        if settings.DISPLAY_SERVICE_NET_HELPER is False:
            return addresses
        net_helper = NetworkHelper()
        port = self.context.get('request').META['SERVER_PORT']
        addresses = net_helper.get_bound_addresses(
            net_helper.get_all_addresses(), port)
        addresses = [
            'http://%s:%s' % (a, port) for a in addresses if a != '127.0.0.1'
        ]
        return addresses

    def get_invoice_min_sequence(self, obj):
        result_query = Invoice.objects.filter(
            officesettings_id=obj.id).aggregate(Max('number'))['number__max']
        if result_query is not None and len(result_query) > 0:
            return convert_to_long(result_query, strip_string_prefix=True) + 1
        return 1

    def get_selected(self, obj):
        if hasattr(self.context['request'], 'officesettings'):
            return self.context['request'].officesettings.id == obj.id
        return False


class UserOfficeSerializer(WithPkMixin, serializers.ModelSerializer):

    def validate_family_name(self, value):
        return get_name_filters().filter(value)

    def validate_first_name(self, value):
        return get_name_filters().filter(value)

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'first_name', 'last_name', 'is_staff',
                  'is_active')


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=False)


class FileImportSerializer(WithPkMixin, serializers.ModelSerializer):
    _status = None

    class Meta:
        model = FileImport
        fields = '__all__'

    analyze = serializers.SerializerMethodField()
    extract = serializers.SerializerMethodField()

    def get_analyze(self, obj):
        if obj.analyze is not None:
            return obj.analyze

    def get_extract(self, obj):
        return Extractor().extract(obj)


class DocumentSerializer(WithPkMixin, serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = '__all__'


class DocumentUpdateSerializer(WithPkMixin, serializers.ModelSerializer):

    class Meta:
        fields = ['title', 'notes', 'document_date']
        model = Document


class PatientDocumentSerializer(WithPkMixin, serializers.ModelSerializer):
    document = DocumentSerializer()
    patient = serializers.PrimaryKeyRelatedField(
        many=False, queryset=Patient.objects.all())

    class Meta:
        model = PatientDocument
        fields = '__all__'
        depth = 2

    def create(self, validated_data):
        document_data = validated_data.pop('document')
        document_data['user'] = validated_data.pop('user')
        patient = validated_data.pop("patient")
        document = Document.objects.create(internal_date=timezone.now(),
                                           **document_data)
        document.clean()
        document.save()
        patient_doc = PatientDocument.objects.create(patient=patient,
                                                     document=document,
                                                     **validated_data)
        return patient_doc


class PatientDocumentDemonstrationSerializer(PatientDocumentSerializer):

    def create(self, validated_data):
        document_data = validated_data.pop('document')
        document_data['user'] = validated_data.pop('user')
        document_data['document_file'] = get_demonstration_file()
        patient = validated_data.pop("patient")
        document = Document.objects.create(internal_date=timezone.now(),
                                           **document_data)
        document.clean()
        document.save()
        patient_doc = PatientDocument.objects.create(patient=patient,
                                                     document=document,
                                                     **validated_data)
        return patient_doc


class PaimentMeanSerializer(WithPkMixin, serializers.ModelSerializer):

    class Meta:
        model = PaimentMean
        fields = '__all__'
