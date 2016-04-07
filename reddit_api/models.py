from django.contrib.auth.models import User
from django.db import models
from django.utils.safestring import mark_safe


class Reddit(models.Model):
    title = models.CharField(max_length=511)
    display_name = models.CharField(max_length=511)
    description = models.TextField()
    over18 = models.BooleanField()
    public_description = models.TextField()
    date_created = models.DateTimeField()
    url = models.CharField(max_length=1023, primary_key=True)
    subscribers = models.DecimalField(max_digits=10, decimal_places=0)
    banner_image = models.URLField(blank=True)
    image = models.ForeignKey("RedditImage", null=True, blank=True, related_name="shown_image")

    def get_html_link(self):
        return mark_safe("<a href={}>{}</a>".format("https://reddit.com" + self.url, self.url))

    def display_image_url(self):
        return mark_safe("<img src='{}' height=70 />".format(self.get_image_url()))

    def get_image_url(self):
        return self.image.url if self.image is not None and self.image.url is not "self" and self.image.url is not "" else "http://placehold.it/400x300"

    def __unicode__(self):
        return self.display_name


class RedditImage(models.Model):
    url = models.URLField()
    reputation = models.IntegerField()
    post = models.URLField(blank=True)
    reddit = models.ForeignKey("Reddit", related_name="all_images", null=True)

    def __unicode__(self):
        return mark_safe(u"<img src='{}' height=30 /> ({})".format(self.url, self.reputation))


class FollowedReddit(models.Model):
    user = models.ForeignKey(User)
    reddit = models.ForeignKey(Reddit)
    counter = models.BigIntegerField(default=0)

    def __unicode__(self):
        return "{} ({})".format(self.reddit.display_name, self.user)
