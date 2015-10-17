from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^image/$', views.get_image),
    url(r'(?P<reddit_name>.*)/$', views.get_submissions),
]