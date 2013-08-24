# Flog is basic blog application for Flask
# authored by Jani Nieminen (jpknie@utu.fi)

from flask import Flask

app = Flask(__name__)
app.config.from_object('config')
from app import views

