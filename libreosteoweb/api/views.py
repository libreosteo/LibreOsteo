from rest_framework import viewsets, filters
from rest_framework.filters import DjangoFilterBackend
import django_filters
from libreosteoweb.models import RegularDoctor, Patient
from libreosteoweb.api.serializers import PatientSerializer


# Create your views here.

# ViewSets define the view behavior.
class SearchFilter(filters.SearchFilter):
    search_param = 'q'


class PatientViewSet(viewsets.ModelViewSet):
    model = Patient
    serializer_class = PatientSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('family_name', 'original_name', 'first_name')



class RegularDoctorViewSet(viewsets.ModelViewSet):
    model = RegularDoctor
