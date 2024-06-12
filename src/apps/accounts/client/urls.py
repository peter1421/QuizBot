# urls.py

from django.urls import path

from apps.accounts.client.views import login_index, register_index


urlpatterns = [
    path("register_index",register_index , name="client_account_register_index"),
    path("login_index",login_index , name="client_account_login_index"),
]
