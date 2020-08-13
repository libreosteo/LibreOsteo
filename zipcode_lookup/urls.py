from __future__ import unicode_literals
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^zipcode_lookup/(?P<zipcode>\d{5})$', views.zipcode_lookup),
]
