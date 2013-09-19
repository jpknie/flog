from app import app, lm
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask import render_template, Flask, request, session, g, redirect, url_for, \
	abort, flash
from sqlalchemy.exc import IntegrityError
from forms import LoginForm, EntryForm, TagForm
from config import ITEMS_PER_PAGE, COLS_IN_TAG_TABLE
from utilities import chunks
from models import *

import datetime

@lm.user_loader
def load_user(userid):
	return User.query.get(int(userid))

@app.before_request
def before_request():
	g.user = current_user

@app.route('/')
@app.route('/entries')
@app.route('/entries/<int:page>')
def entries(page = 1):
	user = g.user
	page_title = "Flog 0.01"
	entries = Entry().all_entries().paginate(page, ITEMS_PER_PAGE, False)
	return render_template('entries.html', page_title = page_title, entries = entries)

@app.route('/add_tag', methods=['GET', 'POST'])
@login_required
def add_tag():
	if g.user.is_admin() != 1:
		flash('This user cannot add tags!')
		return redirect(url_for('tags'))
	form = TagForm(request.form)
	page_title = 'Add new tag'
	if request.method == 'POST' and form.validate_on_submit():
		tag = Tag()
		form.populate_obj(tag)
		try:
			db.session.add(tag)
			db.session.commit()
		except IntegrityError, exc:
			reason = exc.message
			if reason.find('unique constraint'):
				flash('Tag name already found in the database')
				db.session.rollback()
				return redirect(url_for('add_tag'))
		flash('Tag saved successfully')
		return redirect(url_for('tags'))
	return render_template('tag_editor.html', form_action = 'add_tag', form = form, page_title = page_title)

@app.route('/edit_tag/<int:tagid>', methods=['GET', 'POST'])
@login_required
def edit_tag(tagid):
	if g.user.is_admin() != 1:
		flash('This user cannot edit tags!')
		return redirect(url_for('tags'))
	tag = Tag.query.get(int(tagid))
	return render_template('tag_editor.html', form_action = 'edit_tag', form = form, page_title = page_title)

@app.route('/tags')
def tags():
	page_title = 'Tag collection'
	tags = Tag.query.all()
	admin = g.user.is_admin()
	tags = list(chunks(tags, COLS_IN_TAG_TABLE))
	return render_template('tags.html', page_title = page_title, tags = tags, admin = bool(admin))

@app.route('/add_entry', methods=['GET', 'POST'])
@login_required
def add_entry():
	form = EntryForm(request.form)
	page_title = 'Add new blog entry'
	if request.method == 'POST' and form.validate_on_submit():
		entry = Entry()
		entry.user_id = g.user.user_id
		entry.create_time = datetime.datetime.utcnow()
		form.populate_obj(entry)
		db.session.add(entry)
		db.session.commit()
		return redirect(url_for('entries'))
	return render_template('entry_editor.html', form_action = 'add_entry', form = form, page_title = page_title)

@app.route('/edit_entry/<int:entryid>', methods=['GET', 'POST'])
@login_required
def edit_entry(entryid):
	entry = Entry.query.get(int(entryid))
	if entry.user_id != g.user.user_id:
		flash("Cannot edit this entry.", 'error-message')
		return redirect(url_for('entries'))
	form = EntryForm(request.form, obj=entry)
	page_title = 'Edit blog entry'
	if request.method == 'POST' and form.validate_on_submit():
		# save new data in entry here
		form.populate_obj(entry)
		entry.create_time = datetime.datetime.utcnow()
		form.user_id = g.user.user_id
		db.session.add(entry)
		db.session.commit()
		return redirect(url_for('entries'))
	return render_template('entry_editor.html', form_action = 'edit_entry', form = form, page_title = page_title)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm(request.form)
	if form.validate_on_submit():
		user = User.query.filter_by(login_name = form.login_name.data).first()
		if user and (user.password == form.password.data):
			session['user_id'] = user.user_id
			flash('Welcome %s' % user.login_name)
			return redirect(url_for('entries'))
		flash('Wrong email or password', 'error-message')
	return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You were logged out')
	return redirect(url_for('login'))