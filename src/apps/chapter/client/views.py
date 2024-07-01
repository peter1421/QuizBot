# views.py


from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required  # Django的内置登录装饰器

from apps.chapter.models import Chapter


def index_ui(request):
    content = {}
    return render(
        request,
        "client/chapter/index_ui.html",
        context=content,
    )

@login_required
def index(request):
    # Fetch all chapters using the custom manager
    chapters = Chapter.objects.get_all_chapters()
    content = {
        'chapters': chapters  # Add chapters to the context dictionary
    }
    return render(
        request,
        "client/chapter/index.html",
        context=content,
    )
