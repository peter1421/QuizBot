from django.db import models


class ChapterManager(models.Manager):
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

    # 新增方法來獲取指定章節的第一個助理ID
    def get_first_assistant_id_of_chapter(self, chapter_id):
        chapter = self.get_chapter(chapter_id)
        if chapter.assistant_ids:
            return chapter.assistant_ids[0]
        return None  # 章節沒有任何助理ID時返回None

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
    
    def get_first_assistant_id(self):
        if self.assistant_ids:
            return self.assistant_ids[0]
        return None  # 或者返回一個明確的值或錯誤信息，如果列表是空的
