# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^all/$', views.index, name='propeller_index'),
]
