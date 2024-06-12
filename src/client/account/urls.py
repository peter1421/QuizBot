# urls.py

from client.account.views import login_index, profile_index, register_index
from django.urls import path

urlpatterns = [
    path("register", register_index, name="client_account_register_index"),
    path("login", login_index, name="client_account_login_index"),
    path("profile", profile_index, name="client_account_profile_index"),
]
