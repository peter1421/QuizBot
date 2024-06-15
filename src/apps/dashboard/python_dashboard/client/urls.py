# urls.py

from apps.dashboard.python_dashboard.client.views import index
from django.urls import path

urlpatterns = [
    path("index", index, name="client_dashboard_python_dashboard_index"),
    # path("index_ui", index_ui, name="client_chapter_index_ui"),
]
