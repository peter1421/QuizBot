from django.contrib import admin

from apps.chatbot.models import Chatbot
from apps.chatbot.python.models import PythonChatMessage, PythonChatbot


admin.site.register(PythonChatbot)
admin.site.register(PythonChatMessage)
