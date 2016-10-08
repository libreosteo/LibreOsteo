from __future__ import unicode_literals
from rest_framework import viewsets, filters, pagination
from rest_framework.filters import DjangoFilterBackend
import django_filters
from libreosteoweb import models 
from rest_framework.decorators import  detail_route, list_route
from libreosteoweb.api import serializers as apiserializers
from rest_framework.response import Response
from haystack.query import SearchQuerySet
from django.core import serializers
from django.http import HttpResponse
from django.views.generic import View
from haystack.utils import Highlighter
from haystack.views import SearchView
from haystack.query import SearchQuerySet
import json
import logging
from django.contrib.auth.models import User
from .permissions import IsStaffOrTargetUser, IsStaffOrReadOnlyTargetUser, maintenance_available
from .exceptions import Forbidden
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from datetime import date, datetime
from rest_framework import status
from django.views.generic.base import TemplateView
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import (REDIRECT_FIELD_NAME, get_user_model )
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url
from django.shortcuts import resolve_url
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponseNotFound, Http404
from datetime import datetime
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ValidationError
from .receivers import temp_disconnect_signal,receiver_newpatient, receiver_examination,block_disconnect_all_signal
from django.db.models import signals
from django.contrib.admin.views.decorators import staff_member_required

import os

# Get an instance of a logger
logger = logging.getLogger(__name__)

def create_superuser(request, user):
    UserModel = get_user_model()
    UserModel.objects.create_superuser(user['username'], '', user['password1'])

@csrf_protect
@never_cache
def create_admin_account(request, template_name='account/create_admin_account.html',
    redirect_field_name=REDIRECT_FIELD_NAME,
    registration_form=UserCreationForm):
    """
    Displays the login form and handles the login action.
    """
    if len(User.objects.filter(is_staff__exact=True)) > 0 :
        raise Http404
    redirect_to = request.POST.get(redirect_field_name,
    request.GET.get(redirect_field_name, ''))
    if request.method == "POST":
        form = registration_form(request.POST)
        if form.is_valid():
            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
            # Okay, security check complete. Log the user in.
            create_superuser(request, form.data)
            return HttpResponseRedirect(redirect_to)
        else :
            context = {
                'form':form
            }
    else:
        form = registration_form()
        context = {
            'form': form,
            redirect_field_name: redirect_to
        }
    return TemplateResponse(request, template_name, context)

@csrf_protect
@never_cache
def install(request, template_name='install.html',
    redirect_field_name=REDIRECT_FIELD_NAME,
    registration_form=UserCreationForm):
    """
    Displays the install status and handle the action on install.
    """
    if len(User.objects.filter(is_staff__exact=True)) > 0 :
        raise HttpResponseForbidden
    redirect_to = request.POST.get(redirect_field_name,
    request.GET.get(redirect_field_name, ''))
    if request.method == "POST":
        pass
    else:
        context = {
            redirect_field_name: redirect_to
        }
    return TemplateResponse(request, template_name, context)

class SearchViewHtml(SearchView):
    template = 'partials/search-result.html'
    results_per_page = 10
    results = SearchQuerySet()

class InvoiceViewHtml(TemplateView):
    template_name = 'invoice/invoice-result.html'

    def get_context_data(self, **kwargs):
        context = super(InvoiceViewHtml, self).get_context_data(**kwargs)
        context['invoice'] = models.Invoice.objects.get(pk=kwargs['invoiceid'])
        return context



from rest_framework.settings import api_settings
from rest_framework_csv import renderers as r
from .renderers import PatientCSVRenderer, ExaminationCSVRenderer


class PatientViewSet(viewsets.ModelViewSet):
    model = models.Patient
    serializer_class = apiserializers.PatientSerializer
    queryset = models.Patient.objects.all()
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES + [PatientCSVRenderer, ]

    @detail_route(methods=['GET'])
    def examinations(self, request, pk=None):
        current_patient = self.get_object()
        examinations = models.Examination.objects.filter(patient=current_patient).order_by('-date')
        return Response(apiserializers.ExaminationExtractSerializer(examinations, many=True).data)

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
        examination_list = models.Examination.objects.filter(patient=instance.id)
        if not len(examination_list) == 0:
            raise Forbidden()
        models.OfficeEvent.objects.filter(reference=instance.id, clazz=models.Patient.__name__).delete()
        return super(PatientViewSet, self).perform_destroy(instance)


class RegularDoctorViewSet(viewsets.ModelViewSet):
    model = models.RegularDoctor
    queryset = models.RegularDoctor.objects.all()
    serializer_class = apiserializers.RegularDoctorSerializer





class ExaminationViewSet(viewsets.ModelViewSet):
    model = models.Examination
    queryset = models.Examination.objects.all()
    serializer_class = apiserializers.ExaminationSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES + [ExaminationCSVRenderer, ]


    @detail_route(methods=['POST'])
    def close(self, request, pk=None):
        current_examination = self.get_object()
        serializer = apiserializers.ExaminationInvoicingSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data['status'] == 'notinvoiced':
                current_examination.status = models.Examination.EXAMINATION_NOT_INVOICED
                current_examination.status_reason = serializer.data['reason']
                current_examination.save()
                return Response({'invoiced' : None})
            if serializer.data['status'] == 'invoiced':
                current_examination.invoice = self.generate_invoice(serializer.data, )
                if serializer.data['paiment_mode'] == 'notpaid':
                    current_examination.status = models.Examination.EXAMINATION_WAITING_FOR_PAIEMENT
                    current_examination.save()
                if serializer.data['paiment_mode'] in ['check', 'cash']:
                    current_examination.status = models.Examination.EXAMINATION_INVOICED_PAID
                    current_examination.save()
            return Response({'invoiced': current_examination.invoice.id})
        else :
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def generate_invoice(self, invoicingSerializerData):
        officesettings = models.OfficeSettings.objects.all()[0]
        therapeutsettings = models.TherapeutSettings.objects.filter(user=self.request.user)[0]

        invoice = models.Invoice()
        invoice.amount = invoicingSerializerData['amount']
        invoice.currency = officesettings.currency
        invoice.header = officesettings.invoice_office_header
        invoice.office_address_street = officesettings.office_address_street
        invoice.office_address_complement = officesettings.office_address_complement
        invoice.office_address_zipcode = officesettings.office_address_zipcode
        invoice.office_address_city = officesettings.office_address_city
        invoice.office_phone = officesettings.office_phone
        invoice.office_siret = officesettings.office_siret

        # Override the siret on the invoice with the therapeut siret if defined
        if therapeutsettings.siret is not None :
            invoice.office_siret = therapeutsettings.siret

        invoice.paiment_mode = invoicingSerializerData['paiment_mode']
        invoice.therapeut_name = self.request.user.last_name
        invoice.therapeut_first_name = self.request.user.first_name
        invoice.quality = therapeutsettings.quality
        invoice.adeli = therapeutsettings.adeli
        invoice.location = officesettings.office_address_city
        invoice.number = ""

        invoice.patient_family_name = self.get_object().patient.family_name
        invoice.patient_original_name = self.get_object().patient.original_name
        invoice.patient_first_name = self.get_object().patient.first_name
        invoice.patient_address_street = self.get_object().patient.address_street
        invoice.patient_address_complement = self.get_object().patient.address_complement
        invoice.patient_address_zipcode = self.get_object().patient.address_zipcode
        invoice.patient_address_city = self.get_object().patient.address_city
        invoice.content_invoice = officesettings.invoice_content
        invoice.footer = officesettings.invoice_footer

        # Override the footer on the invoice with the therapeut settings if defined
        if therapeutsettings.invoice_footer is not None :
            invoice.footer = therapeutsettings.invoice_footer
        invoice.date = datetime.today()
        invoice.save()
        invoice.number += unicode(10000+invoice.id)
        invoice.save()
        return invoice

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated():
            raise Http404()
        serializer.save(therapeut=self.request.user)

    def perform_update(self, serializer):
        if not self.request.user.is_authenticated():
            raise Http404()
        if not serializer.instance.therapeut :
            serializer.save(therapeut=self.request.user)
        serializer.save(therapeut=serializer.instance.therapeut)

    def perform_destroy(self, instance):
        if not instance.status == 0:
            raise Forbidden()
        models.OfficeEvent.objects.filter(reference=instance.id, clazz=models.Examination.__name__).delete()
        return super(ExaminationViewSet, self).perform_destroy(instance)

    @detail_route(methods=['GET'])
    def comments(self, request, pk=None):
        current_examination = self.get_object()
        comments = models.ExaminationComment.objects.filter(examination=current_examination).order_by('-date')
        return Response(apiserializers.ExaminationCommentSerializer(comments, many=True).data)




class UserViewSet(viewsets.ModelViewSet):
    model = User
    serializer_class =  apiserializers.UserInfoSerializer
    permission_classes = [IsStaffOrTargetUser]
    queryset = User.objects.all()


class UserOfficeViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = apiserializers.UserOfficeSerializer
    permission_classes = [IsStaffOrReadOnlyTargetUser]

    @detail_route(methods=['post'])
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








from .statistics import Statistics

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



class OfficeEventViewSet(viewsets.ReadOnlyModelViewSet):
    model = models.OfficeEvent
    serializer_class =  apiserializers.OfficeEventSerializer
    queryset = models.OfficeEvent.objects.all()
    pagination_class= pagination.LimitOffsetPagination

    def get_queryset(self):
        """
        By default, filter events on only new patient/new examinations
        No update events are given.
        'all' parameter is used to get all events
        """
        queryset = models.OfficeEvent.objects.all().order_by('-date')
        all_flag = self.request.query_params.get('all', None)
        if all_flag is None :
            queryset = queryset.exclude(clazz__exact = 'Patient', type__exact=2 )
        return queryset

class OfficeSettingsView(viewsets.ModelViewSet):
    model = models.OfficeSettings
    serializer_class = apiserializers.OfficeSettingsSerializer
    permission_classes = [IsStaffOrReadOnlyTargetUser]
    queryset = models.OfficeSettings.objects.all()

class TherapeutSettingsViewSet(viewsets.ModelViewSet):
    model = models.TherapeutSettings
    serializer_class = apiserializers.TherapeutSettingsSerializer
    permission_classes = [IsStaffOrTargetUser]
    queryset = models.TherapeutSettings.objects.all()

    @list_route(permission_classes=[AllowAny])
    def get_by_user(self, request):
        if not self.request.user.is_authenticated():
            raise Http404()
        settings = models.TherapeutSettings.objects.filter(user=self.request.user)
        if (len(settings)>0):
            return Response(apiserializers.TherapeutSettingsSerializer(settings[0]).data)
        else:
            return Response({})

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated():
            raise Http404()
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        if not self.request.user.is_authenticated():
            raise Http404()
        if not serializer.instance.user :
            serializer.save(user=self.request.user)
        serializer.save(user=serializer.instance.user)

class ExaminationCommentViewSet(viewsets.ModelViewSet):
    model = models.ExaminationComment
    serializer_class = apiserializers.ExaminationCommentSerializer
    queryset = models.ExaminationComment.objects.all()

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated():
            raise Http404()
        serializer.save(user=self.request.user,date=datetime.today())


from .file_integrator import Extractor, IntegratorHandler

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
            else :
                raise ValidationError("Missing patient file after analyze")
        logger.info("* Status after analyze is : %s "% (status))
        is_all_valid = True
        for f in status :
            (type_file, is_valid, is_empty, errors) = status[f]
            if type_file in ["examination", "patient"]:
                is_all_valid = is_all_valid and is_valid and not(is_empty)
        if is_all_valid:
            instance.status = 1
        else :
            instance.status = 0
        instance.analyze = status
        instance.save()


    @detail_route(methods=['POST','GET'])
    def integrate(self, request, pk=None):
        file_import_couple = self.get_object()
        integrator = IntegratorHandler()
        nb_line_patient = None
        nb_line_examination = None
        response = {'patient' : { 'imported' : 0, 'errors' : []} , 'examination': { 'imported' : 0, 'errors' : []}}
        with temp_disconnect_signal(
            signal=signals.post_save,
            receiver=receiver_newpatient,
            sender=models.Patient
            ):
            if file_import_couple.file_patient :
                # Start integration of each patient in the file
                ( nb_line_patient, errors_patient) = integrator.integrate(file_import_couple.file_patient)
                response['patient'] = {'imported' : nb_line_patient, 'errors': errors_patient}
        with temp_disconnect_signal(
            signal=signals.post_save,
            receiver=receiver_examination,
            sender=models.Examination
            ):
            if file_import_couple.file_examination :
                # Start integration of each examination in the file
                (nb_line_examination, errors_examination) = integrator.integrate(
                    file_import_couple.file_examination,  
                    file_additional=file_import_couple.file_patient, user=request.user)
                response['examination'] = {'imported' : nb_line_examination, 'errors': errors_examination}
        integrator.post_processing(files=[file_import_couple.file_patient, file_import_couple.file_examination])
        return Response( response ,
             status=status.HTTP_200_OK)


from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper

@csrf_protect
@never_cache
@staff_member_required   
def db_dump(request):
    import os,sys
    from cStringIO import StringIO

    from django.core import management
    buf = StringIO()
    management.call_command('dumpdata', exclude=['contenttypes', 'admin', 'auth.Permission'], stdout=buf)
    buf.seek(0)

    wrapper = FileWrapper(buf)
    response = HttpResponse(wrapper, content_type='application/binary')
    response['Content-Length'] = sys.getsizeof(buf)*8

    return response

from django.core.files.base import ContentFile
from django.core.files import File
import tempfile
from django.core.management import call_command

@csrf_protect
@maintenance_available()
def load_dump(request):
    #Retrieve the content of the file uploaded.
    try:
        if('file' in request.FILES.keys() ):
            logger.info("Load a dump from a sent file.")
            # Write the received file into a file into settings.FIXTURE_DIRS
            file_content = ContentFile(request.FILES['file'].read())
            filename = 'load_dump.json'
            fixture = os.path.join(tempfile.gettempdir(), filename)
            tmp_dump = open(fixture, 'w')
            f = File(tmp_dump)
            f.write(file_content.read())
            f.close()
            logger.info("Dump file was persisted for future loading.")
            receivers_senders = [(receiver_examination, models.Examination), (receiver_newpatient, models.Patient)]

            with block_disconnect_all_signal(
                signal=signals.post_save,
                receivers_senders=receivers_senders
                ):
                logger.info("Signals were disactivated, perform clearing of the database")
                call_command('flush', interactive=False, load_initial_data=False)
                # It means that the settings.FIXTURE_DIRS should be set in settings
                previous = settings.FIXTURE_DIRS
                settings.FIXTURE_DIRS = [tempfile.gettempdir()]
                # And when loading dumps, write the file into this directory with the name : load_dump.json
                logger.info("Load the fixture from path : %s "% (fixture))
                call_command('loaddata', fixture)
                # Delete the fixture
                logger.info("Clearing the fixture")
                os.remove(fixture)
                settings.FIXTURE_DIRS = previous
                logger.info("Could restore signals")
            logger.info("end of reloading.")
            return HttpResponse(content=u'reloaded')
        else :
            return HttpResponse()
    except :
        return HttpResponse(content=_(u'This archive file seems to be incorrect. Impossible to load it.'), status=412)
    