from django import template

register = template.Library()


@register.filter
def price_format(value):
    try:
        return f"{int(value):,}"
    except (ValueError, TypeError):
        return value