import json

from flask import url_for

from app import flask_app


@flask_app.context_processor
def context_processors():
    return {
        'static_chunk': static_chunk,
    }


def static_chunk(filename):
    with open('static/webpack-manifest.json', 'r') as in_handle:
        manifest = json.loads(in_handle.read())

    static_file = manifest.get(filename)
    if static_file:
        return url_for('static', filename=static_file)
    return ''  # no matching file so return something that won't break html
