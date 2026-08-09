from django import forms

from .models import Service
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
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["barbers"].queryset = (
            Barber.objects
            .filter(is_active=True)
            .select_related("user")
        )