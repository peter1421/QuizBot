# urls.py

from django.urls import path

from apps.chatbot.client.views import index

urlpatterns = [
    path("index", index, name="client_chatbot_index"),
]
