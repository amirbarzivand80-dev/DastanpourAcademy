from django import forms

from users.models import CustomUser
from reservation.models import Barber
from .models import AdminPermission

class UserEditForm(forms.ModelForm):

    class Meta:
        model = CustomUser

        fields = [
            "full_name",
            "phone",
            "address",
            "birth_date",
            "marriage_date",
            "child_birth",
            "profile_image",
            "is_active",
        ]

        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
            "marriage_date": forms.DateInput(attrs={"type": "date"}),
            "child_birth": forms.DateInput(attrs={"type": "date"}),
        }


class BarberForm(forms.ModelForm):

    user = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(
            barber__isnull=True
        ),
        label="انتخاب کاربر"
    )

    class Meta:
        model = Barber

        fields = [
            "user",
            "work_start",
            "work_end",
            "appointment_duration",
            "is_active",
        ]

        widgets = {
            "work_start": forms.TimeInput(attrs={"type": "time"}),
            "work_end": forms.TimeInput(attrs={"type": "time"}),
        }

        
class BarberEditForm(forms.ModelForm):

    class Meta:
        model = Barber

        fields = [
            "work_start",
            "work_end",
            "appointment_duration",
            "is_active",
        ]

        widgets = {
            "work_start": forms.TimeInput(
                attrs={"type": "time"}
            ),

            "work_end": forms.TimeInput(
                attrs={"type": "time"}
            ),

            "appointment_duration": forms.NumberInput(
                attrs={"min": 15}
            ),
        }
class AdminPermissionForm(forms.ModelForm):

    class Meta:

        model = AdminPermission

        exclude = ["user"]