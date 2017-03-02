# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import url, static, include, patterns


urlpatterns = patterns('propeller.views',
    url(r'^$', view='index', name='propeller_index'),
)
