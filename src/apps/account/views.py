from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from QuizBot.middleware import admin_required  # Django的内置登录装饰器

from .forms import SiteUserCreationForm  # 确保这里导入的是您的自定义表单类
from .models import SiteUser


@login_required
@admin_required
def register_view(request):
    if request.method == "POST":
        form = SiteUserCreationForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/home/")  # 重定向
        else:
            print(form.errors)  # 打印表单验证错误
    else:
        form = SiteUserCreationForm()
    return render(request, "account/register.html", {"form": form})


# 登录视图
def login_view(request):
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
                user = SiteUser.objects.get(username=username)  # 通过手机号码查找用户
            except SiteUser.DoesNotExist:
                pass

        # 如果找到用户，使用authenticate进行密码验证
        if user:
            user = authenticate(
                request, username=user.username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/home/")  # 重定向
        else:
            # 登录失败的错误处理
            return render(request, "account/login.html", {"error": "無效的登錄憑證"})

    return render(request, "account/login.html")


def logout_view(request):
    # 调用 logout 函数，它会处理登出逻辑
    logout(request)
    # 登出后，重定向用户到登录页面或主页
    return redirect("/account/login")  # 确保 'login' 是您的登录视图的 URL 名称
