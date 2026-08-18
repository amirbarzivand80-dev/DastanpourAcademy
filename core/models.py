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