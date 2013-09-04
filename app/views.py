from app import app
from flask import render_template, Flask, request, session, g, redirect, url_for, \
	abort, flash

from models import *

@app.route('/')
@app.route('/index')
def index():
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
  error = None
  if request.method == 'POST':
	if request.form['username'] != app.config['USERNAME']:
		error = 'Invalid Username'
	elif request.form['password'] != app.config['PASSWORD']:
		error = 'Invalid password'
	else:
		session['logged_in'] = True
		flash('You were logged in')
		return redirect(url_for('show_entries'))
  return render_template('login.html', error=error)

@app.route('/logout')
def logout():
  session.pop('logged_in', None)
  flash('You were logged out')
  return redirect(url_for('show_entries'))