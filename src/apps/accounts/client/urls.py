# urls.py

from django.urls import path

from apps.accounts.client.views import register_index


urlpatterns = [
    path("index",register_index , name="client_account_register_index"),
]
