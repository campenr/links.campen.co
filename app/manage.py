import sys
import os

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app import flask_app, db

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = flask_app

MIGRATION_DIR = os.path.join(PROJECT_DIR, 'app', 'migrations')

migrate = Migrate(app, db, directory=MIGRATION_DIR)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
