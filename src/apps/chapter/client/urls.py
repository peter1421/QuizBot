# urls.py

from django.urls import path

from apps.chapter.client.views import index

urlpatterns = [
    path("index", index, name="client_chapter_index"),
]
