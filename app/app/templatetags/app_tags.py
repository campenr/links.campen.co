import json

from django import template
from django.templatetags.static import static

register = template.Library()


@register.simple_tag
def static_chunk(filename):
    with open('static/webpack-manifest.json', 'r') as in_handle:
        manifest = json.loads(in_handle.read())

    static_file = manifest.get(filename)
    if static_file:
        return static(static_file)
    return ''  # no matching file so return something that won't break html
