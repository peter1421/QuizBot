# views.py


from django.shortcuts import render

from apps.accounts.models import SiteUser
from apps.chapter.models import Chapter


def index(request, chapter_id=None):
    if request.user.is_authenticated:
        user=SiteUser.objects.get(id=request.user.id)
    else:
        user = None

    if chapter_id is None:
        chapter = None
    else:
        chapter = Chapter.objects.get(id=chapter_id)

    context = {
        'user': user,
        'chapter': chapter,
    }
    return render(
        request,
        "client/chatbot/index.html",context=context,
    )

def index_ui(request):
    content={}
    return render(
        request,
        "client/chatbot/index_ui.html",context=content,
    )