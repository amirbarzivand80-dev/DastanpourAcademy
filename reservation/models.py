from django.db import models
from django.conf import settings

from services.models import Service
from users.models import CustomUser


class Barber(models.Model):

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE
    )

    work_start = models.TimeField(
        default="09:00"
    )

    work_end = models.TimeField(
        default="18:00"
    )

    appointment_duration = models.IntegerField(
        default=30,
        help_text="مدت هر نوبت (دقیقه)"
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.user.full_name


class BarberWorkingDay(models.Model):

    DAYS = [

        (0, "شنبه"),
        (1, "یکشنبه"),
        (2, "دوشنبه"),
        (3, "سه‌شنبه"),
        (4, "چهارشنبه"),
        (5, "پنجشنبه"),
        (6, "جمعه"),

    ]

    barber = models.ForeignKey(
        Barber,
        on_delete=models.CASCADE,
        related_name="working_days"
    )

    day = models.IntegerField(
        choices=DAYS
    )

    is_working = models.BooleanField(
        default=True
    )

    class Meta:
        unique_together = ("barber", "day")

    def __str__(self):
        return f"{self.barber.user.full_name} - {self.get_day_display()}"


class BarberDayOff(models.Model):

    barber = models.ForeignKey(
        Barber,
        on_delete=models.CASCADE,
        related_name="days_off"
    )

    date = models.DateField()

    reason = models.CharField(
        max_length=200,
        blank=True
    )

    def __str__(self):
        return f"{self.barber.user.full_name} - {self.date}"
class Reservation(models.Model):

    STATUS_CHOICES = [
        ("pending", "در انتظار پرداخت"),
        ("approved", "تایید شده"),
        ("done", "انجام شده"),
        ("cancel", "لغو شده"),
    ]

    PAYMENT_STATUS_CHOICES = [
        ("pending", "در انتظار پرداخت"),
        ("paid", "پرداخت شده"),
        ("failed", "ناموفق"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reservations"
    )

    customer_name = models.CharField(
        max_length=100,
        blank=True
    )

    customer_phone = models.CharField(
        max_length=20,
        blank=True
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE
    )

    barber = models.ForeignKey(
        Barber,
        on_delete=models.CASCADE,
        related_name="reservations"
    )

    date = models.DateField()

    time = models.TimeField()

    # -----------------------------
    # مبلغ‌ها
    # -----------------------------

    service_price = models.PositiveBigIntegerField(
        default=0,
        help_text="قیمت خدمت در زمان رزرو"
    )

    deposit_amount = models.PositiveBigIntegerField(
        default=0,
        help_text="مبلغ بیعانه"
    )

    # -----------------------------
    # وضعیت رزرو
    # -----------------------------

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    # -----------------------------
    # وضعیت پرداخت
    # -----------------------------

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default="pending"
    )

    # -----------------------------
    # اطلاعات پرداخت
    # -----------------------------

    payment_reference = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        unique_together = (
            "barber",
            "date",
            "time",
        )

    def __str__(self):

        if self.user:
            name = self.user.full_name
        else:
            name = self.customer_name

        return f"{name} - {self.service.name}"
    
class BarberBlockedTime(models.Model):

    barber = models.ForeignKey(
        Barber,
        on_delete=models.CASCADE,
        related_name="blocked_times"
    )

    date = models.DateField()

    start_time = models.TimeField()

    end_time = models.TimeField()

    reason = models.CharField(
        max_length=200,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.barber.user.full_name} - {self.date}"