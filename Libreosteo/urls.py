from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static


from django.contrib import admin
admin.autodiscover()

from libreosteoweb.api.views import PatientViewSet, RegularDoctorViewSet, ExaminationViewSet
from rest_framework import  routers
from django.views.generic.base import TemplateView
from libreosteoweb.api import displays


# Routers provide an easy way of automatically determining the URL conf
router = routers.SimpleRouter(trailing_slash = False)
router.register(r'patients', PatientViewSet)
router.register(r'doctors', RegularDoctorViewSet)
router.register(r'examinations', ExaminationViewSet)

urlpatterns = patterns('',
    # Examples:
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^api/', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'account/login.html'}, name='accounts-login'),
    url(r'^accounts/logout', 'django.contrib.auth.views.logout', {'template_name' : 'account/login.html'}, name="accounts-logout"),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Serve web-view
    url(r'^web-view/partials/patient-detail', displays.display_patient),
    url(r'^web-view/partials/doctor-modal', displays.display_doctor),
    url(r'^web-view/partials/add-patient', displays.display_newpatient),
    url(r'^web-view/partials/examinations-timeline', displays.display_examination_timeline)
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

