from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^list/$', views.list_dummy),
    url(r'^import_reddits/$', views.import_reddits),
    url(r'^api/reddits/$', views.all_reddits_list_dummy),
    url(r'^r/(?P<url_fragment>.+)/$', views.view_reddit),

    url(r'^$', views.index_dummy),
]