# views.py


from apps.account.client.bankend import login_user
from apps.account.forms import AccountCreationForm, AccountForm
from apps.account.models import Account
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

def userlist_ui(request):
    content = {}
    return render(
        request,
        "client/account/ui_userlist.html",
        context=content,
    )
def register_index(request):
    form = AccountCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        password = request.POST.get("password1")
        username = form.cleaned_data.get("username")
        is_admin = form.cleaned_data.get("is_admin", False)
        try:
            Account.objects.register_user(username, password, is_admin)
            messages.success(request, "註冊成功")
            return login_user(request, username, password, "client_home_index")
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
        # 登录页面初始请求
    if request.method == "GET":
        # 尝试从请求的 URL 中获取 'next' 参数
        next_page = request.GET.get('next', '/home/')
        request.session['next_page'] = next_page  # 将 'next' 参数存储在 session 中以便重用

    if request.method == "POST":
        username = request.POST.get("username")  # 用户可以输入username
        password = request.POST.get("password")
        user = None

        # 检查输入是否为电子邮件格式
        if "@" in username:
            try:
                user = Account.objects.get(email=username)  # 通过电子邮件查找用户
            except Account.DoesNotExist:
                pass
        else:
            try:
                user = Account.objects.get(
                    username=username)  # 通过username码查找用户
            except Account.DoesNotExist:
                pass

        # 如果找到用户，使用authenticate进行密码验证
        if user:
            user = authenticate(
                request, username=user.username, password=password)

        if user is not None:
            login(request, user)
            # 从 session 中获取 'next' 参数并重定向
            next_page = request.session.get('next_page', '/home/')
            return redirect(next_page)

    return render(request, "client/account/login/index.html")


def logout_index(request):
    logout(request)
    # 登出后，重定向用户到登录页面或主页
    return redirect(reverse("client_home_index"))


@login_required
def profile_index(request):
    user = get_object_or_404(Account, pk=request.user.pk)  # 確保用戶已登入
    if request.method == "POST":
        form = AccountForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("client_account_profile_index")  # 重定向到更新成功的頁面
    else:
        form = AccountForm(instance=user)
    context = {"form": form}
    return render(request, "client/account/profile/index.html", context)
