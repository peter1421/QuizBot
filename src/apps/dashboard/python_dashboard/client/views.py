# views.py


from django.shortcuts import render
from django.contrib import messages

from apps.chapter.models import Chapter


def index_ui(request):
    content = {}
    return render(
        request,
        "client/chapter/index_ui.html",
        context=content,
    )


def index(request):
    content = {
    }
    messages.success(request, "測試")
    return render(
        request,
        "client/dashboard/python_dashboard/index.html",
        context=content,
    )
