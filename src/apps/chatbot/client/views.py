# views.py


from apps.chapter.models import Chapter
from apps.chatbot.backend import get_chatbot_response
from apps.chatbot.models import ChatMessage, Chatbot
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods
from apps.chatbot.backend import create_threads_id

from QuizBot.middleware import chatbot_owner_required
from apps.chatbot.serializers import ChatMessageSerializer


def index(request, chapter_id=None):
    user = request.user if request.user.is_authenticated else None

    chapter = get_object_or_404(Chapter, id=chapter_id) if chapter_id else None
    if chapter is not None:
        chatbot, created = Chatbot.objects.get_or_create(
            account=user, chapter=chapter)
        if created:
            now_thread=create_threads_id()
            chatbot.now_thread = now_thread
            chatbot.save()
    context = {
        "chatbot": chatbot,
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
##TODO:回傳失敗訊息
@require_http_methods(["POST"])
def api_chat_with_bot(request):
    if request.method == 'POST':
        user_message = request.POST.get('message')
        chatbot_id = request.POST.get('chatbot_id')
        chatbot=Chatbot.objects.find_chatbot_by_id(chatbot_id)
        chatbot_response = get_chatbot_response(user_message,chatbot)
        serializer = ChatMessageSerializer(chatbot_response)
        return JsonResponse({'data': serializer.data})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def api_get_message_by_chatbot_id(request):
    chatbot_id=request.GET.get('chatbot_id')
    chatbot=Chatbot.objects.find_chatbot_by_id(chatbot_id)
    now_thread=chatbot.now_thread
    chat_messages=ChatMessage.objects.find_by_thread_id(now_thread)
    serializer = ChatMessageSerializer(chat_messages, many=True)
    return JsonResponse(serializer.data, safe=False)