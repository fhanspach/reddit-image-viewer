from django.contrib import admin
from reddit_api import models
# Register your models here.


class RedditAdmin(admin.ModelAdmin):
    class Meta:
        model = models.Reddit
    list_display = ['title', 'subscribers', 'over18', 'get_html_link']
    search_fields = ['title']


admin.site.register(models.Reddit, RedditAdmin)
