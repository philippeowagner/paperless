# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^all/$', views.index, name='paperless_ui_index'),
    url(r'^view/(?P<checksum>\w+)/$', views.doc_viewer, name='paperless_ui_view'),
]
