# urls.py

from apps.home.client.views import index
from django.urls import path

urlpatterns = [
    path("", index, name="client_home_index"),
]
