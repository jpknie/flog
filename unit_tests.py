import os
import pytest

from app import app
from app.database import db
from app.models import *

class TestUser:
	def test_user():


	def setUp(self):
		app.config['TESTING'] = True
		app.config['CSRF_ENABLED'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://janiniem:devpass@localhost/flog'
		self.app = app.test_client()
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

class TestEntry(unittest.TestCase):
	def setUp(self):
		app.config['TESTING'] = True
		app.config['CSRF_ENABLED'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://janiniem:devpass@localhost/flog'
		self.app = app.test_client()
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

if __name__ == 'main':
	unittest.main()