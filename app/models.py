from flask.ext.sqlalchemy import SQLAlchemy
from database import db

tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('entry_id', db.Integer, db.ForeignKey('entry.id'))
)

class User(db.Model):
	__tablename__ = 'user'

	user_id = db.Column(db.Integer, primary_key = True)
	realname = db.Column(db.String(200), nullable = False)
	login_name = db.Column(db.String(100), nullable = False)
	password = db.Column(db.String(200), nullable = False)
	admin = db.Column(db.SmallInteger, default = 0)
	entries = db.relationship('Entry', backref = 'author', lazy = 'joined')

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

class Entry(db.Model):
	__tablename__ = 'entry'

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(200), unique=False)
	create_time = db.Column(db.DateTime)
	text = db.Column(db.String(500), unique=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
	tags = db.relationship('Tag', secondary=tags, backref=db.backref('entries', lazy='dynamic'))

	def __repr__(self):
		return '<Entry %r, %r, %r>' % (self.title, self.create_time, self.text)

class Tag(db.Model):
	__tablename__ = 'tag'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200))

	def __init__(self, name):
		self.name = name
