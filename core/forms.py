from django import forms
from .models import ContactMessage

class ContactMessageForm(forms.ModelForm):

    class Meta:

        model = ContactMessage

        fields = [
            "full_name",
            "phone",
            "email",
            "message"
        ]

        widgets = {

            "full_name": forms.TextInput(attrs={
                "placeholder": "نام و نام خانوادگی"
            }),

            "phone": forms.TextInput(attrs={
                "placeholder": "شماره تماس"
            }),

            "email": forms.EmailInput(attrs={
                "placeholder": "ایمیل (اختیاری)"
            }),

            "message": forms.Textarea(attrs={
                "rows": 6,
                "placeholder": "پیام شما..."
            }),

        }