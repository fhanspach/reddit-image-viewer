from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import render, redirect
from reddit_api.models import Reddit
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
    context = {
        'popular_reddits': popular_reddits[0:50]
    }
    return render(request, 'ui/list.html', context=context)


def import_reddits(request):
    if "reddit_url" in request.GET:
        reddit_importer.RedditImporter().import_single_reddit(request.GET["reddit_url"])
    else:
        reddit_importer.RedditImporter().import_all_reddits()
    return render(request, 'ui/list.html')


def view_reddit(request, url_fragment):
    url = "/r/{0}/".format(url_fragment)
    try:
        reddit = Reddit.objects.get(url=url)
    except Reddit.DoesNotExist:
        try:
            reddit = reddit_importer.RedditImporter().import_single_reddit(url)
        except Http404:
            return render(request, "ui/index.html", context={"error_title": "Not Found",
                                                             "error_msg": "The reddit {0} was not found :(".format(
                                                                 url_fragment)})
        except KeyError:
            return render(request, "ui/index.html", context={"error_title": "Error",
                                                             "error_msg": "There was an error while accessing {0} :(".format(
                                                                 url_fragment)})
        except HTTPError:
            return render(request, "ui/index.html", context={"error_title": "Error",
                                                             "error_msg": "There was an error while accessing {0} :(".format(
                                                                 url_fragment)})
    context = {
        'reddit': reddit,

        # TODO replace with template tag
        'popular_reddits': Reddit.objects.order_by('-subscribers')[0:10]
    }
    return render(request, "ui/index.html", context=context)