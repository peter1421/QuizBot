from django.db import models


class ChapterManager(models.Manager):
    def get_first_assistant_for_chatbot(self, chatbot_id):
        """获取特定 Chatbot 的第一个 assistant_id"""
        chatbot = self.get(id=chatbot_id)
        if chatbot.assistant_ids:
            return chatbot.assistant_ids[0]
        else:
            return None  # 没有任何 assistant_id 时返回 None

    def create_chapter(self, number, title, content):
        chapter = self.create(number=number, title=title, content=content)
        return chapter

    def get_chapter(self, id):
        return self.get(id=id)

    def get_all_chapters(self):
        return self.all()

    def update_chapter(self, id, **kwargs):
        chapter = self.get(id=id)
        for key, value in kwargs.items():
            setattr(chapter, key, value)
        chapter.save()
        return chapter

    def delete_chapter(self, id):
        chapter = self.get(id=id)
        chapter.delete()


class Chapter(models.Model):
    number = models.IntegerField()
    title = models.CharField(max_length=100)
    content = models.TextField()
    assistant_ids = models.JSONField(default=list, verbose_name="助理ID")

    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "章節"
        verbose_name_plural = "章節們"

    objects = ChapterManager()
    def __str__(self):
        return self.title