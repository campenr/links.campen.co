# Copyright 2016 Richard Campen
# All rights reserved
# This software is released under the Modified BSD license
# See LICENSE.txt for the full license documentation

"""Simple Flask application for creating/managing shortened URLs.

# LinkShortener 1.0.0

For complete documentation see README.md.
"""

import sys
import os

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from LinkShortener import app, db

app.config.from_object('config')
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()