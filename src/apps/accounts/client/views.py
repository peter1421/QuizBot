# views.py

import urllib

from apps.accounts.client.bankend import login_user
from apps.accounts.forms import SiteUserCreationForm, SiteUserForm
from apps.accounts.models import SiteUser
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render

from QuizBot.service import LineService
from QuizBot.utils import handle_error


def register_index(request):
    form = SiteUserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        phone = request.POST.get("phone")
        password = request.POST.get("password1")
        username = form.cleaned_data.get("username")
        is_admin = form.cleaned_data.get("is_admin", False)
        try:
            SiteUser.objects.register_user(phone, username, password, is_admin)
            messages.success(request, "註冊成功")
            return login_user(request, phone, password, "client_home_index")
        except ValueError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f"發生意外錯誤: {str(e)}")
    else:
        messages.error(request, f"註冊失敗: {form.errors}")

    context = {"form": form}
    return render(request, "client/account/register/index.html", context)

# 登录视图
def login_index(request):
    if request.method == "POST":
        username = request.POST.get("username")  # 用户可以输入电子邮件或手机号码
        password = request.POST.get("password")
        user = None

        # 检查输入是否为电子邮件格式
        if "@" in username:
            try:
                user = SiteUser.objects.get(email=username)  # 通过电子邮件查找用户
            except SiteUser.DoesNotExist:
                pass
        else:
            try:
                user = SiteUser.objects.get(phone=username)  # 通过手机号码查找用户
            except SiteUser.DoesNotExist:
                pass

        # 如果找到用户，使用authenticate进行密码验证
        if user:
            user = authenticate(request, username=user.phone, password=password)

        if user is not None:
            login(request, user)
            return redirect("/home/")  # 重定向

    return render(request, "client/account/login/index.html")

def line_login(request):
    client_id = settings.LINE_LOGIN_CHANNEL_ID
    redirect_uri = urllib.parse.quote(settings.LINE_LOGIN_CALLBACK_URL, safe="")
    scope = urllib.parse.quote("profile openid email", safe="")
    auth_url, state = LineService.build_auth_url(client_id, redirect_uri, scope)
    return HttpResponseRedirect(auth_url)


def line_callback(request):
    """LINE 登錄的回調處理函數。"""
    code = request.GET.get("code")
    token_data = LineService.exchange_token(
        code,
        settings.LINE_LOGIN_CALLBACK_URL,
        settings.LINE_LOGIN_CHANNEL_ID,
        settings.LINE_LOGIN_CHANNEL_SECRET,
    )

    if token_data:
        return process_line_login(request, token_data)

    messages.error(request, "無法獲得 access token")
    return HttpResponseRedirect("/error")  # 導向錯誤頁面


def process_line_login(request, token_data):
    """處理從 LINE 獲取的 token 和用戶數據。"""
    user_data = LineService.verify_id_token(
        token_data.get("id_token"), settings.LINE_LOGIN_CHANNEL_ID,
    )
    error_url = "/error"
    if not user_data:
        return handle_error(request, "ID token 驗證失敗", error_url)

    user_profile = get_user_profile_from_line(token_data["access_token"])
    if not user_profile:
        return handle_error(request, "無法獲取用戶資料", error_url)

    return create_and_login_user(request, user_profile, user_data)


def get_user_profile_from_line(access_token):
    """從 LINE 獲取用戶資料的函數。"""
    return LineService.get_profile(access_token)


def create_and_login_user(request, user_profile, user_data):
    """創建和登錄用戶的函數。"""
    user = SiteUser.objects.create_user_from_line(
        line_id=user_profile["userId"],
        email=user_data.get("email"),
        username=user_data.get("name"),
    )
    login(request, user)
    messages.success(request, "登入成功")
    return redirect("client_account_profile_index")


@login_required
def profile_index(request):
    user = get_object_or_404(SiteUser, pk=request.user.pk)  # 確保用戶已登入
    if request.method == "POST":
        form = SiteUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("client_account_profile_index")  # 重定向到更新成功的頁面
    else:
        form = SiteUserForm(instance=user)
    context = {"form": form}
    return render(request, "client/account/profile/index.html", context)
