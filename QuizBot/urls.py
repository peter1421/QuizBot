"""
URL configuration for QuizBot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/

Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path

# from apps.member.views.crud import TmlMemberViewSet

# router = DefaultRouter()
# router.register(r'member', TmlMemberViewSet)
# router.register(r'musics', views.MusicViewSet)


# 定義一個簡單的視圖函數用於重定向
def redirect_to_musics(request):
    return redirect("/home/")  # 重定向


urlpatterns = [
    path("", redirect_to_musics),  # 當訪問根 URL 時，執行重定向
    path("admin/", admin.site.urls, name="admin"),
    # path('callback', views.callback),
    path("home/", include("apps.home.urls")),
    path("account/", include("apps.account.urls")),
    path("management_sample/", include("apps.management_sample.urls")),
    # client
    path("client/home/", include("apps.home.client.urls")),
    path("client/account/", include("apps.account.client.urls")),
    path("client/chatbot/", include("apps.chatbot.client.urls")),

    path("client/chapter/", include("apps.chapter.client.urls")),
    # path("admin/chapter/", include("apps.chapter.admin.urls")),

]
