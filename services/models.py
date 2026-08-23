from django.db import models


class ServiceCategory(models.Model):

    name = models.CharField(
        max_length=100
    )

    def __str__(self):
        return self.name


class Service(models.Model):

    name = models.CharField(
        max_length=100
    )

    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="services"
    )

    barbers = models.ManyToManyField(
        "reservation.Barber",
        blank=True,
        related_name="services"
    )

    description = models.TextField(
        blank=True
    )

    # قیمت پایه خدمت
    price = models.PositiveIntegerField(
        default=0
    )

    order = models.PositiveIntegerField(
        default=0
    )

    image = models.ImageField(
        upload_to="services/",
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


# =========================================================
# قیمت و مدت اختصاصی هر آرایشگر برای هر خدمت
# =========================================================

class BarberServicePrice(models.Model):

    barber = models.ForeignKey(
        "reservation.Barber",
        on_delete=models.CASCADE,
        related_name="service_prices"
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="barber_prices"
    )

    price = models.PositiveIntegerField(
        default=0
    )

    duration = models.PositiveIntegerField(
        default=30,
        help_text="مدت خدمت به دقیقه"
    )

    class Meta:

        unique_together = (
            "barber",
            "service",
        )

    def __str__(self):

        return (
            f"{self.barber} - "
            f"{self.service} - "
            f"{self.price}"
        )


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
    

class ServiceDetail(models.Model):

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="details"
    )

    name = models.CharField(
        max_length=100
    )

    description = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    order = models.PositiveIntegerField(
        default=0
    )

    def __str__(self):
        return f"{self.service.name} - {self.name}"


class BarberServiceDetailPrice(models.Model):

    detail = models.ForeignKey(
        ServiceDetail,
        on_delete=models.CASCADE,
        related_name="barber_prices"
    )

    barber = models.ForeignKey(
        "reservation.Barber",
        on_delete=models.CASCADE,
        related_name="service_detail_prices"
    )

    price = models.PositiveIntegerField(
        default=0
    )

    duration = models.PositiveIntegerField(
        default=10,
        help_text="مدت جزئیات به دقیقه"
    )

    class Meta:
        unique_together = (
            "detail",
            "barber",
        )

    def __str__(self):
        return (
            f"{self.barber} - "
            f"{self.detail} - "
            f"{self.price}"
        )