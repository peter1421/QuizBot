from django.contrib import messages
from django.shortcuts import redirect


def handle_error(request, error_message, error_url):
    """處理登錄過程中的錯誤。"""
    messages.error(request, error_message)
    return redirect(error_url)


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]  # 取 X-Forwarded-For 头部中的第一个 IP（最左边）
    else:
        ip = request.META.get(
            "REMOTE_ADDR", "",
        )  # 如果没有 X-Forwarded-For 头部，就直接取 REMOTE_ADDR
    return ip
