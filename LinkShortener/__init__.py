# Copyright 2016 Richard Campen
# All rights reserved
# This software is released under the Modified BSD license
# See LICENSE.txt for the full license documentation

"""
LinkShortener v0.3.1

A Flask app for creating/managing short links for longer length URLs.
"""

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

from LinkShortener import views, models, forms

app.jinja_env.filters['date_filter'] = models.Link.format_date
