from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import Required, EqualTo, Email

class LoginForm(Form):
	login_name = TextField('Login', [Required()])
	password = PasswordField('Password',[Required()])
