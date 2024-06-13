# Correct import if User is your model
from apps.account.models import Account
from apps.chatbot.backend import create_threads_id
from django.db import models


class ChatbotManager(models.Manager):
    """聊天機器人的管理器，封裝與資料庫的交互邏輯"""

    def get_or_create_by_account_and_chapter(self, account, chapter):
        chatbot, created = super().get_or_create(
            account=account, chapter=chapter)
        if created:
            chatbot.now_thread = create_threads_id()
            chatbot.save()
        return chatbot

    def find_chapter_by_chatbot_id(self, chatbot_id):
        try:
            return self.chapter  # 返回對應的 Chapter 實例
        except Chatbot.DoesNotExist:
            return None  # 若找不到 Chatbot，返回 None

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

    def find_chatbot_by_id(self, chatbot_id):
        """Find a chatbot instance by its ID and handle errors."""
        try:
            return self.get(id=chatbot_id)
        except Chatbot.DoesNotExist:
            return None  # Return None if the chatbot does not exist

    def validate_owner(self, chatbot_id, user_id):
        """Validate if the chatbot is owned by the given user."""
        chatbot = self.find_chatbot_by_id(chatbot_id)
        if chatbot and chatbot.account_id == user_id:
            return True
        return False  # Return False if not owned by the user or chatbot does not exist


class Chatbot(models.Model):
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, verbose_name="使用者")
    chapter = models.ForeignKey(
        "chapter.Chapter", on_delete=models.CASCADE, verbose_name="章節")
    now_thread = models.CharField(
        max_length=200, verbose_name="目前聊天序列")  # 目前處理的執行緒或過程的標識符

    objects = ChatbotManager()

    class Meta:
        unique_together = ("account", "chapter")
        verbose_name = "聊天機器人"
        verbose_name_plural = "聊天機器人們"

    def __str__(self):
        account = self.account if self.account is not None else "No account"
        chapter = self.chapter if self.chapter is not None else "No chapter"
        now_thread = self.now_thread if self.now_thread is not None else "No thread"
        return f"Chatbot(account={account}, chapter={chapter}, now_thread={now_thread})"


# Create your models here.
# 訊息ID
# 機器人ID
# 角色 sender(user or bot or system)
# 訊息內容
# 標籤
# 訊息時間戳

class ChatMessage(models.Model):
    chatbot = models.ForeignKey(
        Chatbot, on_delete=models.CASCADE, verbose_name="聊天機器人")
    role = models.CharField(
        max_length=10, verbose_name="角色")  # 信息發送者的角色
    content = models.TextField(verbose_name="訊息內容")  # 信息內容
    tag = models.CharField(
        max_length=20, verbose_name="標籤")  # 信息的標籤
    timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name="訊息時間戳")  # 信息的時間戳

    class Meta:
        verbose_name = "聊天訊息"
        verbose_name_plural = "聊天訊息們"

    def __str__(self):
        chatbot = self.chatbot if self.chatbot is not None else "No chatbot"
        role = self.role if self.role is not None else "No role"
        content = self.content if self.content is not None else "No content"
        tag = self.tag if self.tag is not None else "No tag"
        timestamp = self.timestamp if self.timestamp is not None else "No timestamp"
        return f"ChatMessage(chatbot={chatbot}, role={role}, content={content}, tag={tag}, timestamp={timestamp})"
# Create your models here.
# 訊息ID
# 機器人ID
# 角色 sender(user or bot or system)
# 訊息內容
# 標籤
# 訊息時間戳
