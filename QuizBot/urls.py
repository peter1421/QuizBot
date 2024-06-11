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

from django.shortcuts import redirect
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# from apps.member.views.crud import TmlMemberViewSet

# router = DefaultRouter()
# router.register(r'member', TmlMemberViewSet)
# router.register(r'musics', views.MusicViewSet)


# 定義一個簡單的視圖函數用於重定向
def redirect_to_musics(request):
    return redirect("/home/")  # 重定向


schema_view = get_schema_view(
    openapi.Info(
        title="Episyche Technologies",
        default_version="v1"),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("", redirect_to_musics),  # 當訪問根 URL 時，執行重定向
    path("docs/", schema_view.with_ui("swagger",
         cache_timeout=0), name="schema-swagger-ui"),
    # path("admin/", admin.site.urls),
    # path('callback', views.callback),
    path("home/", include("apps.home.urls")),
    path("accounts/", include("apps.accounts.urls")),
    path("management_sample/", include("apps.management_sample.urls")),

    # client
    path("client/home/", include("client.home.urls")),
    path("client/account/", include("client.account.urls")),

]
