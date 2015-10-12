from django.shortcuts import render
from setuptools.command.sdist import re_finder


def index_dummy(request):
    return render(request, "ui/index.html")


def list_dummy(request):
    return render(request, 'ui/list.html')