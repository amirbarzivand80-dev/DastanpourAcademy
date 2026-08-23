
from django import forms

from .models import DiscountCode


class DiscountCodeForm(forms.ModelForm):

    # =========================================================
    # انتخاب محدوده محصول
    # =========================================================

    product_target = forms.ChoiceField(
        label="محدوده محصولات",
        choices=[
            ("none", "هیچ‌کدام"),
            ("selected", "محصولات خاص"),
            ("all", "همه محصولات"),
        ],
        widget=forms.RadioSelect,
        required=True,
    )

    # =========================================================
    # انتخاب محدوده دوره
    # =========================================================

    course_target = forms.ChoiceField(
        label="محدوده دوره‌ها",
        choices=[
            ("none", "هیچ‌کدام"),
            ("selected", "دوره‌های خاص"),
            ("all", "همه دوره‌ها"),
        ],
        widget=forms.RadioSelect,
        required=True,
    )

    # =========================================================
    # انتخاب محدوده خدمت
    # =========================================================

    service_target = forms.ChoiceField(
        label="محدوده خدمات",
        choices=[
            ("none", "هیچ‌کدام"),
            ("selected", "خدمات خاص"),
            ("all", "همه خدمات"),
        ],
        widget=forms.RadioSelect,
        required=True,
    )

    # =========================================================
    # انتخاب کاربران
    # =========================================================

    user_target = forms.ChoiceField(
        label="کاربران مجاز",
        choices=[
            ("all", "همه کاربران"),
            ("selected", "کاربران خاص"),
        ],
        widget=forms.RadioSelect,
        required=True,
    )

    class Meta:

        model = DiscountCode

        fields = [
            "code",
            "discount_type",
            "value",

            "products",
            "courses",
            "services",

            "users",

            "is_active",
            "start_date",
            "end_date",

            "minimum_purchase",
            "usage_limit",
            "per_user_limit",
        ]

        widgets = {

            "code": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "مثلاً: SUMMER1405",
                    "autocomplete": "off",
                }
            ),

            "discount_type": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "value": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1",
                    "placeholder": "مثلاً 20 یا 500000",
                }
            ),

            "products": forms.SelectMultiple(
                attrs={
                    "class": "form-control multi-select",
                }
            ),

            "courses": forms.SelectMultiple(
                attrs={
                    "class": "form-control multi-select",
                }
            ),

            "services": forms.SelectMultiple(
                attrs={
                    "class": "form-control multi-select",
                }
            ),

            "users": forms.SelectMultiple(
                attrs={
                    "class": "form-control multi-select",
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),

            "start_date": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                }
            ),

            "end_date": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                }
            ),

            "minimum_purchase": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "placeholder": "0 یعنی بدون محدودیت",
                }
            ),

            "usage_limit": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1",
                    "placeholder": "خالی = نامحدود",
                }
            ),

            "per_user_limit": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1",
                    "placeholder": "مثلاً 1",
                }
            ),
        }

    # =========================================================
    # مقداردهی اولیه
    # =========================================================

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["products"].required = False
        self.fields["courses"].required = False
        self.fields["services"].required = False
        self.fields["users"].required = False

        # -----------------------------------------------------
        # تعیین وضعیت فعلی محصول
        # -----------------------------------------------------

        if self.instance.pk:

            if self.instance.products_all:

                self.initial["product_target"] = "all"

            elif self.instance.products.exists():

                self.initial["product_target"] = "selected"

            else:

                self.initial["product_target"] = "none"

        else:

            self.initial["product_target"] = "none"

        # -----------------------------------------------------
        # تعیین وضعیت فعلی دوره
        # -----------------------------------------------------

        if self.instance.pk:

            if self.instance.courses_all:

                self.initial["course_target"] = "all"

            elif self.instance.courses.exists():

                self.initial["course_target"] = "selected"

            else:

                self.initial["course_target"] = "none"

        else:

            self.initial["course_target"] = "none"

        # -----------------------------------------------------
        # تعیین وضعیت فعلی خدمت
        # -----------------------------------------------------

        if self.instance.pk:

            if self.instance.services_all:

                self.initial["service_target"] = "all"

            elif self.instance.services.exists():

                self.initial["service_target"] = "selected"

            else:

                self.initial["service_target"] = "none"

        else:

            self.initial["service_target"] = "none"

        # -----------------------------------------------------
        # تعیین وضعیت کاربران
        # -----------------------------------------------------

        if self.instance.pk:

            if self.instance.users.exists():

                self.initial["user_target"] = "selected"

            else:

                self.initial["user_target"] = "all"

        else:

            self.initial["user_target"] = "all"

    # =========================================================
    # ذخیره
    # =========================================================

    def save(self, commit=True):

        instance = super().save(commit=False)

        # =====================================================
        # محصولات
        # =====================================================

        product_target = self.cleaned_data.get(
            "product_target"
        )

        if product_target == "all":

            instance.products_all = True

        else:

            instance.products_all = False

        # =====================================================
        # دوره‌ها
        # =====================================================

        course_target = self.cleaned_data.get(
            "course_target"
        )

        if course_target == "all":

            instance.courses_all = True

        else:

            instance.courses_all = False

        # =====================================================
        # خدمات
        # =====================================================

        service_target = self.cleaned_data.get(
            "service_target"
        )

        if service_target == "all":

            instance.services_all = True

        else:

            instance.services_all = False

        # =====================================================
        # ذخیره اصلی
        # =====================================================

        if commit:

            instance.save()

            # =================================================
            # خیلی مهم:
            # ذخیره روابط ManyToMany
            # =================================================

            self.save_m2m()

            # -------------------------------------------------
            # محصولات
            # -------------------------------------------------

            if product_target == "none":

                instance.products.clear()

            elif product_target == "all":

                instance.products.clear()

            # -------------------------------------------------
            # دوره‌ها
            # -------------------------------------------------

            if course_target == "none":

                instance.courses.clear()

            elif course_target == "all":

                instance.courses.clear()

            # -------------------------------------------------
            # خدمات
            # -------------------------------------------------

            if service_target == "none":

                instance.services.clear()

            elif service_target == "all":

                instance.services.clear()

            # -------------------------------------------------
            # کاربران
            # -------------------------------------------------

            user_target = self.cleaned_data.get(
                "user_target"
            )

            if user_target == "all":

                instance.users.clear()

            return instance

        return instance

    # =========================================================
    # اعتبارسنجی
    # =========================================================

    def clean(self):

        cleaned_data = super().clean()

        discount_type = cleaned_data.get("discount_type")
        value = cleaned_data.get("value")

        product_target = cleaned_data.get(
            "product_target"
        )

        course_target = cleaned_data.get(
            "course_target"
        )

        service_target = cleaned_data.get(
            "service_target"
        )

        user_target = cleaned_data.get(
            "user_target"
        )

        # =====================================================
        # مقدار تخفیف
        # =====================================================

        if value is not None and value <= 0:

            self.add_error(
                "value",
                "مقدار تخفیف باید بیشتر از صفر باشد."
            )

        # =====================================================
        # درصد
        # =====================================================

        if discount_type == "percent" and value is not None:

            if value > 100:

                self.add_error(
                    "value",
                    "تخفیف درصدی نمی‌تواند بیشتر از ۱۰۰٪ باشد."
                )

        # =====================================================
        # محصول خاص
        # =====================================================

        if product_target == "selected":

            products = cleaned_data.get("products")

            if not products:

                self.add_error(
                    "products",
                    "حداقل یک محصول را انتخاب کنید."
                )

        # =====================================================
        # دوره خاص
        # =====================================================

        if course_target == "selected":

            courses = cleaned_data.get("courses")

            if not courses:

                self.add_error(
                    "courses",
                    "حداقل یک دوره را انتخاب کنید."
                )

        # =====================================================
        # خدمت خاص
        # =====================================================

        if service_target == "selected":

            services = cleaned_data.get("services")

            if not services:

                self.add_error(
                    "services",
                    "حداقل یک خدمت را انتخاب کنید."
                )

        # =====================================================
        # کاربر خاص
        # =====================================================

        if user_target == "selected":

            users = cleaned_data.get("users")

            if not users:

                self.add_error(
                    "users",
                    "حداقل یک کاربر را انتخاب کنید."
                )

        # =====================================================
        # تاریخ
        # =====================================================

        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date:

            if end_date <= start_date:

                self.add_error(
                    "end_date",
                    "تاریخ پایان باید بعد از تاریخ شروع باشد."
                )

        # =====================================================
        # حداقل خرید
        # =====================================================

        minimum_purchase = cleaned_data.get(
            "minimum_purchase"
        )

        if (
            minimum_purchase is not None
            and minimum_purchase < 0
        ):

            self.add_error(
                "minimum_purchase",
                "مبلغ نمی‌تواند منفی باشد."
            )

        # =====================================================
        # محدودیت استفاده
        # =====================================================

        usage_limit = cleaned_data.get(
            "usage_limit"
        )

        if (
            usage_limit is not None
            and usage_limit <= 0
        ):

            self.add_error(
                "usage_limit",
                "محدودیت استفاده باید بیشتر از صفر باشد."
            )

        # =====================================================
        # محدودیت هر کاربر
        # =====================================================

        per_user_limit = cleaned_data.get(
            "per_user_limit"
        )

        if (
            per_user_limit is not None
            and per_user_limit <= 0
        ):

            self.add_error(
                "per_user_limit",
                "محدودیت استفاده برای هر کاربر باید بیشتر از صفر باشد."
            )

        return cleaned_data
