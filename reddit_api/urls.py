from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'(?P<reddit_name>.*)/recommended/$', views.get_recommended),
    url(r'(?P<reddit_name>.*)/$', views.get_submissions),
]