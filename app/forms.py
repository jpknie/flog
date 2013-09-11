from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import Required, EqualTo, Email, Length

class LoginForm(Form):
	login_name = TextField('Login', [Required()])
	password = PasswordField('Password',[Required()])

class EntryForm(Form):
	title = TextField('Title',[Required()])
	text = TextAreaField('Content',[Required()])