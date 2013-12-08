from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static


from django.contrib import admin
admin.autodiscover()

from libreosteoweb.models import RegularDoctor, Children, Patient
from rest_framework import viewsets, routers
from django.views.generic.base import TemplateView



# ViewSets define the view behavior.


class PatientViewSet(viewsets.ModelViewSet):
    model = Patient


class RegularDoctorViewSet(viewsets.ModelViewSet):
    model = RegularDoctor


# Routers provide an easy way of automatically determining the URL conf
router = routers.SimpleRouter()
router.register(r'patients', PatientViewSet)
router.register(r'doctors', RegularDoctorViewSet)


urlpatterns = patterns('',
    # Examples:
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^api/', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'account/login.html'}, name='accounts-login'),
    url(r'^accounts/logout', 'django.contrib.auth.views.logout', {'template_name' : 'account/login.html'}, name="accounts-logout"),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

