from django.conf.urls import url
from . import views

__author__ = 'felixhanspach'

urlpatterns = [
    url(r'list/$', views.list_dummy),
    url(r'$', views.index_dummy),

]