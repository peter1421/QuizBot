from django.db import models


class ChapterManager(models.Manager):
    def get_first_assistant_id(self, chapter_id):
        chapter = self.get(id=chapter_id)
        if chapter.assistant_ids:
            return chapter.assistant_ids[0]
        return None

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
    assistant_ids = models.JSONField(default=list, blank=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "章節"
        verbose_name_plural = "章節們"

    objects = ChapterManager()
    def __str__(self):
        return self.title