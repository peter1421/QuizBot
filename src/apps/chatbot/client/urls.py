# urls.py

from django.urls import path

from apps.chatbot.client.views import index

urlpatterns = [
    path("index/<str:chapter_id>/", index, name="client_chatbot_index_with_chapter"),
    path("index", index, name="client_chatbot_index"),
]
