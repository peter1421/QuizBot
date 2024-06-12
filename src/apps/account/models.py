import random

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

from QuizBot.middleware import debug_info


class SiteUserManager(BaseUserManager):
    # 創建一般用戶的方法
    def create_user(self, phone, username, password):
        if not phone:
            raise ValueError("用戶必須有一個電話號碼")
        if not username:
            raise ValueError("用戶必須有一個用戶名")

        user = self.model(
            password=password,
            phone=phone,
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        print(user.password)
        return user

    # 創建超級用戶的方法
    def create_superuser(self, phone, username, password):
        user = self.create_user(
            password=password,
            phone=phone,
            username=username,
        )
        user.is_admin = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    @debug_info
    def create_user_from_line(self, line_id, phone=None, email=None, username=None):
        if not line_id:
            raise ValueError("LINE ID 是必需的")
        # 嘗試獲取現有用戶或創建新用戶
        user, created = self.model.objects.get_or_create(line_id=line_id)
        if created:
            # 如果是創建新用戶，則生成唯一的手機號碼
            if not phone:
                phone = self.generate_unique_phone()
            user.phone = phone
            user.email = email
            user.username = username
            user.set_unusable_password()  # 設置一個不可用的密碼
            user.save(using=self._db)

        return user

    def generate_unique_phone(self):
        while True:
            # 生成一個以 '10' 開頭的假電話號碼
            new_phone = "10" + "".join([str(random.randint(0, 9)) for _ in range(8)])
            # 檢查生成的號碼是否已存在於資料庫中
            if not self.model.objects.filter(phone=new_phone).exists():
                return new_phone

    def register_user(self, phone, username, password, is_admin=False):
        try:
            if is_admin:
                user = self.create_superuser(phone, username, password)
            else:
                user = self.create_user(phone, username, password)
            return user
        except Exception as e:
            # Log the error here if needed
            raise ValueError(f"無法創建用戶: {str(e)}")


class SiteUser(AbstractBaseUser):
    phone = models.CharField(verbose_name="手機號碼", max_length=255, unique=True)
    email = models.EmailField(verbose_name="電子郵件", max_length=255, null=True)
    username = models.CharField(
        verbose_name="使用者名稱", max_length=254, blank=True, null=True,
    )
    is_active = models.BooleanField(default=True)  # 是否為活躍用戶
    is_admin = models.BooleanField(default=False)  # 是否為管理員
    tml_house_id = models.IntegerField(
        verbose_name="家庭編號", null=True, blank=True, default=0,
    )
    tml_person_id = models.IntegerField(
        verbose_name="個人編號", null=True, blank=True, default=0,
    )
    line_id = models.CharField(
        verbose_name="Line ID", max_length=254, unique=True, blank=True, null=True,
    )

    objects = SiteUserManager()

    USERNAME_FIELD = "phone"

    def __str__(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
