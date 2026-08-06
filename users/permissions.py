from django.contrib.auth.models import Group


def is_superadmin(user):
    return user.groups.filter(name="SuperAdmin").exists()


def is_admin(user):
    return user.groups.filter(name="Admin").exists()


def is_barber(user):
    return user.groups.filter(name="Barber").exists()


def is_admin_or_super(user):
    return (
        is_superadmin(user)
        or is_admin(user)
    )


def is_barber_or_super(user):
    return (
        is_superadmin(user)
        or is_barber(user)
    )