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

    def get_html_link(self):
        return mark_safe("<a href={}>{}</a>".format("https://reddit.com" + self.url, self.url))
