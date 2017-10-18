# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^create/$', views.OrderCreate, name='OrderCreate'),
    url(r'^torg12/(?P<id>\d+)/$', views.get_torg12)
]