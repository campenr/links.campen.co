from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_oauthlib.client import OAuth


flask_app = Flask(__name__)

flask_app.config.from_object('config')
db = SQLAlchemy(flask_app)
oauth = OAuth(flask_app)

google = oauth.remote_app(
    'google',
    consumer_key=flask_app.config.get('GOOGLE_OAUTH')['client_id'],
    consumer_secret=flask_app.config.get('GOOGLE_OAUTH')['client_secret'],
    request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email'},
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth'
)

login_manager = LoginManager()
login_manager.init_app(flask_app)
login_manager.login_view = "login"

from app import views, models, forms, api