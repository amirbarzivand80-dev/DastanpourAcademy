from django import forms
from .models import BarberBlockedTime
from django import forms
from .models import Reservation, Barber
from services.models import Service

class BarberBlockedTimeForm(forms.ModelForm):

    class Meta:
        model = BarberBlockedTime

        fields = [
            "date",
            "start_time",
            "end_time",
            "reason",
        ]

        widgets = {

            "date": forms.DateInput(attrs={"type": "date"}),

            "start_time": forms.TimeInput(attrs={"type": "time"}),

            "end_time": forms.TimeInput(attrs={"type": "time"}),

            "reason": forms.TextInput(),

        }

class WalkInReservationForm(forms.Form):

    customer_name = forms.CharField(
        label="نام مشتری",
        max_length=100
    )

    customer_phone = forms.CharField(
        label="شماره موبایل",
        max_length=20,
        required=False
    )

    service = forms.ModelChoiceField(
        queryset=Service.objects.filter(is_active=True),
        label="خدمت"
    )

    date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"})
    )

    time = forms.TimeField(
        widget=forms.TimeInput(attrs={"type": "time"})
    )