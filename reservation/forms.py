from django import forms

from .models import BarberBlockedTime, Reservation


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
            "date": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),

            "start_time": forms.TimeInput(
                attrs={
                    "type": "time"
                }
            ),

            "end_time": forms.TimeInput(
                attrs={
                    "type": "time"
                }
            ),
        }


class WalkInReservationForm(forms.ModelForm):

    class Meta:
        model = Reservation

        fields = [
            "customer_name",
            "customer_phone",
            "service",
            "date",
            "time",
        ]

        widgets = {
            "date": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),

            "time": forms.TimeInput(
                attrs={
                    "type": "time"
                }
            ),
        }