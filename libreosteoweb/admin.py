from django.contrib import admin

from libreosteoweb.models import RegularDoctor, Children, Patient, Examination


admin.site.register(RegularDoctor)
admin.site.register(Children)
admin.site.register(Patient)
admin.site.register(Examination)