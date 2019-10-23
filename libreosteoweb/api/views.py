
# This file is part of Libreosteo.
#
# Libreosteo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Libreosteo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Libreosteo.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import unicode_literals
import sys
if sys.version_info.major == 2:
    from io import BytesIO
    from io import BytesIO as StringIO
else :
    from io import BytesIO,StringIO
from datetime import datetime
from django.utils import timezone
import logging
import os
import tempfile
import zipfile

from rest_framework import pagination, viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError,PermissionDenied,ParseError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from haystack.query import SearchQuerySet
from haystack.views import SearchView
from django.contrib.auth import get_user_model, REDIRECT_FIELD_NAME
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files import File
from django.core.management import call_command
from django.db.models import signals
from django.http import (
    HttpResponse, HttpResponseForbidden,
    HttpResponseRedirect, Http404)
from django.shortcuts import resolve_url
from django.utils.http import is_safe_url
from django.utils.translation import ugettext_lazy as _
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.generic.base import TemplateView
from django.db.models import Max

from libreosteoweb.api import serializers as apiserializers
from libreosteoweb import models
from .exceptions import Forbidden
from .permissions import StaffRequiredMixin
from .permissions import (
    IsStaffOrTargetUser, IsStaffOrReadOnlyTargetUser, maintenance_available,
    IsStaffOrTargetUserFactory)
from .receivers import (
    block_disconnect_all_signal, receiver_examination, temp_disconnect_signal,
    receiver_newpatient)
from .renderers import (
    ExaminationCSVRenderer, InvoiceCSVRenderer,
    PatientCSVRenderer)
from .statistics import Statistics
from .file_integrator import Extractor, IntegratorHandler
from .utils import convert_to_long
from libreosteoweb.api.invoicing import generator as invoicing_generator
from libreosteoweb.api.events.settings import settings_event_tracer

# Get an instance of a logger
logger = logging.getLogger(__name__)


def create_superuser(request, user):
    UserModel = get_user_model()
    UserModel.objects.create_superuser(user['username'], '', user['password1'])


class CreateAdminAccountView(TemplateView):
    template_name = 'account/create_admin_account.html'

    def get(self, request, *args, **kwargs):
        """
        Displays the login form and handles the login action.
        """
        if len(User.objects.filter(is_staff__exact=True)) > 0:
            raise Http404
        self.redirect_to = request.POST.get(
            REDIRECT_FIELD_NAME, request.GET.get(REDIRECT_FIELD_NAME, ''))
        self.form = UserCreationForm()
        return super(TemplateView,
                     self).render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        redirect_to = request.POST.get(
            REDIRECT_FIELD_NAME, request.GET.get(REDIRECT_FIELD_NAME, ''))
        if form.is_valid():
            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
            # Okay, security check complete. Log the user in.
            create_superuser(request, form.data)
            return HttpResponseRedirect(redirect_to)
        else:
            self.form = form
        return super(TemplateView,
                     self).render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super(CreateAdminAccountView,
                        self).get_context_data(**kwargs)
        if self.form:
            context['form'] = self.form
            if self.redirect_to:
                context[REDIRECT_FIELD_NAME] = self.redirect_to
        return context


class InstallView(TemplateView):
    template_name = 'install.html'
    http_method_names = ['get', 'post', 'head', 'options', 'trace']

    def get(self, request, *args, **kwargs):
        """
        Displays the install status and handle the action on install.
        """
        if len(User.objects.filter(is_staff__exact=True)) > 0:
            raise HttpResponseForbidden
        self.redirect_field_name = request.POST.get(
            REDIRECT_FIELD_NAME, request.GET.get(REDIRECT_FIELD_NAME, ''))
        return super(TemplateView,
                     self).render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        if len(User.objects.filter(is_staff__exact=True)) > 0:
            raise HttpResponseForbidden
        return super(TemplateView,
                     self).render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)
        if self.redirect_field_name:
            context[REDIRECT_FIELD_NAME] = self.redirect_field_name
        return context


class SearchViewHtml(SearchView):
    template = 'partials/search-result.html'
    results_per_page = 10
    results = SearchQuerySet()


class InvoiceViewHtml(TemplateView):
    template_name = 'invoice/invoice-result.html'

    def get_context_data(self, **kwargs):
        context = super(InvoiceViewHtml, self).get_context_data(**kwargs)
        context['invoice'] = models.Invoice.objects.get(pk=kwargs['invoiceid'])
        if context['invoice'].paiment_mode != 'notpaid':
            context['paiment_mean'] = _(
                models.PaimentMean.objects.get(
                    code=context['invoice'].paiment_mode).text).lower()
        else:
            context['paiment_mean'] = _('Not paid')
        context['paiments'] = [p for p in context['invoice'].paiment_set.all()]
        for p in context['paiments']:
            p.paiment_mode = _(
                models.PaimentMean.objects.get(
                    code=p.paiment_mode).text).lower()
        return context


class PatientViewSet(viewsets.ModelViewSet):
    model = models.Patient
    serializer_class = apiserializers.PatientSerializer
    queryset = models.Patient.objects.all()
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES + [
        PatientCSVRenderer,
    ]

    @action(detail=True, methods=['get'])
    def examinations(self, request, pk=None):
        current_patient = self.get_object()
        examinations = models.Examination.objects.filter(
            patient=current_patient).order_by('-date')
        return Response(
            apiserializers.ExaminationExtractSerializer(examinations,
                                                        many=True).data)

    def perform_create(self, serializer):
        instance = models.Patient(**serializer.validated_data)
        instance.set_user_operation(self.request.user)
        instance.full_clean()
        instance.save()
        serializer.instance = instance

    def perform_update(self, serializer):
        serializer.instance.set_user_operation(self.request.user)
        return super(PatientViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        is_gdpr_request = 'gdpr' in self.request.query_params and self.request.query_params[
            'gdpr']
        examination_list = models.Examination.objects.filter(
            patient=instance.id)
        if not len(examination_list) == 0 and not is_gdpr_request:
            raise Forbidden()

        models.OfficeEvent.objects.filter(
            reference=instance.id, clazz=models.Patient.__name__).delete()
        for e in examination_list:
            models.OfficeEvent.objects.filter(
                reference=e.id, clazz=models.Examination.__name__).delete()
        models.Examination.objects.filter(patient=instance.id).delete()
        models.PatientDocument.objects.filter(patient=instance.id).delete()
        return super(PatientViewSet, self).perform_destroy(instance)


class RegularDoctorViewSet(viewsets.ModelViewSet):
    model = models.RegularDoctor
    queryset = models.RegularDoctor.objects.all()
    serializer_class = apiserializers.RegularDoctorSerializer



class ExaminationViewSet(viewsets.ModelViewSet):
    model = models.Examination
    queryset = models.Examination.objects.all()
    serializer_class = apiserializers.ExaminationSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES + [
        ExaminationCSVRenderer,
    ]

    @action(detail=True, methods=['post'])
    def invoice(self, request, pk=None):
        current_examination = self.get_object()
        serializer = apiserializers.ExaminationInvoicingSerializer(
            data=request.data)
        return self._invoice_examination(current_examination, serializer)

    def _invoice_examination(self, current_examination, invoicing_serializer):
        if invoicing_serializer.is_valid():
            if invoicing_serializer.data['status'] == 'notinvoiced':
                current_examination.status = models.Examination.EXAMINATION_NOT_INVOICED
                current_examination.status_reason = invoicing_serializer.data[
                    'reason']
                current_examination.save()
                return Response({'invoiced': None})
            if invoicing_serializer.data['status'] == 'invoiced':
                current_invoice = self.generate_invoice(
                    invoicing_serializer.data, )
                current_examination.invoices.add(current_invoice)
                if invoicing_serializer.data['paiment_mode'] == 'notpaid':
                    current_examination.status = models.ExaminationStatus.WAITING_FOR_PAIEMENT
                    current_invoice.status = models.InvoiceStatus.WAITING_FOR_PAIEMENT
                    current_invoice.save()
                    current_examination.save()
                if invoicing_serializer.data['paiment_mode'] in [
                        p.code
                        for p in models.PaimentMean.objects.filter(enable=True)
                ]:
                    current_examination.status = models.ExaminationStatus.INVOICED_PAID
                    current_invoice.status = models.InvoiceStatus.INVOICED_PAID
                    current_invoice.save()
                    current_examination.save()
            return Response({'invoiced': current_invoice.id})
        else:
            return Response(invoicing_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def update_paiement(self, request, pk=None):
        current_examination = self.get_object()
        serializer = apiserializers.ExaminationInvoicingSerializer(
            data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if serializer.data[
                'status'] != 'invoiced' or current_examination.last_invoice is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if serializer.data['paiment_mode'] == 'notpaid':
            return Response(
                {'not modified': current_examination.last_invoice.id})
        if current_examination.last_invoice.status != models.InvoiceStatus.WAITING_FOR_PAIEMENT:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        current_examination.status = models.ExaminationStatus.INVOICED_PAID
        invoice_to_update = models.Invoice.objects.get(
            id=current_examination.last_invoice.id)
        invoice_to_update.status = models.InvoiceStatus.INVOICED_PAID
        officesettings = models.OfficeSettings.objects.all()[0]
        p = models.Paiment(amount=invoice_to_update.amount,
                           currency=officesettings.currency,
                           date=timezone.now(),
                           paiment_mode=serializer.data['paiment_mode'])
        p.save()
        p.invoice.add(current_examination.last_invoice)
        p.save()
        invoice_to_update.save()
        current_examination.save()
        return Response({'invoiced': current_examination.last_invoice.id})

    @action(detail=True, methods=['POST'])
    def close(self, request, pk=None):
        current_examination = self.get_object()
        serializer = apiserializers.ExaminationInvoicingSerializer(
            data=request.data)
        return self._invoice_examination(current_examination, serializer)

    def generate_invoice(self, invoicingSerializerData):
        officesettings = models.OfficeSettings.objects.all()[0]
        therapeutsettings = models.TherapeutSettings.objects.filter(
            user=self.request.user)[0]

        invoice = invoicing_generator.Generator(
            officesettings,
            therapeutsettings).generate_invoice(self.get_object(),
                                                invoicingSerializerData,
                                                self.request)
        officesettings.save()
        invoice.save()
        return invoice


    def perform_create(self, serializer):
        if not self.request.user.is_authenticated():
            raise Http404()
        serializer.save(therapeut=self.request.user)

    def perform_update(self, serializer):
        if not self.request.user.is_authenticated():
            raise Http404()
        if not serializer.instance.therapeut:
            serializer.save(therapeut=self.request.user)
        serializer.save(therapeut=serializer.instance.therapeut)

    def perform_destroy(self, instance):
        if not instance.status == 0:
            raise Forbidden()
        models.OfficeEvent.objects.filter(
            reference=instance.id, clazz=models.Examination.__name__).delete()
        return super(ExaminationViewSet, self).perform_destroy(instance)

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        current_examination = self.get_object()
        comments = models.ExaminationComment.objects.filter(
            examination=current_examination).order_by('-date')
        return Response(
            apiserializers.ExaminationCommentSerializer(comments,
                                                        many=True).data)

    @action(detail=False, methods=['get'])
    def unpaid(self, request, pk=None):
        unpaid_examinations = models.Examination.objects.filter(
            status=models.ExaminationStatus.WAITING_FOR_PAIEMENT).order_by(
                '-date')
        return Response(
            apiserializers.ExaminationSerializer(unpaid_examinations,
                                                 many=True).data)


class UserViewSet(viewsets.ModelViewSet):
    model = User
    serializer_class = apiserializers.UserInfoSerializer
    permission_classes = [IsStaffOrTargetUser]
    queryset = User.objects.all()


class UserOfficeViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = apiserializers.UserOfficeSerializer
    permission_classes = [IsStaffOrReadOnlyTargetUser]

    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = apiserializers.PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.data['password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)



class StatisticsView(APIView):

    def get(self, request, *args, **kwargs):
        myStats = Statistics(*args, **kwargs)
        result = myStats.compute()
        response = Response(result, status=status.HTTP_200_OK)
        return response


class InvoiceViewSet(viewsets.ReadOnlyModelViewSet):
    model = models.Invoice
    queryset = models.Invoice.objects.all()
    serializer_class = apiserializers.InvoiceSerializer
    filter_fields = {'date': ['lte', 'gte']}
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES + [
        InvoiceCSVRenderer
    ]

    def get_renderer_context(self):
        # allows to select which fields we want via ?fields=field1,field2
        # works only for CSV renderer
        context = super(InvoiceViewSet, self).get_renderer_context()
        context['header'] = (self.request.GET['fields'].split(',')
                             if 'fields' in self.request.GET else None)
        return context

    def get_queryset(self):
        queryset = models.Invoice.objects.all()
        therapeut_id = self.request.query_params.get('therapeut_id', None)
        if therapeut_id is not None:
            queryset = queryset.filter(therapeut_id=therapeut_id)
        return queryset

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        # Ensure that invoice was not canceled before
        if self.get_object().status != models.InvoiceStatus.CANCELED:
            officesettings = models.OfficeSettings.objects.all()[0]
            cancelation = invoicing_generator.Generator(
                officesettings, None).cancel_invoice(self.get_object())
            canceled = self.get_object()
            canceled.status = models.InvoiceStatus.CANCELED
            cancelation.save()
            canceled.canceled_by = cancelation
            canceled.save()
            officesettings.save()
            response = {
                'canceled': self.serializer_class(self.get_object()).data,
                'credit_note': self.serializer_class(cancelation).data
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class OfficeEventViewSet(viewsets.ReadOnlyModelViewSet):
    model = models.OfficeEvent
    serializer_class = apiserializers.OfficeEventSerializer
    queryset = models.OfficeEvent.objects.all()
    pagination_class = pagination.LimitOffsetPagination

    def get_queryset(self):
        """
        By default, filter events on only new patient/new examinations
        No update events are given.
        'all' parameter is used to get all events
        """
        queryset = models.OfficeEvent.objects.all().order_by('-date')
        all_flag = self.request.query_params.get('all', None)
        if all_flag is None:
            queryset = queryset.exclude(clazz__exact='Patient', type__exact=2)
        return queryset


class OfficeSettingsView(viewsets.ModelViewSet):
    model = models.OfficeSettings
    serializer_class = apiserializers.OfficeSettingsSerializer
    permission_classes = [IsStaffOrReadOnlyTargetUser]
    queryset = models.OfficeSettings.objects.all()

    def perform_update(self, serializer):
        # Check that the invoice_start_sequence is valid
        result_query = models.Invoice.objects.aggregate(
            Max('number'))['number__max']
        if result_query is not None:
            max_value = convert_to_long(result_query)
        else:
            max_value = 1
        try:
            asked_value = serializer.validated_data['invoice_start_sequence']
            if asked_value is not None and asked_value.isnumeric():
                if convert_to_long(asked_value) > 0 and convert_to_long(
                        asked_value) > max_value:
                    settings_event_tracer(serializer.instance,
                                          self.request.user, asked_value)
                    serializer.save()
                else:
                    raise PermissionDenied(
                        detail="invoice start sequence could not be applied")
            else:
                serializer.validated_data[
                    'invoice_start_sequence'] = serializer.instance.invoice_start_sequence
                serializer.save()
        except KeyError as e:
            raise ParseError(detail=e)


class TherapeutSettingsViewSet(viewsets.ModelViewSet):
    model = models.TherapeutSettings
    serializer_class = apiserializers.TherapeutSettingsSerializer
    permission_classes = [
        IsStaffOrTargetUserFactory.additional_methods(['get_by_user'])
    ]
    queryset = models.TherapeutSettings.objects.all()

    @action(detail=False)
    def get_by_user(self, request):
        therapeut_settings, _ = models.TherapeutSettings.objects.get_or_create(
            user=self.request.user)
        return Response(
            apiserializers.TherapeutSettingsSerializer(
                therapeut_settings).data)

    def perform_update(self, serializer):
        if not serializer.instance.user:
            serializer.save(user=self.request.user)
        serializer.save(user=serializer.instance.user)


class ExaminationCommentViewSet(viewsets.ModelViewSet):
    model = models.ExaminationComment
    serializer_class = apiserializers.ExaminationCommentSerializer
    queryset = models.ExaminationComment.objects.all()

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated():
            raise Http404()
        serializer.save(user=self.request.user, date=datetime.today())


class FileImportViewSet(viewsets.ModelViewSet):
    model = models.FileImport
    serializer_class = apiserializers.FileImportSerializer
    queryset = models.FileImport.objects.all()


    def perform_create(self, serializer):
        if not self.request.user.is_authenticated():
            raise Http404()
        instance = serializer.save()
        logger.info("* Ready to start analyze")
        extractor = Extractor()

        status = extractor.analyze(instance)

        if status['patient'][0] == 'examination':
            tmp = status['examination']
            tmp_file = instance.file_examination
            status['examination'] = status['patient']
            instance.file_examination = instance.file_patient
            if tmp[0] == 'patient' and tmp_file:
                status['patient'] = tmp
                instance.file_patient = tmp_file
            else:
                raise ValidationError("Missing patient file after analyze")
        logger.info("* Status after analyze is : %s " % (status))
        is_all_valid = True
        for f in status:
            (type_file, is_valid, is_empty, errors) = status[f]
            if type_file in ["examination", "patient"]:
                is_all_valid = is_all_valid and is_valid and not (is_empty)
        if is_all_valid:
            instance.status = 1
        else:
            instance.status = 0
        instance.analyze = status
        instance.save()

    @action(detail=True, methods=['post', 'get'])
    def integrate(self, request, pk=None):
        file_import_couple = self.get_object()
        integrator = IntegratorHandler()
        nb_line_patient = None
        nb_line_examination = None
        response = {
            'patient': {
                'imported': 0,
                'errors': []
            },
            'examination': {
                'imported': 0,
                'errors': []
            }
        }
        with temp_disconnect_signal(signal=signals.post_save,
                                    receiver=receiver_newpatient,
                                    sender=models.Patient):
            if file_import_couple.file_patient:
                # Start integration of each patient in the file
                (nb_line_patient, errors_patient) = integrator.integrate(
                    file_import_couple.file_patient)
                response['patient'] = {
                    'imported': nb_line_patient,
                    'errors': errors_patient
                }
        with temp_disconnect_signal(signal=signals.post_save,
                                    receiver=receiver_examination,
                                    sender=models.Examination):
            if file_import_couple.file_examination:
                # Start integration of each examination in the file
                (nb_line_examination,
                 errors_examination) = integrator.integrate(
                     file_import_couple.file_examination,
                     file_additional=file_import_couple.file_patient,
                     user=request.user)
                response['examination'] = {
                    'imported': nb_line_examination,
                    'errors': errors_examination
                }
        integrator.post_processing(files=[
            file_import_couple.file_patient,
            file_import_couple.file_examination
        ])
        return Response(response, status=status.HTTP_200_OK)


class DocumentViewSet(viewsets.ModelViewSet):
    model = models.Document
    queryset = models.Document.objects.all()

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated():
            raise Http404()
        serializer.save(user=self.request.user, internal_date=datetime.today())

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return apiserializers.DocumentUpdateSerializer
        else:
            return apiserializers.DocumentSerializer


class PatientDocumentViewSet(viewsets.ModelViewSet):
    model = models.PatientDocument
    serializer_class = apiserializers.PatientDocumentSerializer
    filter_fields = ['patient']

    def get_queryset(self):
        try:
            patient = self.kwargs['patient']
            return models.PatientDocument.objects.filter(patient__id=patient)
        except KeyError:
            return models.PatientDocument.objects.all()

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated():
            raise Http404()
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if settings.DEMONSTRATION :
            return apiserializers.PatientDocumentDemonstrationSerializer
        return apiserializers.PatientDocumentSerializer


class PaimentMeanViewSet(viewsets.ModelViewSet):
    model = models.PaimentMean
    serializer_class = apiserializers.PaimentMeanSerializer
    queryset = models.PaimentMean.objects.all()


DUMP_FILE = "libreosteo.db"


class DbDump(StaffRequiredMixin, View):
    @never_cache
    def get(self, request, *args, **kwargs):
        zip_content = BytesIO()
        zf = zipfile.ZipFile(zip_content, "w")

        buf = StringIO()
        call_command('dumpdata',
                     exclude=['contenttypes', 'admin', 'auth.Permission'],
                     stdout=buf)
        buf.seek(0)

        zf.writestr('dump.json', buf.getvalue())

        documents = models.Document.objects.all()

        for document in documents:
            zf.write(document.document_file.path, document.document_file.name)

        zf.close()

        response = HttpResponse(zip_content.getvalue(),
                                content_type="application/binary")
        response['Content-Disposition'] = 'attachment; filename=%s-%s' % (
            datetime.now().isoformat(), DUMP_FILE)

        return response


class RebuildIndex(StaffRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        call_command('rebuild_index', interactive=False)
        return HttpResponse(u'index rebuilt')


class LoadDump(View):
    @maintenance_available()
    def post(self, request, *args, **kwargs):
        # Retrieve the content of the file uploaded.
        try:
            if ('file' in request.FILES.keys()):
                logger.info("Load a dump from a sent file.")
                # Write the received file into a file into settings.FIXTURE_DIRS
                file_content = ContentFile(request.FILES['file'].read())
                filename = 'dump.json'
                tmpdir = tempfile.gettempdir()
                fixture = os.path.join(tmpdir, filename)

                # Check if zip file
                if zipfile.is_zipfile(file_content):
                    # uncompress the files
                    # uncompress the dump file
                    zf = zipfile.ZipFile(file_content)
                    if filename in zf.namelist():
                        zf.extract(filename, tmpdir)
                        # uncompress all document
                        for d in [
                                f for f in zf.namelist() if f != 'dump.json'
                        ]:
                            zf.extract(d, settings.MEDIA_ROOT)
                    else:
                        raise Exception(
                            "This zipfile does not contain the db dump")
                else:
                    # old fashioned style of import archive
                    tmp_dump = open(fixture, 'w')
                    f = File(tmp_dump)
                    for chunk in file_content.chunks():
                        f.write(chunk)
                    f.close()

                logger.info("Dump file was persisted for future loading.")
                receivers_senders = [(receiver_examination,
                                      models.Examination),
                                     (receiver_newpatient, models.Patient)]

                with block_disconnect_all_signal(
                        signal=signals.post_save,
                        receivers_senders=receivers_senders):
                    logger.info(
                        "Signals were disactivated, perform clearing of the database"
                    )
                    call_command('flush',
                                 interactive=False,
                                 load_initial_data=False)
                    # It means that the settings.FIXTURE_DIRS should be set in settings
                    previous = settings.FIXTURE_DIRS
                    settings.FIXTURE_DIRS = [tempfile.gettempdir()]
                    # And when loading dumps, write the file into this directory with the name : load_dump.json
                    logger.info("Load the fixture from path : %s " % (fixture))
                    call_command('loaddata', fixture)
                    # Delete the fixture
                    logger.info("Clearing the fixture")
                    os.remove(fixture)
                    settings.FIXTURE_DIRS = previous
                    logger.info("Could restore signals")
                logger.info("end of reloading.")
                return HttpResponse(content=u'reloaded')
            else:
                return HttpResponse()
        except:
            logger.exception('Import failed')
            return HttpResponse(content=_(
                u'This archive file seems to be incorrect. Impossible to load it.'
            ),
                                status=412)
