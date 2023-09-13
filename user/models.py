from djongo import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None):
        if not phone_number:
            raise ValueError("Users must have an phone number")

        user = self.model(
            phone_number=phone_number,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None):
        user = self.create_user(
            phone_number=phone_number,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=255, null=True, verbose_name="사용자 이름")
    phone_number = models.CharField(max_length=255, unique=True, verbose_name="핸드폰 번호")
    auth_number = models.CharField(max_length=4, null=True,verbose_name="핸드폰인증 번호")
    nickname = models.CharField(max_length=255, blank=True, verbose_name="닉네임")
    address = models.TextField(verbose_name="주소")
    profile_image = models.ImageField(
        upload_to="profile_image", blank=True, verbose_name="프로필 사진"
    )
    is_admin = models.BooleanField(default=False, verbose_name="관리자 권한")

    objects = UserManager()

    # custom user 모델을 기본 유저 모델로 설정하려면 username field 필수 > unique 한 값
    USERNAME_FIELD = "phone_number"

    def __str__(self):
        return self.phone_number

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
