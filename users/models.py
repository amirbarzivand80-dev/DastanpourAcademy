
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.utils import timezone


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
            password=password,
        )

        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.phone_verified = True

        user.save(using=self._db)

        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):

    full_name = models.CharField(
        max_length=100
    )

    phone = models.CharField(
        max_length=11,
        unique=True
    )

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

    is_active = models.BooleanField(
        default=True
    )

    is_staff = models.BooleanField(
        default=False
    )

    phone_verified = models.BooleanField(
        default=False
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "phone"

    REQUIRED_FIELDS = ["full_name"]

    @property
    def is_super_admin(self):
        return self.groups.filter(
            name="SuperAdmin"
        ).exists()

    @property
    def is_admin(self):
        return self.groups.filter(
            name="Admin"
        ).exists()

    @property
    def is_barber(self):
        return self.groups.filter(
            name="Barber"
        ).exists()

    def __str__(self):
        return self.full_name


class CustomerGalleryImage(models.Model):

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="gallery_images"
    )

    image = models.ImageField(
        upload_to="customer_gallery/"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.full_name} - {self.id}"


class PhoneVerificationCode(models.Model):

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="verification_codes",
        blank=True,
        null=True
    )

    phone = models.CharField(
        max_length=11
    )

    code = models.CharField(
        max_length=6
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    expires_at = models.DateTimeField()

    is_used = models.BooleanField(
        default=False
    )

    attempts = models.PositiveIntegerField(
        default=0
    )

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"{self.phone} - {self.code}"