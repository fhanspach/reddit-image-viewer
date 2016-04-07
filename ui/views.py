from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import render, redirect
from reddit_api.models import Reddit, FollowedReddit
from reddit_api.imports import import_reddits as reddit_importer
from requests import HTTPError


def index_dummy(request):
    return redirect(to=list_dummy)


def all_reddits_list_dummy(request):
    data = [].append(r.url for r in Reddit.objects.all())
    data = {'data': data}
    return JsonResponse(data)


def list_dummy(request):
    popular_reddits = Reddit.objects.order_by('-subscribers')
    followed_reddits = get_followed_reddits(request)
    context = {
        'popular_reddits': popular_reddits.exclude(pk__in=followed_reddits)[0:50],
        "my_reddits": followed_reddits
    }
    return render(request, 'ui/list.html', context=context)


def get_followed_reddits(request):
    if request.user.is_authenticated():
        followed_reddits = Reddit.objects.filter(followedreddit__user=request.user).order_by("-followedreddit__counter")
    else:
        followed_reddits = []
    return followed_reddits


def import_reddits(request):
    if "reddit_url" in request.GET:
        reddit_importer.RedditImporter().import_single_reddit(request.GET["reddit_url"])
    else:
        reddit_importer.RedditImporter().import_all_reddits()
    return render(request, 'ui/list.html')


def view_reddit(request, url_fragment):
    url = "/r/{}/".format(url_fragment)
    try:
        reddit = Reddit.objects.get(url=url)
    except Reddit.DoesNotExist:
        try:
            reddit = reddit_importer.RedditImporter().import_single_reddit(url)
        except Http404:
            return render(request, "ui/index.html", context={"error_title": "Not Found",
                                                             "error_msg": "The reddit {} was not found :(".format(
                                                                     url_fragment)})
        except KeyError:
            return render(request, "ui/index.html", context={"error_title": "Error",
                                                             "error_msg": "There was an error while accessing {} :(".format(
                                                                     url_fragment)})
        except HTTPError:
            return render(request, "ui/index.html", context={"error_title": "Error",
                                                             "error_msg": "There was an error while accessing {} :(".format(
                                                                     url_fragment)})

    reddit_is_followed = False if not request.user.is_authenticated() \
        else FollowedReddit.objects.filter(user=request.user, reddit=reddit).exists()

    if reddit_is_followed:
        followed = FollowedReddit.objects.get(user=request.user, reddit=reddit)
        followed.counter += 1
        followed.save()

    context = {
        'reddit': reddit,
        'followed': reddit_is_followed,
        "my_reddits": get_followed_reddits(request)
    }
    return render(request, "ui/index.html", context=context)
