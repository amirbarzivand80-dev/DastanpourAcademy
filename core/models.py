from django.db import models
from users.models import CustomUser


class ContactMessage(models.Model):

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    full_name = models.CharField(max_length=100)

    phone = models.CharField(max_length=11)

    email = models.EmailField(
        blank=True,
        null=True
    )

    message = models.TextField()

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.full_name
    
class ActivityLog(models.Model):

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    action = models.CharField(
        max_length=255
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return self.action
    

class ConsultationRequest(models.Model):
    SUBJECT_CHOICES = [
        ("education", "مشاوره درباره دوره‌های آموزشی"),
        ("registration", "ثبت‌نام در دوره"),
        ("career", "مشاوره ورود به بازار کار"),
        ("other", "سایر موارد"),
    ]

    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=30, choices=SUBJECT_CHOICES)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name
    


class HomeOffer(models.Model):

    title = models.CharField(
        max_length=200,
        default="پیشنهادات امروز"
    )

    description = models.CharField(
        max_length=300,
        blank=True
    )

    discount_percent = models.PositiveIntegerField(
    null=True,
    blank=True
)

    end_time = models.DateTimeField()

    products = models.ManyToManyField(
        "shop.Product",
        blank=True,
        related_name="home_offers"
    )

    courses = models.ManyToManyField(
        "academy.Course",
        blank=True,
        related_name="home_offers"
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title