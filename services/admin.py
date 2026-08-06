from django.contrib import admin
from .models import Service, ServiceImage, ServiceCategory

class ServiceImageInline(admin.TabularInline):

    model = ServiceImage

    extra = 1


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):

    list_display = (
         "name",  
          "category",  
          "price",    
          "order",   
         "is_active",
    )
    list_filter = (
    "category",
    "is_active",
    )

    ordering = (
    "order",
    )

    inlines = [
        ServiceImageInline
    ]


admin.site.register(ServiceImage)
admin.site.register(ServiceCategory)