# urls.py

from apps.chatbot.python.client.views import api_chat_with_bot, api_get_message_by_chatbot_id, index
from django.urls import path

urlpatterns = [
    path("index/<str:chapter_id>/", index, name="client_chatbot_index_with_chapter"),
    path("index", index, name="client_chatbot_index"),
    path("api/chat_with_bot",api_chat_with_bot,name="api_chat_with_bot"),
    path("api/get_message_by_chatbot_id",api_get_message_by_chatbot_id,name="api_get_message_by_chatbot_id"),
]
