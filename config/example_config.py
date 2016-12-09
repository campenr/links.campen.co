# Copyright 2016 Richard Campen
# All rights reserved
# This software is released under the Modified BSD license
# See LICENSE.txt for the full license documentation

"""Simple Flask application for creating/managing shortened URLs.

# LinkShortener 1.0.0

For complete documentation see README.md.
"""

# Set the values below as indicated, and rename this file to __init__.py

import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Set this to something unique
SECRET_KEY = ""

# Set this to the URI to the database that you wish to use for this application
SQLALCHEMY_DATABASE_URI = ""

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False
