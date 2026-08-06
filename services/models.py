from django.db import models

class ServiceCategory(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Service(models.Model):

    name = models.CharField(max_length=100)

    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="services"
    )

    description = models.TextField(blank=True)

    price = models.PositiveIntegerField(default=0)

    order = models.PositiveIntegerField(default=0)

    image = models.ImageField(
        upload_to="services/",
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
class ServiceImage(models.Model):

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        upload_to="services/gallery/"
    )

    def __str__(self):
        return self.service.name