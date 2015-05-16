from django.conf.urls import url
from . import views

__author__ = 'felixhanspach'

urlpatterns = [
    url(r'$', views.index_dummy)
]