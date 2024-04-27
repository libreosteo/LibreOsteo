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
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView

from django.contrib import admin

admin.autodiscover()

from libreosteoweb.api import views

from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from django.views.generic.base import TemplateView
from libreosteoweb.api import displays

# Routers provide an easy way of automatically determining the URL conf
router = routers.SimpleRouter(trailing_slash=False)
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
router.register(r'office-users', views.UserOfficeViewSet, 'OfficeUser')
router.register(r'file-import', views.FileImportViewSet)
router.register(r'patient-documents', views.PatientDocumentViewSet,
                'PatientDocuments')
router.register(r'paiment-mean', views.PaimentMeanViewSet, 'PaimentMean')

urlpatterns = [
    # Examples:
    re_path(r'^$', displays.display_index),
    re_path(r'^api/', include(format_suffix_patterns(router.urls))),
    re_path(r'^accounts/login/$',
            LoginView.as_view(
                template_name='account/login.html',
                extra_context={'demonstration': settings.DEMONSTRATION}),
            name='login'),
    re_path(r'^accounts/logout/$',
            LogoutView.as_view(
                template_name='account/login.html',
                extra_context={'demonstration': settings.DEMONSTRATION}),
            name="logout"),
    re_path(r'^accounts/create-admin/$',
            views.CreateAdminAccountView.as_view(),
            name='accounts-create-admin'),
    re_path(r'^install/$', views.InstallView.as_view(), name='install'),
    re_path(r'^api-auth/',
            include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'^api/statistics[/]?$',
            views.StatisticsView.as_view(),
            name='statistics_view'),
    re_path(r'^api/patients/(?P<patient>.+)/documents$',
            views.PatientDocumentViewSet.as_view({'get': 'list'}),
            name="patient_document_view"),
    re_path(r'^myuserid',
            TemplateView.as_view(template_name='account/myuserid.html')),
    re_path(r'', include('libreosteoweb.urls')),
    re_path(r'^internal/dump.json', views.DbDump.as_view(), name='db_dump'),
    re_path(r'^internal/restore', views.LoadDump.as_view(), name='load_dump'),
    re_path(r'^internal/rebuild_index',
            views.RebuildIndex.as_view(),
            name="rebuild_index"),

    # Serve web-view
    re_path(r'^web-view/partials/patient-detail', displays.display_patient),
    re_path(r'^web-view/partials/doctor-selector', displays.select_doctor),
    re_path(r'^web-view/partials/doctor-modal', displays.display_doctor),
    re_path(r'^web-view/partials/add-patient', displays.display_newpatient),
    re_path(r'^web-view/partials/examinations-timeline',
            displays.display_examination_timeline),
    re_path(r'^web-view/partials/examination', displays.display_examination),
    re_path(r'^web-view/partials/search-result',
            views.SearchViewHtml(),
            name='search_view'),
    re_path(r'^web-view/partials/user-profile', displays.display_userprofile),
    re_path(r'^web-view/partials/dashboard', displays.display_dashboard),
    re_path(r'^web-view/partials/officeevent', displays.display_officeevent),
    re_path(r'^web-view/partials/invoice-modal', displays.display_invoicing),
    re_path(r'^web-view/partials/add-user-modal', displays.display_adduser),
    re_path(r'^web-view/partials/set-password-modal',
            displays.display_setpassword),
    re_path(r'^web-view/partials/office-settings$',
            displays.display_officesettings),
    re_path(r'^web-view/partials/import-file$', displays.display_import_files),
    re_path(r'^web-view/partials/rebuild-index$',
            displays.display_rebuild_index),
    re_path(r'^web-view/partials/filemanager$', displays.display_file_manager),
    re_path(r'^web-view/partials/restore$', displays.display_restore),
    re_path(r'^web-view/partials/register$',
            displays.display_register,
            name='accounts-register'),
    re_path(r'^web-view/partials/invoice-list$', displays.display_invoices),
    re_path(r'^invoice/(?P<invoiceid>\d+)$',
            views.InvoiceViewHtml.as_view(),
            name="invoice_view"),
    re_path(r'^web-view/partials/confirmation', displays.display_confirmation),
    re_path(
        r'^zipcode_lookup/',
        include(('zipcode_lookup.urls', 'zipcode_lookup'),
                namespace='zipcode-lookup')),
    re_path(r'^files/', include('protected_media.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.views.i18n import JavaScriptCatalog

js_info_dict = {'domain': 'djangojs', 'packages': ('libreosteoweb', )}

urlpatterns += [
    re_path(r'^jsi18n/$',
            JavaScriptCatalog.as_view(domain='djangojs',
                                      packages=[
                                          'libreosteoweb',
                                      ]),
            name='javascript-catalog'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
