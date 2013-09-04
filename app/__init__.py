# Flog is basic blog application for Flask
# authored by Jani Nieminen (jpknie@utu.fi)

from database import db_session
from flask import Flask
from flask.ext.login import LoginManager

app = Flask(__name__)
app.config.from_object('config')

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

from app import views
