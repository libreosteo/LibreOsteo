from __future__ import unicode_literals
from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^zipcode_lookup/(?P<zipcode>\d{5})$', views.zipcode_lookup),
]
