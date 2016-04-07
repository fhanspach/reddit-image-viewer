from django.contrib import admin
from reddit_api import models
# Register your models here.
from reddit_api.models import RedditImage, FollowedReddit


class RedditAdmin(admin.ModelAdmin):
    class Meta:
        model = models.Reddit
    list_display = ['title', 'subscribers', 'over18', 'display_image_url']
    search_fields = ['title']


admin.site.register(models.Reddit, RedditAdmin)
admin.site.register(RedditImage)
admin.site.register(FollowedReddit)
