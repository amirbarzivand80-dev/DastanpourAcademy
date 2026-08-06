from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def permission_required(permission_name):

    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            # سوپرادمین همیشه اجازه دارد
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            # اگر اصلاً رکورد دسترسی ندارد
            if not hasattr(request.user, "admin_permission"):
                messages.error(
                    request,
                    "شما دسترسی لازم را ندارید."
                )
                return redirect("superadmin_dashboard")

            permission = request.user.admin_permission

            if getattr(permission, permission_name):

                return view_func(request, *args, **kwargs)

            messages.error(
                request,
                "شما اجازه ورود به این بخش را ندارید."
            )

            return redirect("superadmin_dashboard")

        return wrapper

    return decorator