# urls.py

from django.contrib.auth import views as auth_views
from django.urls import path

from client.home.views import index

urlpatterns = [
    path("", index, name="client_home_index"),
]
