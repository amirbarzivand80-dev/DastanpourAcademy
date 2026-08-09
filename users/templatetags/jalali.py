from django import template
from khayyam import JalaliDate

register = template.Library()


@register.filter
def to_jalali(value):

    if not value:
        return ""

    try:
        return JalaliDate(value).strftime("%Y/%m/%d")
    except:
        return value