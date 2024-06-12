# Correct import if User is your model
from apps.account.models import SiteUser
from apps.chapter.models import Chapter
from apps.chatbot.backend import get_threads_id
from django.db import models


class ChatbotManager(models.Manager):
    """聊天機器人的管理器，封裝與資料庫的交互邏輯"""

    def get_or_create_by_account_and_chapter(self, account, chapter):
        chatbot, created = super().get_or_create(
            account=account, chapter=chapter)
        if created:
            chatbot.now_thread = get_threads_id(chapter)
            chatbot.save()
        return chatbot

    def create_chatbot(self, user, chapter, now_thread):
        """創建一個新的聊天機器人實例"""
        chatbot = self.create(
            account=user, chapter=chapter, now_thread=now_thread)
        return chatbot

    def fetch_by_user(self, user):
        """根據使用者取得所有相關的聊天機器人"""
        return self.filter(account=user)

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
    account = models.ForeignKey(
        SiteUser, on_delete=models.CASCADE, verbose_name="使用者")
    chapter = models.ForeignKey(
        Chapter, on_delete=models.CASCADE, verbose_name="章節")
    now_thread = models.CharField(
        max_length=200, verbose_name="目前聊天序列")  # 目前處理的執行緒或過程的標識符

    objects = ChatbotManager()

    class Meta:
        unique_together = ("account", "chapter")
        verbose_name = "聊天機器人"
        verbose_name_plural = "聊天機器人們"

    def __str__(self):
        account = self.account if self.account is not None else 'No account'
        chapter = self.chapter if self.chapter is not None else 'No chapter'
        now_thread = self.now_thread if self.now_thread is not None else 'No thread'
        return f"Chatbot(account={account}, chapter={chapter}, now_thread={now_thread})"