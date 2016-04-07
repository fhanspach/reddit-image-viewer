from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^(?P<reddit_name>.+)/recommended/$', views.get_recommended),
    url(r'^(?P<reddit_name>.+)/follow/$', views.follow),
    url(r'^(?P<reddit_name>.+)/unfollow/$', views.unfollow),
    url(r'^(?P<reddit_name>.+)/$', views.get_submissions),
]
