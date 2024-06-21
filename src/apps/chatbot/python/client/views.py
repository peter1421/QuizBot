# views.py


from apps.chapter.models import Chapter
from apps.chatbot.python.client.backend import PythonChatbotHelper
from apps.chatbot.python.models import PythonChatbot, PythonChatMessage
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from apps.chatbot.python.serializers import PythonChatMessageSerializer


def index(request, chapter_id=None):
    user = request.user if request.user.is_authenticated else None

    chapter = get_object_or_404(Chapter, id=chapter_id) if chapter_id else None
    if chapter is not None:
        chatbot, created = PythonChatbot.objects.get_or_create(
            account=user, chapter=chapter)
        if created:
            chatbot_helper = PythonChatbotHelper(chatbot)
            now_thread=chatbot_helper.create_threads_id()
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
        chatbot=PythonChatbot.objects.find_chatbot_by_id(chatbot_id)
        chatbot_helper = PythonChatbotHelper(chatbot)
        chatbot_helper.get_chatbot_asscistant()
        
        chatbot_response = chatbot_helper.get_chatbot_response(user_message)
        serializer = PythonChatMessageSerializer(chatbot_response)
        return JsonResponse({'data': serializer.data})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def api_get_message_by_chatbot_id(request):
    chatbot_id=request.GET.get('chatbot_id')
    chatbot=PythonChatbot.objects.find_chatbot_by_id(chatbot_id)
    now_thread=chatbot.now_thread
    chat_messages=PythonChatMessage.objects.find_by_thread_id(now_thread)
    serializer = PythonChatMessageSerializer(chat_messages, many=True)
    return JsonResponse(serializer.data, safe=False)