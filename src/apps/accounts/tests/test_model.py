import pytest
from django.contrib.auth import get_user_model


# 設置測試數據
@pytest.fixture
def user_info():
    return {
        "phone": "1098765432",
        "username": "testuser",
        "password": "securepassword123",
    }


@pytest.fixture
def super_user_info():
    return {
        "phone": "1012345678",
        "username": "superuser",
        "password": "supersecurepassword123",
    }


@pytest.fixture
def line_user_info():
    return {
        "line_id": "line123456",
        "phone": "1023456789",
        "email": "lineuser@example.com",
        "username": "lineuser",
    }


@pytest.mark.django_db
def test_create_user(user_info):
    """
    測試創建一般用戶
    """
    User = get_user_model()
    user = User.objects.register_user(**user_info, is_admin=False)
    assert user.phone == user_info["phone"]
    assert user.username == user_info["username"]
    assert user.check_password(user_info["password"])
    assert not user.is_admin
    assert user.is_active


@pytest.mark.django_db
def test_create_superuser(super_user_info):
    """
    測試創建超級用戶
    """
    User = get_user_model()
    superuser = User.objects.register_user(**super_user_info, is_admin=True)
    assert superuser.phone == super_user_info["phone"]
    assert superuser.username == super_user_info["username"]
    assert superuser.check_password(super_user_info["password"])
    assert superuser.is_admin
    assert superuser.is_active


@pytest.mark.django_db
def test_create_user_from_line(line_user_info):
    """
    測試根據 LINE ID 創建用戶
    """
    User = get_user_model()
    user = User.objects.create_user_from_line(**line_user_info)
    assert user.line_id == line_user_info["line_id"]
    assert user.phone == line_user_info["phone"]
    assert user.email == line_user_info["email"]
    assert user.username == line_user_info["username"]
    assert user.is_active


@pytest.mark.django_db
def test_generate_unique_phone():
    """
    測試生成獨特的電話號碼
    """
    User = get_user_model()
    phone = User.objects.generate_unique_phone()
    # 確保電話號碼以 '10' 開頭且長度為10位數
    assert phone.startswith("10")
    assert len(phone) == 10
    # 確保電話號碼是唯一的
    assert not User.objects.filter(phone=phone).exists()


@pytest.mark.django_db
def test_create_user_with_invalid_phone():
    """
    測試使用無效電話號碼創建用戶應拋出 ValueError
    """
    User = get_user_model()
    with pytest.raises(ValueError):
        User.objects.create_user(phone="", username="testuser", password="password123")


@pytest.mark.django_db
def test_create_superuser_with_invalid_username():
    """
    測試使用無效用戶名創建超級用戶應拋出 ValueError
    """
    User = get_user_model()
    with pytest.raises(ValueError):
        User.objects.create_superuser(
            phone="1234567890", username="", password="password123",
        )


@pytest.mark.django_db
def test_password_encryption():
    """
    測試密碼是否被加密儲存
    """
    User = get_user_model()
    user = User.objects.create_user(
        phone="1234567890", username="testuser", password="password123",
    )
    assert user.password != "password123"  # 密碼不應該以明文儲存


@pytest.mark.django_db
def test_user_deactivation():
    """
    測試用戶的活躍狀態可以被更新為非活躍
    """
    User = get_user_model()
    user = User.objects.create_user(
        phone="1234567890", username="testuser", password="password123",
    )
    user.is_active = False
    user.save()
    updated_user = User.objects.get(phone="1234567890")
    assert not updated_user.is_active
