from django import template
import calendar

register = template.Library()


@register.filter
def month_name(month_number):
    return calendar.month_name[int(month_number)][0:3]


@register.filter
def sentence_case(name):
    if str(name) == 'rto':
        return str(name).upper()
    else:
        return str(name).title()


@register.filter
def upper_case(name):
    return str(name).upper()


@register.filter
def background_image(name):
    return "root/images/usertypes/" + str(name).lower() + "_login.jpg"


@register.filter
def vehicle_label(key):
    key = str(key).replace('_', ' ')
    key = str(key).capitalize()
    return key
