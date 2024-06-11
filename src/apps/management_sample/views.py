from django.contrib.auth import login
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse  # 1
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import reverse

# from myTool.funTool import log_activity

# from management_sample.models import MemberSample


# Create your views here.
def index(request):
    template = loader.get_template("management_sample/index.html")
    return HttpResponse(template.render({}, request))


def generate_view(request, filename):
    template_name = (
        f"management_sample/{filename}"
        if ".html" in filename
        else f"management_sample/{filename}.html"
    )
    return render(request, template_name)


# @log_activity
# def register_users(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         email = request.POST.get("email")
#         password = request.POST.get("password")
#         # 創建用戶
#         MemberSample.objects.create_user(
#             email=email,
#             password=password,
#             name=name,
#         )
#         return redirect(reverse("show_users"))


# def get_user(request, user_id):
#     MemberSample.objects.get(pk=user_id)
#     # 使用取得到的使用者物件進行其他操作


# @log_activity
# def show_users(request):
#     users = MemberSample.objects.all()
#     return render(request, "management_sample/show-users.html", {"users": users})


# @log_activity
# def login_users(request):
#     if request.method == "POST":
#         email = request.POST.get("email")
#         password = request.POST.get("password")
#         try:
#             # 從 MemberSample 資料庫中獲取用戶
#             user = MemberSample.objects.get(email=email)
#             # 檢查密碼是否正確
#             if check_password(password, user.password):
#                 # 如果密碼正確，進行登入
#                 login(request, user)
#                 # 設置 Cookie
#                 response = redirect("/management_sample")
#                 response.set_cookie("userAuthenticated", True)
#                 response.set_cookie("user_email", email)
#                 return response
#             else:
#                 # 密碼錯誤
#                 return HttpResponse("登入失敗，請確認輸入的資訊正確")
#         except MemberSample.DoesNotExist:
#             # 用戶不存在
#             return HttpResponse("該用戶不存在")


# @log_activity
# def logout_user(request):
#     # 清除相關的Cookie
#     response = redirect("/management_sample")
#     response.delete_cookie("userAuthenticated")
#     response.delete_cookie("user_email")

#     return response
