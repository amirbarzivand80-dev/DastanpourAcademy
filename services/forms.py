from django import forms
from .models import (
    Service,
    BarberServicePrice,
    ServiceDetail,
    BarberServiceDetailPrice,
)
from reservation.models import Barber


class ServiceForm(forms.ModelForm):

    class Meta:
        model = Service

        fields = [
            "name",
            "category",
            "barbers",
            "description",
            "price",
            "order",
            "image",
            "is_active",
        ]

        widgets = {
            "description": forms.Textarea(
                attrs={
                    "rows": 4
                }
            ),

            "barbers": forms.CheckboxSelectMultiple(),

            "price": forms.NumberInput(
                attrs={
                    "placeholder": "قیمت پایه"
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["barbers"].queryset = (
            Barber.objects
            .filter(is_active=True)
            .select_related("user")
        )

        # قیمت اختصاصی قبلی هر آرایشگر
        self.barber_prices = {}

        if self.instance and self.instance.pk:

            prices = BarberServicePrice.objects.filter(
                service=self.instance
            )

            self.barber_prices = {
                item.barber_id: item.price
                for item in prices
            }

class ServiceDetailForm(forms.ModelForm):

    class Meta:
        model = ServiceDetail

        fields = [
            "name",
            "description",
            "order",
            "is_active",
        ]

        widgets = {

            "description": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "توضیحات جزئیات"
                }
            ),

            "order": forms.NumberInput(
                attrs={
                    "min": 0
                }
            ),
        }