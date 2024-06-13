import random

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

from QuizBot.middleware import debug_info


class SiteUserManager(BaseUserManager):
    # 創建一般用戶的方法
    def create_user(self, username, password):
        if not username:
            raise ValueError("用戶必須有一個用戶名")

        user = self.model(
            password=password,
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    # 創建超級用戶的方法
    def create_superuser(self,  username, password):
        user = self.create_user(
            password=password,
            username=username,
        )
        user.is_admin = True
        user.set_password(password)
        user.save(using=self._db)
        return user


    def generate_unique_phone(self):
        while True:
            # 生成一個以 '10' 開頭的假電話號碼
            new_phone = "10" + "".join([str(random.randint(0, 9)) for _ in range(8)])
            # 檢查生成的號碼是否已存在於資料庫中
            if not self.model.objects.filter(phone=new_phone).exists():
                return new_phone

    def register_user(self, username, password, is_admin=False):
        try:
            if is_admin:
                user = self.create_superuser(username, password)
            else:
                user = self.create_user(username, password)
            return user
        except Exception as e:
            # Log the error here if needed
            raise ValueError(f"無法創建用戶: {str(e)}")


class SiteUser(AbstractBaseUser):
    email = models.EmailField(verbose_name="電子郵件", max_length=255, null=True)
    username = models.CharField(
        verbose_name="使用者名稱", max_length=254, blank=True, null=True, unique=True
    )
    phone = models.CharField(verbose_name="手機", max_length=255)
    is_active = models.BooleanField(default=True)  # 是否為活躍用戶
    is_admin = models.BooleanField(default=False)  # 是否為管理員

    objects = SiteUserManager()

    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
