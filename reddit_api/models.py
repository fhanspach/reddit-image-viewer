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
    banner_image = models.URLField()
    image = models.ForeignKey("RedditImage", null=True, blank=True, related_name="shown_image")

    def get_html_link(self):
        return mark_safe("<a href={0}>{1}</a>".format("https://reddit.com" + self.url, self.url))

    def display_image_url(self):
        return mark_safe("<img src='{0}' height=70 />".format(self.get_image_url()))

    def get_image_url(self):
        return self.image.url if self.image is not None and self.image.url is not "self" and self.image.url is not "" else "http://placehold.it/400x300"


class RedditImage(models.Model):
    url = models.URLField()
    reputation = models.IntegerField()
    post = models.URLField(blank=True, null=True)
    reddit = models.ForeignKey("Reddit", related_name="all_images", null=True)

    def __unicode__(self):
        return mark_safe(u"<img src='{0}' height=30 /> ({1})".format(self.url, self.reputation))
