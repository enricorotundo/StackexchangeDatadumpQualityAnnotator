from django import template

register = template.Library()


@register.filter
def translateQuality(value):
    if value == -1:
        return "Don't know"
    if value == 0:
        return "Low"
    if value == 1:
        return  "Medium"
    if value == 2:
        return "High"


