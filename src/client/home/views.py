# views.py

import os

from django.conf import settings
from django.contrib.auth.decorators import login_required  # Django的内置登录装饰器
from django.http import Http404, HttpResponse
from django.shortcuts import render


def index(request):
    return render(
        request,
        "client/home/index.html",
    )