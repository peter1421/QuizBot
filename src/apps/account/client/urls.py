# urls.py

from apps.account.client.views import login_index, logout_index, register_index
from django.urls import path

urlpatterns = [
    path("register_index", register_index,
         name="client_account_register_index"),
    path("login_index", login_index, name="client_account_login_index"),
    path("logout", logout_index, name="client_account_logout")
]
