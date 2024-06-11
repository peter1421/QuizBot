# import pytest
# from django.urls import reverse
# from django.contrib.auth import get_user_model

# # 設定測試數據庫
# @pytest.mark.django_db
# class TestViews:
#     # 測試註冊視圖
#     def test_register_view(self, client):
#     # 設置測試的 POST 數據
#         user_data = {
#             "email": "test@example.com",
#             "phone": "123456789",
#             "password1": "strong_password",
#             "password2": "strong_password",
#             "username": "testuser"
#         }
#         # 發送 POST 請求到註冊視圖        
#         response = client.post(reverse('register'), user_data)

#         # 如果表單無效，打印錯誤信息
#         if response.context and 'form' in response.context:
#             form = response.context['form']
#             if not form.is_valid():
#                 print(form.errors)

#         # 檢查用戶是否已經被創建
#         user_model = get_user_model()     
#         assert user_model.objects.filter(email="test@example.com").exists()
