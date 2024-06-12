# urls.py

from django.urls import path

from apps.chapter.admin.views import index

urlpatterns = [
    path("index", index, name="admin_chapter_index"),
]
