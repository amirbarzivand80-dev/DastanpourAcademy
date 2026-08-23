from django.db import models
from django.conf import settings
from django.utils import timezone


class DiscountCode(models.Model):

    DISCOUNT_TYPE_CHOICES = [
        ("percent", "درصدی"),
        ("fixed", "مبلغ ثابت"),
    ]

    # =====================================================
    # اطلاعات اصلی کد
    # =====================================================

    code = models.CharField(
        max_length=50,
        unique=True
    )

    discount_type = models.CharField(
        max_length=10,
        choices=DISCOUNT_TYPE_CHOICES,
        default="percent"
    )

    value = models.PositiveIntegerField(
        default=0
    )

    # =====================================================
    # محدوده محصولات
    # =====================================================

    products_all = models.BooleanField(
        default=False
    )

    products = models.ManyToManyField(
        "shop.Product",
        blank=True,
        related_name="discount_codes"
    )

    # =====================================================
    # محدوده دوره‌ها
    # =====================================================

    courses_all = models.BooleanField(
        default=False
    )

    courses = models.ManyToManyField(
        "academy.Course",
        blank=True,
        related_name="discount_codes"
    )

    # =====================================================
    # محدوده خدمات
    # =====================================================

    services_all = models.BooleanField(
        default=False
    )

    services = models.ManyToManyField(
        "services.Service",
        blank=True,
        related_name="discount_codes"
    )

    # =====================================================
    # کاربران خاص
    #
    # خالی = همه کاربران
    # انتخاب کاربر = فقط همان کاربران
    # =====================================================

    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="available_discount_codes"
    )

    # =====================================================
    # فعال / غیرفعال
    # =====================================================

    is_active = models.BooleanField(
        default=True
    )

    # =====================================================
    # تاریخ اعتبار
    # =====================================================

    start_date = models.DateTimeField(
        blank=True,
        null=True
    )

    end_date = models.DateTimeField(
        blank=True,
        null=True
    )

    # =====================================================
    # حداقل مبلغ خرید
    # =====================================================

    minimum_purchase = models.PositiveIntegerField(
        default=0
    )

    # =====================================================
    # محدودیت تعداد استفاده
    # =====================================================

    usage_limit = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    # =====================================================
    # تعداد استفاده فعلی
    # =====================================================

    used_count = models.PositiveIntegerField(
        default=0
    )

    # =====================================================
    # محدودیت استفاده برای هر کاربر
    # =====================================================

    per_user_limit = models.PositiveIntegerField(
        default=1
    )

    # =====================================================
    # تاریخ ایجاد و ویرایش
    # =====================================================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # =====================================================
    # بررسی اعتبار زمانی کد
    # =====================================================

    def is_valid_now(self):

        if not self.is_active:
            return False

        now = timezone.now()

        if self.start_date and now < self.start_date:
            return False

        if self.end_date and now > self.end_date:
            return False

        if (
            self.usage_limit is not None
            and self.used_count >= self.usage_limit
        ):
            return False

        return True

    # =====================================================
    # نمایش
    # =====================================================

    def __str__(self):

        return self.code


class DiscountUsage(models.Model):

    # =====================================================
    # کد تخفیف
    # =====================================================

    discount = models.ForeignKey(
        DiscountCode,
        on_delete=models.CASCADE,
        related_name="usages"
    )

    # =====================================================
    # کاربر
    # =====================================================

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="discount_usages"
    )

    # =====================================================
    # زمان استفاده
    # =====================================================

    used_at = models.DateTimeField(
        auto_now_add=True
    )

    # =====================================================
    # مبلغ تخفیف
    # =====================================================

    discount_amount = models.PositiveIntegerField(
        default=0
    )

    # =====================================================
    # مبلغ قبل از تخفیف
    # =====================================================

    original_amount = models.PositiveIntegerField(
        default=0
    )

    # =====================================================
    # مبلغ نهایی
    # =====================================================

    final_amount = models.PositiveIntegerField(
        default=0
    )

    # =====================================================
    # مرتب‌سازی
    # =====================================================

    class Meta:

        ordering = [
            "-used_at"
        ]

    # =====================================================
    # نمایش
    # =====================================================

    def __str__(self):

        return (
            f"{self.user.full_name} - "
            f"{self.discount.code}"
        )