from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static


from django.contrib import admin
admin.autodiscover()

from libreosteoweb.api import views

from rest_framework import  routers
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

urlpatterns = patterns('',
    # Examples:
    url(r'^$', displays.display_index ),
    url(r'^api/', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'account/login.html', 'extra_context' : {'demonstration' : settings.DEMONSTRATION}}, name='accounts-login'),
    url(r'^accounts/logout', 'django.contrib.auth.views.logout', {'template_name' : 'account/login.html', 'extra_context' : {'demonstration' : settings.DEMONSTRATION}}, name="accounts-logout"),
    url(r'^accounts/create-admin/$', views.create_admin_account, name='accounts-create-admin'),
    url(r'^install/$', views.install, name='install'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/statistics[/]?$', views.StatisticsView.as_view(), name='statistics_view'),
    url(r'^api/patients/(?P<patient>.+)/documents$', views.PatientDocumentViewSet.as_view({'get' : 'list'}), name="patient_document_view"),
    url(r'^myuserid', TemplateView.as_view(template_name='account/myuserid.html')),
    url(r'^internal/dump.json', views.db_dump, name='db_dump'),
    url(r'^internal/restore', views.load_dump, name='load_dump'),
    url(r'^internal/rebuild_index', views.rebuild_index, name="rebuild_index"),

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
    url(r'^invoice/(?P<invoiceid>\d+)$', views.InvoiceViewHtml.as_view(), name="invoice_view"),
    url(r'^web-view/partials/confirmation', displays.display_confirmation),
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


from django.views.i18n import javascript_catalog

js_info_dict = {
    'domain' : 'djangojs',
    'packages' : ('libreosteoweb',)
}

urlpatterns += patterns('',
    (r'^jsi18n/$', javascript_catalog, js_info_dict),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
