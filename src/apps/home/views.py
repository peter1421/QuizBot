import os

from django.conf import settings
from django.contrib.auth.decorators import login_required  # Django的内置登录装饰器
from django.http import Http404, HttpResponse
from django.shortcuts import render

from QuizBot.middleware import admin_required


def index(request):
    return render(
        request,
        "home/index.html",
    )


@login_required
@admin_required
def download_db(request):
    # 指定文件的路徑
    filepath = os.path.join(settings.BASE_DIR, "database.sqlite3")
    if os.path.exists(filepath):
        with open(filepath, "rb") as fh:
            response = HttpResponse(fh.read(), content_type="application/x-sqlite3")
            response["Content-Disposition"] = "inline; filename=" + os.path.basename(
                filepath,
            )
            return response
    raise Http404


@login_required
@admin_required
def download_log(request):
    # 檢查logs目錄是否存在
    logs_directory = os.path.join(os.getcwd(), "logs")
    if not os.path.exists(logs_directory):
        return HttpResponse("Logs directory doesn't exist.")

    # 檢查request.log文件是否存在
    log_file_path = os.path.join(logs_directory, "request.log")
    if not os.path.exists(log_file_path):
        return HttpResponse("Request log file doesn't exist.")

    # 讀取log文件內容
    with open(log_file_path, "rb") as log_file:
        response = HttpResponse(log_file.read(), content_type="text/plain")
        response["Content-Disposition"] = 'attachment; filename="request.log"'
        return response
