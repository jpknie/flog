# Flog is basic blog application for Flask
# authored by Jani Nieminen (jpknie@utu.fi)

from flask import Flask

app = Flask(__name__)
from app import views

