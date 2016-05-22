# -*- coding: utf-8 -*-
from app import app
from flask import render_template
@app.route('/')
@app.route('/index')
def index():
	user = {'nickname': 'Magic'}
	posts =[{'author': {'nickname': 'John'}, 
            'body': '1Beautiful day in Portland!' },
			{'author': {'nickname': 'John'}, 
            'body': '1Beautiful day in Portland!' },
			{'author': {'nickname': 'John'}, 
            'body': '1Beautiful day in Portland!' },
			{'author': {'nickname': 'John'}, 
            'body': '1Beautiful day in Portland!' },
			{'author': {'nickname': 'John'}, 
            'body': '1Beautiful day in Portland!' },
			{'author': {'nickname': '2John'}, 
            'body': '2Beautiful day in Portland!' }]
	return render_template('index.html',
							title='Home',
							user=user,
							posts=posts)

