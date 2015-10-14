from django.conf.urls import url
from . import views

__author__ = 'felixhanspach'

urlpatterns = [
    url(r'list/$', views.list_dummy),
    url(r'import_reddits/$', views.import_reddits),
    url(r'$', views.index_dummy),


]