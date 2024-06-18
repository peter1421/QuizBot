from django.db import models
from django.utils import timezone

from apps.chatbot.models import Chatbot as BaseChatbot, ChatbotManager as BaseChatbotManager, ChatMessage as BaseChatMessage, ChatMessageManager as BaseChatMessageManager


class PythonChatbotManager(BaseChatbotManager):
    """擴展的聊天機器人管理器，新增額外的管理方法"""


class PythonChatbot(BaseChatbot):
    """擴展的聊天機器人模型，新增額外的欄位"""

    objects = PythonChatbotManager()

    class Meta():
        verbose_name = "Python的聊天機器人"
        verbose_name_plural = "Python的聊天機器人們"


class PythonChatMessageManager(BaseChatMessageManager):
    """擴展的聊天訊息管理器，新增額外的查詢方法"""


class PythonChatMessage(BaseChatMessage):
    """擴展的聊天訊息模型，新增額外的欄位"""

    objects = PythonChatMessageManager()

    class Meta():
        verbose_name = "Python的聊天訊息"
        verbose_name_plural = "Python的聊天訊息們"
