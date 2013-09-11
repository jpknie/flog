from app import app, lm
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask import render_template, Flask, request, session, g, redirect, url_for, \
	abort, flash
from forms import LoginForm, EntryForm
from models import *

import datetime

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
	entries = Entry.query.options(db.joinedload('author')).order_by(Entry.id)
	return render_template('index.html', page_title = page_title, entries = entries)

@app.route('/add_entry', methods=['GET', 'POST'])
@login_required
def add_entry():
	form = EntryForm(request.form)
	page_title = 'Add new blog entry'
	if request.method == 'POST' and form.validate_on_submit():
		entry = Entry()
		entry.user_id = g.user.user_id
		entry.create_time = datetime.datetime.now()
		form.populate_obj(entry)
		db.session.add(entry)
		db.session.commit()
		return redirect(url_for('index'))
	return render_template('entry_editor.html', form_action = 'add_entry', form = form, page_title = page_title)

@app.route('/edit_entry/<int:entryid>', methods=['GET', 'POST'])
@login_required
def edit_entry(entryid):
	entry = Entry.query.get(int(entryid))
	if entry.user_id != g.user.user_id:
		flash("Cannot edit this entry.", 'error-message')
		return redirect(url_for('index'))
	form = EntryForm(request.form, obj=entry)
	page_title = 'Edit blog entry'
	if request.method == 'POST' and form.validate_on_submit():
		# save new data in entry here
		form.populate_obj(entry)
		form.user_id = g.user.user_id
		db.session.add(entry)
		db.session.commit()
		return redirect(url_for('index'))
	return render_template('entry_editor.html', form_action = 'edit_entry', form = form, page_title = page_title)

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