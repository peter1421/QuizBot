import json
import logging
from datetime import datetime
from functools import wraps

import pytz
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils.encoding import force_str

from QuizBot.utils import get_client_ip
from apps.chatbot.models import Chatbot


def convert_to_unicode(obj):
    if isinstance(obj, str):
        return force_str(obj)
    elif isinstance(obj, list):
        return [convert_to_unicode(item) for item in obj]
    elif isinstance(obj, dict):
        return {
            convert_to_unicode(key): convert_to_unicode(value)
            for key, value in obj.items()
        }
    else:
        return obj


class LogRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger("request_logger")

    def __call__(self, request):
        user_ip = get_client_ip(request)
        timezone = pytz.timezone(settings.TIME_ZONE)
        current_time = datetime.now(timezone).strftime("%Y-%m-%d %H:%M:%S")
        response = self.get_response(request)
        log_message = f"[{current_time}]{user_ip} {request.method} {request.path} {response.status_code} {request.META.get('HTTP_USER_AGENT')}"
        self.logger.info(log_message)
        request_data = {}
        try:
            if request.method == "POST":
                request_data = dict(request.POST)
                request_data_unicode = convert_to_unicode(request_data)
                self.logger.info("Request Data:")
                self.logger.info(
                    json.dumps(request_data_unicode, indent=2, ensure_ascii=False),
                )
            elif request.method == "PUT":
                request_body = request.body.decode("utf-8")
                request_data = json.loads(request_body)
                request_data_unicode = convert_to_unicode(request_data)
                self.logger.info("Request Data:")
                self.logger.info(
                    json.dumps(request_data_unicode, indent=2, ensure_ascii=False),
                )
        except Exception as e:
            self.logger.error(f"Error decoding request body: {e}")
        return response


def handle_exceptions(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except (KeyError, ValueError):
            return JsonResponse(
                {"status": "error", "message": "Invalid request"}, status=400,
            )
        except ObjectDoesNotExist:
            return JsonResponse(
                {"status": "error", "message": "Entry not found"}, status=404,
            )

    return wrapper


def debug_info(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        arg_names = func.__code__.co_varnames[: func.__code__.co_argcount]
        args_dict = dict(zip(arg_names, args))
        args_dict.update(kwargs)
        args_str = ", ".join(f"\n{k}: {v!r}" for k, v in args_dict.items())

        try:
            result = func(*args, **kwargs)
            # 使用 repr() 確保即使 result 是 None 也能安全轉換為字符串
            result_repr = repr(result)
        except Exception as e:
            result_repr = f"Error occurred: {e}"

        print(f"Function name: {func.__name__}")
        print(f"Arguments: {args_str}")
        print(f"Return value: {result_repr}")
        return result

    return wrapper


def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_admin:
            return view_func(request, *args, **kwargs)
        else:
            message = f"您沒有權限執行此操作，請聯絡管理員"
            messages.error(request, message)
            # 'home' 是你的首頁的URL名稱
            return HttpResponseRedirect(reverse("client_home_index"))

    return _wrapped_view

def chatbot_owner_required(view_func):
    """
    裝飾器檢查當前用戶是否為聊天機器人的擁有者。
    假設 'chatbot_id' 作為關鍵字參數傳遞給視圖。
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        chatbot_id = kwargs.get('chatbot_id')
        if chatbot_id is None:
            # 處理未提供 chatbot_id 的情況
            message = "缺少必要的chatbot_id參數。"
            messages.error(request, message)
            return HttpResponseRedirect(reverse("client_home_index"))

        user = request.user
        if user.is_authenticated:
            if Chatbot.objects.validate_owner(chatbot_id, user.id):
                return view_func(request, *args, **kwargs)
            else:
                message = "您沒有權限訪問此聊天機器人，請聯絡管理員。"
        else:
            message = "請先登入才能進行操作。"

        messages.error(request, message)
        return HttpResponseRedirect(reverse("client_home_index"))

    return _wrapped_view

warningLogger = logging.getLogger("request_logger")
