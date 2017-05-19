# Copyright 2016 Richard Campen
# All rights reserved
# This software is released under the Modified BSD license
# See LICENSE.txt for the full license documentation

"""
LinkShortener v0.3.2

A Flask app for creating/managing short links for longer length URLs.
"""

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_oauthlib.client import OAuth

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
oauth = OAuth(app)

google = oauth.remote_app(
    'google',
    consumer_key=app.config.get('GOOGLE_OAUTH')['client_id'],
    consumer_secret=app.config.get('GOOGLE_OAUTH')['client_secret'],
    request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email'},
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth'
)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

from LinkShortener import views, models, forms

app.jinja_env.filters['date_filter'] = models.Link.format_date
