from app import app
from flask import render_template

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
