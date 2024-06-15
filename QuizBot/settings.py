"""
Django settings for QuizBot project.

Generated by 'django-admin startproject' using Django 4.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
import sys
from pathlib import Path

from .config import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(BASE_DIR, "src"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = "django-insecure-gkcj*#5-$1uu@mqqtb+gi0fu0^jd5$%p1(17wmb6-krw1=m+v&"

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = False
DEBUG = True

ALLOWED_HOSTS = ["*"]
# CSRF_TRUSTED_ORIGINS = ['*']


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "apps.management_sample",
    "apps.home.apps.HomeConfig",
    # "apps.home.client.apps.ClientHomeConfig",
    "apps.account.apps.AccountConfig",
    "apps.account.client.apps.ClientAccountConfig",

    "apps.chapter.apps.ChapterConfig",
    # "apps.chapter.admin.apps.AdminChapterConfig",
    "apps.chapter.client.apps.ClientChapterConfig",

    "apps.chatbot.apps.ChatbotConfig",
    "apps.chatbot.client.apps.ClientChatbotConfig",

    "apps.dashboard.python_dashboard.client.apps.ClientPythonDashboardConfig",
    "apps.dashboard.python_dashboard.apps.PythonDashboardConfig",

    
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "QuizBot.middleware.LogRequestMiddleware",  # 替换为您的中间件路径
]
MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

ROOT_URLCONF = "QuizBot.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "src/templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "QuizBot.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "database.sqlite3"),
    },
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    # },
    # 允許與用戶屬性相似
    # {
    #     "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    # },
    # 允許最小數字
    # {
    #     "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    # },
    # 允許常用密碼
    # {
    #     "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    # },
    # 允許純數字
]
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "zh-hant"

TIME_ZONE = "Asia/Taipei"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# 静态文件配置
STATIC_URL = "/static/"
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'src\static')]
STATICFILES_DIRS = [os.path.join(BASE_DIR, "src", "static")]

STATIC_ROOT = BASE_DIR / "productionfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "account.Account"
LOGIN_URL = "/account/login/"

# CSRF_TRUSTED_ORIGINS = ["https://*", "http://*"]
CSRF_TRUSTED_ORIGINS = ["https://*.azurewebsites.net"]

X_FRAME_OPTIONS = "ALLOW-FROM uri"


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",  # 使用StreamHandler输出到终端
        },
        "django": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/django.log"),
            "encoding": "utf-8",
        },
        "request": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/request.log"),
            "encoding": "utf-8",
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["console"],  # 使用上面配置的console处理程序
            "level": "DEBUG",
            "propagate": True,
        },
        "django": {
            "handlers": ["django"],
            "level": "DEBUG",
            "propagate": True,
        },
        "request_logger": {  # 自定义日志记录器，以匹配 middleware.py 中的 logger 名称
            "handlers": ["request"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}

# 確保logs目錄存在，並自動創建它
LOGS_DIR = os.path.join(BASE_DIR, "logs")
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

# 確保日誌檔案存在，並自動創建它們
for log_file in ["django.log", "request.log"]:
    log_file_path = os.path.join(LOGS_DIR, log_file)
    if not os.path.exists(log_file_path):
        with open(log_file_path, "w"):
            pass

# 本地端ASSISTANT_ID
CHATBOT_CONFIGS = {
    1: {
        "name": "Python機器人",
        "assistant_id": "asst_UELrrm9ZEgiY2LjnROnWP3NJ",
    },
}
API_KEY = API_KEY
