from django.shortcuts import render


def index_dummy(request):
    return render(request, "image_viewer/index.html")