from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager
)


class CustomUserManager(BaseUserManager):

    def create_user(self, phone, full_name, password=None):

        if not phone:
            raise ValueError("شماره موبایل الزامی است")

        user = self.model(
            phone=phone,
            full_name=full_name,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, phone, full_name, password):

        user = self.create_user(
            phone=phone,
            full_name=full_name,
            password=password
        )

        user.is_staff = True
        user.is_superuser = True
        user.is_active = True

        user.save(using=self._db)

        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):

    full_name = models.CharField(max_length=100)

    phone = models.CharField(max_length=11, unique=True)

    created_at = models.DateTimeField(
    auto_now_add=True
    )

    profile_image = models.ImageField(
        upload_to="profile_pics/",
        blank=True,
        null=True
    )

    address = models.TextField(
        blank=True,
        null=True
    )

    birth_date = models.DateField(
        blank=True,
        null=True
    )

    marriage_date = models.DateField(
        blank=True,
        null=True
    )

    child_birth = models.DateField(
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "phone"

    REQUIRED_FIELDS = ["full_name"]

    @property
    def is_super_admin(self):
        return self.groups.filter(name="SuperAdmin").exists()

    @property
    def is_admin(self):
        return self.groups.filter(name="Admin").exists()

    @property
    def is_barber(self):
        return self.groups.filter(name="Barber").exists()

    def __str__(self):
        return self.full_name