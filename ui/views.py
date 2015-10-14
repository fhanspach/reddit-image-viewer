from django.shortcuts import render


def index_dummy(request):
    return render(request, "ui/index.html")


def list_dummy(request):
    return render(request, 'ui/list.html')


def import_reddits(request):
    from reddit_api.imports import import_reddits as reddit_importer

    if "reddit_url" in request.GET:
        reddit_importer.RedditImporter().import_single_reddit(request.GET["reddit_url"])
    else:
        reddit_importer.RedditImporter().import_all_reddits()
    return render(request, 'ui/list.html')