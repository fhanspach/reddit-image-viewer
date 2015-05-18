from django.contrib.auth.models import User as AuthUser
from django.db import models
from django.utils.safestring import mark_safe


class SavedReddit(models.Model):
    title = models.CharField(max_length=1047)


class RedditImage(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    reddit = models.ForeignKey("SavedReddit")
    image_url = models.CharField(max_length=2047)
    is_nsfw = models.BooleanField()

    @property
    def image_html(self):
        return mark_safe("<img src='{}' height='50px'>".format(self.image_url))

    def __unicode__(self):
        return u"{} ({})".format(self.reddit, self.image_url)


class User(models.Model):
    user = models.ForeignKey(AuthUser, null=True, blank=True)
    followed_reddits = models.ManyToManyField(SavedReddit)