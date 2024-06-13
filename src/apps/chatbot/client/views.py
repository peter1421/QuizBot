# views.py


from apps.chapter.models import Chapter
from apps.chatbot.backend import get_chatbot_response
from apps.chatbot.models import Chatbot
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from QuizBot.middleware import chatbot_owner_required


def index(request, chapter_id=None):
    user = request.user if request.user.is_authenticated else None

    chapter = get_object_or_404(Chapter, id=chapter_id) if chapter_id else None

    chatbot = None
    if chapter is not None:
        chatbot = Chatbot.objects.get_or_create_by_account_and_chapter(user, chapter)
        # messages.success(request, chatbot)

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

def api_chat_with_bot(request):
    if request.method == 'POST':
        user_message = request.POST.get('message')
        chatbot_id = request.POST.get('chatbot_id')
        chatbot=Chatbot.objects.find_chatbot_by_id(chatbot_id)
        response_message = get_chatbot_response(user_message,chatbot.now_thread,chatbot.chapter)
        return JsonResponse({'message': response_message})
    return JsonResponse({'error': 'Invalid request'}, status=400)
