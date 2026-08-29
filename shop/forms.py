from django import forms
from .models import Product,Category, Brand,ProductImage, ProductSpecification, ProductFeature,ProductComment


class ProductForm(forms.ModelForm):

    class Meta:

        model = Product

        fields = [
            "category",
            "brand",
            "name",
            "slug",
            "short_description",
            "description",
            "price",
            "discount_price",
            "stock",
            "image",
            "related_products",
            "is_active",
        ]

        widgets = {

            "name": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "slug": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "short_description": forms.Textarea(attrs={
                "class": "form-control",
                   "rows": 3
            }),

            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5
            }),

            "category": forms.Select(attrs={
                "class": "form-control"
            }),

            "brand": forms.Select(attrs={
                "class": "form-control"
            }),

            "price": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "discount_price": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "stock": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "image": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
            
            "related_products": forms.SelectMultiple(
             attrs={
            "class": "form-control"
            }
            ),

            "is_active": forms.CheckboxInput()

        }
class CategoryForm(forms.ModelForm):

    class Meta:

        model = Category

        fields = [
            "name",
            "slug",
        ]

        widgets = {

            "name": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "slug": forms.TextInput(attrs={
                "class": "form-control"
            }),

        }

class BrandForm(forms.ModelForm):

    class Meta:

        model = Brand

        fields = [
            "name",
            "slug",
            "logo",
        ]

        widgets = {

            "name": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "slug": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "logo": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
        }

class ProductImageForm(forms.ModelForm):

    class Meta:

        model = ProductImage

        fields = ["image"]

        widgets = {
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control"
            })
        }


class ProductSpecificationForm(forms.ModelForm):

    class Meta:

        model = ProductSpecification

        fields = [
            "title",
            "value",
        ]

        widgets = {

            "title": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "value": forms.TextInput(attrs={
                "class": "form-control"
            }),
        }


class ProductFeatureForm(forms.ModelForm):

    class Meta:

        model = ProductFeature

        fields = [
            "title",
        ]

        widgets = {

            "title": forms.TextInput(attrs={
                "class": "form-control"
            }),

        }

from .models import ProductComment


class ProductCommentForm(forms.ModelForm):

    class Meta:

        model = ProductComment

        fields = [
            "rating",
            "text",
        ]


        widgets = {

            "rating": forms.Select(
                choices=[
                    (5, "⭐⭐⭐⭐⭐"),
                    (4, "⭐⭐⭐⭐☆"),
                    (3, "⭐⭐⭐☆☆"),
                    (2, "⭐⭐☆☆☆"),
                    (1, "⭐☆☆☆☆"),
                ],
                attrs={
                    "class": "form-control"
                }
            ),


            "text": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "نظر شما درباره این محصول..."
                }
            ),

        }