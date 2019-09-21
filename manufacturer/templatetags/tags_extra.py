from django import template
import calendar

register = template.Library()


@register.filter
def month_name(month_number):
    return calendar.month_name[int(month_number)][0:3]


@register.filter
def sentence_case(name):
    return str(name).title()


@register.filter
def upper_case(name):
    return str(name).upper()


@register.filter
def background_image(name):
    return "root/images/" + str(name).lower() + "_login.jpg"
