# views.py


import json
from apps.chapter.models import Chapter
from apps.chatbot.backend import create_threads_id, get_chatbot_response
from apps.chatbot.models import Chatbot, ChatMessage
from apps.chatbot.serializers import ChatMessageSerializer
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from QuizBot.middleware import chatbot_owner_required


def index(request, chapter_id=None):
    user = request.user if request.user.is_authenticated else None

    chapter = get_object_or_404(Chapter, id=chapter_id) if chapter_id else None
    if chapter is not None:
        chatbot, created = Chatbot.objects.get_or_create(
            account=user, chapter=chapter)
        if created:
            now_thread = create_threads_id()
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

# {
#   "csrfmiddlewaretoken": "your_csrf_token_here",
#   "messages": [
#     {"role": "user", "content": "Hello, how are you?"},
#     {"role": "assistant", "content": "I'm good, thank you! How can I assist you today?"}
#   ],
#   "chatbot_id": "your_chatbot_id_here"
# }
# TODO:多重請求
@require_http_methods(["POST"])
def api_chat_with_bot(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        messages = data.get('messages', [])
        chatbot_id = data.get('chatbot_id')
        chatbot = Chatbot.objects.find_chatbot_by_id(chatbot_id)
        chatbot_responses = get_chatbot_response(messages, chatbot)
        #  检查是否响应是单个对象还是列表
        if isinstance(chatbot_responses, list):
            serializer = ChatMessageSerializer(chatbot_responses, many=True)
        else:
            serializer = ChatMessageSerializer(chatbot_responses)
        return JsonResponse({'data': serializer.data})
    return JsonResponse({'error': 'Invalid request'}, status=400)


def api_get_message_by_chatbot_id(request):
    chatbot_id = request.GET.get('chatbot_id')
    chatbot = Chatbot.objects.find_chatbot_by_id(chatbot_id)
    now_thread = chatbot.now_thread
    chat_messages = ChatMessage.objects.find_by_thread_id(now_thread)
    serializer = ChatMessageSerializer(chat_messages, many=True)
    return JsonResponse(serializer.data, safe=False)


def api_update_threads(request):
    chatbot_id = request.POST.get('chatbot_id')  # 使用POST方法获取参数

    if not chatbot_id:
        return JsonResponse({'error': 'Missing chatbot_id parameter'}, status=400)

    try:
        threads_id = create_threads_id()
        updated = Chatbot.objects.update_thread(chatbot_id, threads_id)
        if updated:  # 检查是否真的更新了记录
            return JsonResponse({'success': True, 'data': threads_id})
        else:
            return JsonResponse({'error': 'No chatbot updated'}, status=404)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Chatbot not found'}, status=404)
    except Exception as e:  # 捕获其他可能的错误
        return JsonResponse({'error': str(e)}, status=500)
