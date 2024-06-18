# urls.py

from django.urls import path

from apps.chatbot.python.client.views import index,api_chat_with_bot, api_get_message_by_chatbot_id


urlpatterns = [
    path("index/<str:chapter_id>/", index, name="client_chatbot_index_with_chapter"),
    path("index", index, name="client_chatbot_index"),
    path("api/chat_with_bot",api_chat_with_bot,name="api_chat_with_bot"),
    path("api/get_message_by_chatbot_id",api_get_message_by_chatbot_id,name="api_get_message_by_chatbot_id"),
]
