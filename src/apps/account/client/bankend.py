from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.urls import reverse


def login_user(request, username, password, success_url):
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        messages.success(request, "登入成功")
        return redirect(reverse(success_url))
    else:
        messages.error(request, "登入失敗")
        return None
