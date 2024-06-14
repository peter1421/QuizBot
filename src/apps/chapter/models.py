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


class Chapter(models.Model):
    number = models.IntegerField()
    title = models.CharField(max_length=100)
    content = models.TextField()
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "章節"
        verbose_name_plural = "章節們"

    objects = ChapterManager()
    def __str__(self):
        return self.title