from django.shortcuts import render, get_object_or_404
from .models import Service, ServiceCategory

def services_view(request):

    services = Service.objects.filter(
        is_active=True
    ).order_by("order")

    categories = ServiceCategory.objects.all()

    return render(
        request,
        "core/services.html",
        {
            "services": services,
            "categories": categories,
        }
    )


def service_detail(request, id):
    service = get_object_or_404(        Service,        id=id    )
    images = service.images.all()
    return render(        request,        "core/service_detail.html",        {            "service": service,            "images": images,        }    )

    return render(
        request,
        "core/service_detail.html",
        {
            "service": service
        }
    )

