from app import app
from flask.ext.sqlalchemy import SQLAlchemy
import os

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://janiniem:devpass@localhost/flog'

db = SQLAlchemy(app)
