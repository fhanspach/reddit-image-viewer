from django.shortcuts import render
from setuptools.command.sdist import re_finder


def index_dummy(request):
    return render(request, "image_viewer/index.html")


def list_dummy(request):
    return render(request, 'image_viewer/list.html')