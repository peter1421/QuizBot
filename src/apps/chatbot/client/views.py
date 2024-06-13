# views.py


from apps.chapter.models import Chapter
from apps.chatbot.models import Chatbot
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt


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


@csrf_exempt  # 允许跨站请求，为了简化示例
def api_chat_with_bot(request):
    if request.method == 'POST':
        user_message = request.POST.get('message')
        # 在这里添加您的处理逻辑来生成响应
        response_message = "这里是机器人的回复。"  # 示例响应
        return JsonResponse({'message': response_message})
    return JsonResponse({'error': 'Invalid request'}, status=400)
