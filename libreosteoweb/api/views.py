from rest_framework import viewsets, filters
from rest_framework.filters import DjangoFilterBackend
import django_filters
from libreosteoweb.models import RegularDoctor, Patient, Examination
from rest_framework.decorators import action, detail_route
from libreosteoweb.api.serializers import PatientSerializer, ExaminationSerializer
from rest_framework.response import Response

# Create your views here.

# ViewSets define the view behavior.
class SearchFilter(filters.SearchFilter):
    search_param = 'q'


class PatientViewSet(viewsets.ModelViewSet):
    model = Patient
    filter_backends = (SearchFilter,)
    search_fields = ('family_name', 'original_name', 'first_name')

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
