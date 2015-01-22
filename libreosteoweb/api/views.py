from __future__ import unicode_literals
from rest_framework import viewsets, filters
from rest_framework.filters import DjangoFilterBackend
import django_filters
from libreosteoweb.models import RegularDoctor, Patient, Examination, OfficeEvent
from rest_framework.decorators import action, detail_route
from libreosteoweb.api.serializers import PatientSerializer, ExaminationSerializer, UserInfoSerializer, ExaminationInvoicingSerializer, OfficeEventSerializer
from rest_framework.response import Response
from haystack.query import SearchQuerySet
from django.core import serializers
from django.http import HttpResponse
from django.views.generic import View
from django.core import serializers
from haystack.utils import Highlighter
from haystack.views import SearchView
import json
import logging
from django.contrib.auth.models import User
from .permissions import IsStaffOrTargetUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Get an instance of a logger
logger = logging.getLogger(__name__)


class SearchViewJson(View):

    def get(self, request, *args, **kwargs):
        # Get the query
        search_query = self.request.GET['q']
        # Build the query set for result
        sqs = SearchQuerySet().auto_query(search_query)
        # Get the results only
        data_results = [ result.object for result in sqs ]

        json_data = serializers.serialize('json', data_results, fields=('family_name', 'first_name', 'original_name'))

        return HttpResponse(json_data, content_type='application/json')




class SearchViewHtml(SearchView):
    template = 'partials/search-result.html'
    results_per_page = 10






class PatientViewSet(viewsets.ModelViewSet):
    model = Patient

    @detail_route(methods=['GET'])
    def examinations(self, request, pk=None):
        current_patient = self.get_object()
        examinations = Examination.objects.filter(patient=current_patient).order_by('-date')
        return Response(ExaminationSerializer(examinations, many=True).data)

    def pre_save(self, obj):
        """ Set the user which perform the operation as the currently logged user"""
        if not self.request.user.is_authenticated():
            raise Http404()
        obj.set_user_operation(self.request.user)




class RegularDoctorViewSet(viewsets.ModelViewSet):
    model = RegularDoctor





class ExaminationViewSet(viewsets.ModelViewSet):
    model = Examination


    @detail_route(methods=['POST'])
    def close(self, request, pk=None):
        current_examination = self.get_object()
        serializer = ExaminationInvoicingSerializer(data=request.DATA)
        if serializer.is_valid():
            if serializer.data['status'] == 'notinvoiced':
                current_examination.status = Examination.EXAMINATION_NOT_INVOICED
                current_examination.status_reason = serializer.data['reason']
                current_examination.save()
            return Response({'invoicing':'try to execute the close'})
        else :
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def pre_save(self, obj):
        if not self.request.user.is_authenticated():
            raise Http404()

        if not obj.therapeut:
            setattr(obj, 'therapeut', self.request.user)




class UserViewSet(viewsets.ModelViewSet):
    model = User
    serializer_class =  UserInfoSerializer
    permission_classes = [IsStaffOrTargetUser]







from .statistics import Statistics

class StatisticsView(APIView):

    def get(self, request, *args, **kwargs):
        myStats = Statistics(*args, **kwargs)
        result = myStats.compute()
        response = Response(result, status=status.HTTP_200_OK)
        return response




class OfficeEventViewSet(viewsets.ReadOnlyModelViewSet):
    model = OfficeEvent
    serializer_class =  OfficeEventSerializer

    def get_queryset(self):
        """
        By default, filter events on only new patient/new examinations
        No update events are given.
        'all' parameter is used to get all events
        """
        queryset = OfficeEvent.objects.all()
        all_flag = self.request.QUERY_PARAMS.get('all', None)
        if all_flag is None :
            queryset = queryset.exclude(clazz__exact = 'Patient', type__exact=2 )
        return queryset