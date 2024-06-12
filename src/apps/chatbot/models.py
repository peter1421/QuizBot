# from django.db import models
# class StudentBookBot(models.Model):
#     """
#     學生書籍機器人模型
#     """
#     bot_id = models.BigAutoField(primary_key=True, verbose_name='機器人ID')
#     student = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='學生')
#     book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='書籍')
#     now_chatroom_id= models.CharField(max_length=100,blank=True, verbose_name='當前聊天房間')
#     class Meta:
#         unique_together = ('student', 'book', 'now_chatroom_id')
#         verbose_name = '學生書籍機器人'


#     def __str__(self):
#         return f'{self.student.username} - {self.book.name}'

# class ChatMessage(models.Model):
#     bot_id = models.ForeignKey(StudentBookBot, on_delete=models.CASCADE, related_name='chat_messages', verbose_name='學生書籍機器人')
#     # 聊天室ID - 同一個聊天室的訊息，聊天室ID都一樣
#     chatroom_id = models.CharField(max_length=100)

#     # 角色sender - 表明訊息是由用戶還是機器人發送
#     SENDER_CHOICES = [
#         ('user', 'User'),
#         ('bot', 'Bot'),
#     ]
#     sender = models.CharField(max_length=4, choices=SENDER_CHOICES)

#     # message - 訊息內容
#     message = models.TextField()

#     # 標籤 - 訊息的標籤，可選
#     tag = models.CharField(max_length=50, blank=True)

#     # 訊息編號 - 自定義格式的唯一識別符

#     # 訊息時間戳 - 記錄訊息的發送時間
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def save(self, *args, **kwargs):
#         super(ChatMessage, self).save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.bot_id}-{self.chatroom_id}-{self.message_id}"

#     class Meta:
#         # 設置對象的可讀名稱
#         verbose_name = '聊天訊息'
#         verbose_name_plural = '聊天訊息'