from sqlalchemy import Column, Integer, String, SmallInteger
from database import Base

class User(Base):
	__tablename__ = 'user'

	user_id = Column(Integer, primary_key = True)
	realname = Column(String(200), nullable = False)
	login_name = Column(String(100), nullable = False)
	password = Column(String(200), nullable = False)
	admin = Column(SmallInteger, default = 0)

	def __init__(self, realname=None, login_name=None, password=None):
		self.realname = realname
		self.login_name = login_name
		self.password = password

	def is_admin(self):
		return bool(self.admin)

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)

	def __repr__(self):
		return '<User %r, %r, %r>' % (self.user_id, self.realname, self.login_name)

class Entry(Base):
	__tablename__ = 'entry'

	id = Column(Integer, primary_key=True)
	title = Column(String(20), unique=False)
	text = Column(String(200), unique=False)

	def __init__(self, title=None, text=None):
		self.title = title
		self.text = text

	def __repr__(self):
		return '<Entry %r>' % (self.title)
