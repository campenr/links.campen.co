from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.flask_client import OAuth


flask_app = Flask(__name__)

flask_app.config.from_object('config')
db = SQLAlchemy(flask_app)
oauth = OAuth(flask_app)

oauth.register(
    name='google',
    client_id=flask_app.config.get('GOOGLE_OAUTH_CLIENT_ID'),
    client_secret=flask_app.config.get('GOOGLE_OAUTH_CLIENT_SECRET'),
    client_kwargs={'scope': 'https://www.googleapis.com/auth/userinfo.email'},
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth'
)

login_manager = LoginManager()
login_manager.init_app(flask_app)
login_manager.login_view = "login"

from app import views, models, forms, api