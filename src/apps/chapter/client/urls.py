# urls.py

from django.urls import path

from apps.chapter.client.views import index, index_ui

urlpatterns = [
    path("index", index, name="client_chapter_index"),
    path("index_ui", index_ui, name="client_chapter_index_ui"),
]
