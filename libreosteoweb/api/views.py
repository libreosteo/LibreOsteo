from __future__ import unicode_literals
from rest_framework import viewsets, filters
from rest_framework.filters import DjangoFilterBackend
import django_filters
from libreosteoweb.models import RegularDoctor, Patient, Examination
from rest_framework.decorators import action, detail_route
from libreosteoweb.api.serializers import PatientSerializer, ExaminationSerializer
from rest_framework.response import Response
from haystack.query import SearchQuerySet
from django.core import serializers
from django.http import HttpResponse
from django.views.generic import View
from django.core import serializers
from haystack.utils import Highlighter
from haystack.views import SearchView
from libreosteoweb.api.exceptions import AlreadyExistsException
import json
import logging

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

    def create(self, request, *args, **kwargs):
        found = Patient.objects.filter(family_name__iexact=request.DATA['family_name'])\
            .filter( first_name__iexact=request.DATA['first_name'] )\
            .filter( birth_date__iexact=request.DATA['birth_date'] )\
            .exists()

        if ( not found):
            return super(PatientViewSet, self).create(request, *args, **kwargs)
        else :
            raise AlreadyExistsException

    @detail_route(methods=['GET'])
    def examinations(self, request, pk=None):
        current_patient = self.get_object()
        examinations = Examination.objects.filter(patient=current_patient).order_by('-date')
        return Response(ExaminationSerializer(examinations, many=True).data)



class RegularDoctorViewSet(viewsets.ModelViewSet):
    model = RegularDoctor


class ExaminationViewSet(viewsets.ModelViewSet):
    model = Examination

    def pre_save(self, obj):
        if not self.request.user.is_authenticated():
            raise Http404()

        if not obj.therapeut:
            setattr(obj, 'therapeut', self.request.user)
