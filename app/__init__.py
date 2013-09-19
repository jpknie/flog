# Flog is basic blog application for Flask
# authored by Jani Nieminen (jpknie@utu.fi)

from flask import Flask
from flask.ext.login import LoginManager

app = Flask(__name__)
app.config.from_object('config')

from utilities import MomentJS
app.jinja_env.globals['momentjs'] = MomentJS

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

from app import views
