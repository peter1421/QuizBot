# urls.py

from django.contrib.auth import views as auth_views
from django.urls import path
from client.account.views import profile_index, register_index


urlpatterns = [
    path("register", register_index, name="client_account_register_index"),
    path('profile', profile_index, name='client_account_profile_index'),
]
