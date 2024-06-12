from django.db import models
from apps.accounts.models import SiteUser  # Correct import if User is your model

from apps.chapter.models import Chapter
class ChatbotManager(models.Manager):
    """聊天機器人的管理器，封裝與資料庫的交互邏輯"""

    def create_chatbot(self, user, chapter, now_thread):
        """創建一個新的聊天機器人實例"""
        chatbot = self.create(accounts=user, chapter=chapter, now_thread=now_thread)
        return chatbot

    def fetch_by_user(self, user):
        """根據使用者取得所有相關的聊天機器人"""
        return self.filter(accounts=user)

    def update_thread(self, chatbot_id, new_thread):
        """更新聊天機器人的聊天序列"""
        chatbot = self.get(id=chatbot_id)
        chatbot.now_thread = new_thread
        chatbot.save()
        return chatbot

    def delete_chatbot(self, chatbot_id):
        """刪除一個聊天機器人"""
        chatbot = self.get(id=chatbot_id)
        chatbot.delete()
class Chatbot(models.Model):
    accounts  = models.ForeignKey(SiteUser, on_delete=models.CASCADE, verbose_name="使用者")
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, verbose_name="章節")
    now_thread = models.CharField(max_length=200, verbose_name="目前聊天序列")  # 目前處理的執行緒或過程的標識符
    
    objects = ChatbotManager()
    
    class Meta:
        verbose_name = "聊天機器人"
        verbose_name_plural = "聊天機器人們"