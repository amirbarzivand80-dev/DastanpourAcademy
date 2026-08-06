from django.db import models
from users.models import CustomUser


class AdminPermission(models.Model):

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="admin_permission"
    )

    users_access = models.BooleanField(default=False)

    barbers_access = models.BooleanField(default=False)

    services_access = models.BooleanField(default=False)

    reservations_access = models.BooleanField(default=False)

    courses_access = models.BooleanField(default=False)

    shop_access = models.BooleanField(default=False)

    orders_access = models.BooleanField(default=False)

    comments_access = models.BooleanField(default=False)

    messages_access = models.BooleanField(default=False)

    reports_access = models.BooleanField(default=False)

    settings_access = models.BooleanField(default=False)

    def __str__(self):
        return self.user.full_name