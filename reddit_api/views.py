from django.http import JsonResponse
from django.conf import settings
from django.template import RequestContext
from django.template.loader import render_to_string
import praw
from reddit_api.models import Reddit, RedditImage
from requests import ConnectionError

r = praw.Reddit(user_agent=settings.REDDIT_API_USER_AGENT)


def get_submissions(request, reddit_name):
    reddit = Reddit.objects.get(url="/r/{}/".format(reddit_name))
    reddit_image = reddit.image
    if reddit_image is None:
        reddit_image = RedditImage(url="http://placehold.it/400x300", reputation=0)
        reddit_image.save()
        reddit.image = reddit_image
        reddit.save()

    try:
        api_submissions = r.get_subreddit(reddit_name).get_new(
            limit=100, params={}
        )
    except ConnectionError:
        api_submissions = []

    entry_list = []
    for submission in api_submissions:
        entry_list.append(submission)
        if reddit_image.reputation < submission.ups:
            reddit_image.url = submission.thumbnail
            reddit_image.post = submission.permalink
            reddit_image.reddit = reddit
            reddit_image.reputation = submission.ups

    context = {
        'submissions': entry_list
    }
    html = render_to_string('reddit_api/submissions.html', RequestContext(request, context))
    reddit_image.save()
    return JsonResponse({"html": html})
