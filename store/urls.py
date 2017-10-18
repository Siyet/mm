# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.ProductList, name='ProductList'),

    # url(r'^set_product/$', views.set_product),
    url(r'^prices_update/$', views.update_prices),
    url(r'^for_yandex/$', views.get_products_yml),
    url(r'^(?P<category_slug>[-\w]+)/$', views.ProductList, name='ProductListByCategory'),
    url(r'^(?P<category_slug>[-\w]+)/(?P<id>\d+)/$', views.ProductDetail, name='ProductDetail'),
]
