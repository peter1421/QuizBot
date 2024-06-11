# urls.py

from apps.home.views import download_db, download_log, index
from django.urls import path

urlpatterns = [
    path("", index, name="index"),
    path("download-db/", download_db, name="download_db"),
    path("download-request-log/", download_log, name="download_request_log"),
]
