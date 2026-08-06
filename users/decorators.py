from django.contrib.auth.decorators import user_passes_test


def superadmin_required(view_func):
    return user_passes_test(
        lambda u: u.is_authenticated and u.groups.filter(name="SuperAdmin").exists()
    )(view_func)


def admin_required(view_func):
    return user_passes_test(
        lambda u: u.is_authenticated and (
            u.groups.filter(name="SuperAdmin").exists() or
            u.groups.filter(name="Admin").exists()
        )
    )(view_func)


def barber_required(view_func):
    return user_passes_test(
        lambda u: u.is_authenticated and (
            u.groups.filter(name="SuperAdmin").exists() or
            u.groups.filter(name="Barber").exists()
        )
    )(view_func)