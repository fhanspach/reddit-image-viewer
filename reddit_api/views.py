from django.http import JsonResponse
from django.conf import settings
from django.template import RequestContext
from django.template.loader import render_to_string
import praw
from reddit_api.models import Reddit, RedditImage
from requests import ConnectionError

r = praw.Reddit(user_agent=settings.REDDIT_API_USER_AGENT)


def _send_request(reddit_name, display='hot', period=None):
    if display == 'new':
        request_submissions = r.get_subreddit(reddit_name).get_new
    elif display == 'hot' or display == "":
        request_submissions = r.get_subreddit(reddit_name).get_hot
    elif display == 'top':
        if period == "week" or period is None:
            request_submissions = r.get_subreddit(reddit_name).get_top
        elif period == "month":
            request_submissions = r.get_subreddit(reddit_name).get_top_from_month
        elif period == "year":
            request_submissions = r.get_subreddit(reddit_name).get_top_from_year
        elif period == "all":
            request_submissions = r.get_subreddit(reddit_name).get_top_from_all
        elif period == "day":
            request_submissions = r.get_subreddit(reddit_name).get_top_from_day
        else:
            raise ValueError("Period parameter unknown")
    else:
        raise ValueError("Display Parameter must be one of 'hot', 'top' or 'new'")

    try:
        api_submissions = request_submissions(limit=100, params={})
    except ConnectionError:
        api_submissions = []
    return api_submissions


def get_submissions(request, reddit_name):
    reddit = Reddit.objects.get(url="/r/{}/".format(reddit_name))
    reddit_image = reddit.image
    if reddit_image is None:
        reddit_image = RedditImage(url="http://placehold.it/400x300", reputation=0)
        reddit_image.save()
        reddit.image = reddit_image
        reddit.save()

    api_submissions = _send_request(reddit_name, display=request.GET.get('display', 'hot'),
                                    period=request.GET.get('period', None))

    entry_list = []
    for submission in api_submissions:
        entry_list.append(submission)
        if reddit_image.reputation < submission.ups:
            reddit_image.url = submission.thumbnail
            reddit_image.post = submission.permalink
            reddit_image.reddit = reddit
            reddit_image.reputation = submission.ups

    context = {
        'submissions': entry_list,
        'reddit': reddit
    }
    html = render_to_string('reddit_api/submissions.html', RequestContext(request, context))
    reddit_image.save()
    return JsonResponse({"html": html})
