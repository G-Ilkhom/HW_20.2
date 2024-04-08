from django import template

register = template.Library()


@register.simple_tag
def media_url(data):
    if data:
        return f'/media/{data}'
    return '#'
