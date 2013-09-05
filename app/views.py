from app import app, lm
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask import render_template, Flask, request, session, g, redirect, url_for, \
	abort, flash
from forms import LoginForm
from models import *

@lm.user_loader
def load_user(userid):
	return User.query.get(int(userid))

@app.before_request
def before_request():
	g.user = current_user

@app.route('/')
@app.route('/index')
@login_required
def index():
	user = g.user
	page_title = "Flog 0.01"
	entries = [
		{
			'title': 'First post',
			'author': { 'name': 'Jani Nieminen' },
			'body': 'Eka postaus'
		},
		{
			'title': 'Second post',
			'author': { 'name': 'Jani Nieminen' },
			'body': 'Toka postaus'
		}
	]
	return render_template('index.html', page_title=page_title, entries = entries)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm(request.form)
	if form.validate_on_submit():
		user = User.query.filter_by(login_name = form.login_name.data).first()
		if user and (user.password == form.password.data):
			session['user_id'] = user.user_id
			flash('Welcome %s' % user.login_name)
			return redirect(url_for('index'))
		flash('Wrong email or password', 'error-message')
	return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You were logged out')
	return redirect(url_for('login'))