
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
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView,LogoutView


from django.contrib import admin
admin.autodiscover()

from libreosteoweb.api import views

from rest_framework import  routers
from rest_framework.urlpatterns import format_suffix_patterns
from django.views.generic.base import TemplateView
from libreosteoweb.api import displays


# Routers provide an easy way of automatically determining the URL conf
router = routers.SimpleRouter(trailing_slash = False)
router.register(r'patients', views.PatientViewSet)
router.register(r'doctors', views.RegularDoctorViewSet)
router.register(r'examinations', views.ExaminationViewSet)
router.register(r'documents', views.DocumentViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'events', views.OfficeEventViewSet)
router.register(r'invoices', views.InvoiceViewSet)
router.register(r'settings', views.OfficeSettingsView)
router.register(r'profiles', views.TherapeutSettingsViewSet)
router.register(r'comments', views.ExaminationCommentViewSet)
router.register(r'office-users', views.UserOfficeViewSet)
router.register(r'file-import', views.FileImportViewSet)
router.register(r'patient-documents', views.PatientDocumentViewSet, 'PatientDocuments')
router.register(r'paiment-mean', views.PaimentMeanViewSet, 'PaimentMean')

urlpatterns = [
    # Examples:
    url(r'^$', displays.display_index ),
    url(r'^api/', include(format_suffix_patterns(router.urls))),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', LoginView.as_view(template_name='account/login.html',extra_context={'demonstration' : settings.DEMONSTRATION}), name='login'),
    url(r'^accounts/logout', LogoutView.as_view(template_name='account/login.html',extra_context={'demonstration' : settings.DEMONSTRATION}), name="logout"),
    url(r'^accounts/create-admin/$', views.CreateAdminAccountView.as_view(), name='accounts-create-admin'),
    url(r'^install/$', views.InstallView.as_view(), name='install'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/statistics[/]?$', views.StatisticsView.as_view(), name='statistics_view'),
    url(r'^api/patients/(?P<patient>.+)/documents$', views.PatientDocumentViewSet.as_view({'get' : 'list'}), name="patient_document_view"),
    url(r'^myuserid', TemplateView.as_view(template_name='account/myuserid.html')),
    url(r'^internal/dump.json', views.DbDump.as_view(), name='db_dump'),
    url(r'^internal/restore', views.LoadDump.as_view(), name='load_dump'),
    url(r'^internal/rebuild_index', views.RebuildIndex.as_view(), name="rebuild_index"),

    # Serve web-view
    url(r'^web-view/partials/patient-detail', displays.display_patient),
    url(r'^web-view/partials/doctor-modal', displays.display_doctor),
    url(r'^web-view/partials/add-patient', displays.display_newpatient),
    url(r'^web-view/partials/examinations-timeline', displays.display_examination_timeline),
    url(r'^web-view/partials/examination', displays.display_examination),
    url(r'^web-view/partials/search-result', views.SearchViewHtml(), name='search_view'),
    url(r'^web-view/partials/user-profile', displays.display_userprofile),
    url(r'^web-view/partials/dashboard', displays.display_dashboard),
    url(r'^web-view/partials/officeevent', displays.display_officeevent),
    url(r'^web-view/partials/invoice-modal', displays.display_invoicing),
    url(r'^web-view/partials/add-user-modal', displays.display_adduser),
    url(r'^web-view/partials/set-password-modal', displays.display_setpassword),
    url(r'^web-view/partials/office-settings$', displays.display_officesettings),
    url(r'^web-view/partials/import-file$', displays.display_import_files),
    url(r'^web-view/partials/rebuild-index$', displays.display_rebuild_index),
    url(r'^web-view/partials/filemanager$', displays.display_file_manager),
    url(r'^web-view/partials/restore$', displays.display_restore),
    url(r'^web-view/partials/register$', displays.display_register, name='accounts-register'),
    url(r'^web-view/partials/invoice-list$', displays.display_invoices),

    url(r'^invoice/(?P<invoiceid>\d+)$', views.InvoiceViewHtml.as_view(), name="invoice_view"),
    url(r'^web-view/partials/confirmation', displays.display_confirmation),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


from django.views.i18n import JavaScriptCatalog

js_info_dict = {
    'domain' : 'djangojs',
    'packages' : ('libreosteoweb',)
}

urlpatterns += [
    url(r'^jsi18n/$', JavaScriptCatalog.as_view(domain='djangojs', packages=['libreosteoweb',]), name='javascript-catalog'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
