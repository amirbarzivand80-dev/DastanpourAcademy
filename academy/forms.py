from django import forms
from .models import Course


class CourseForm(forms.ModelForm):

    class Meta:
        model = Course

        fields = [
            "title",
            "slug",
            "course_type",
            "teacher",
            "description",
            "price",
            "image",
            "start_date",
            "start_time",
            "end_time",
            "capacity",
            "location",
            "duration",
            "is_active",
        ]

        widgets = {
            "description": forms.Textarea(
                attrs={
                    "rows": 5
                }
            ),
        }