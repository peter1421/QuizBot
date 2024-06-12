# views.py


from apps.account.models import SiteUser
from apps.chapter.models import Chapter
from apps.chatbot.models import Chatbot
from django.shortcuts import get_object_or_404, render
from django.contrib import messages

def index(request, chapter_id=None):
    user = request.user if request.user.is_authenticated else None

    chapter = get_object_or_404(Chapter, id=chapter_id) if chapter_id else None

    chatbot = None
    if chapter is not None:
        chatbot = Chatbot.objects.get_or_create_by_account_and_chapter(user, chapter)
        messages.success(request, chatbot)
        # thread_id = get_threads_id(chapter)

    context = {
        "chatbot": chatbot,
        "user": user,
        "chapter": chapter,
    }
    return render(
        request,
        "client/chatbot/index.html", context=context,
    )


def index_ui(request):
    content = {}
    return render(
        request,
        "client/chatbot/index_ui.html", context=content,
    )
