# -*- coding: utf-8 -*-
from app import app
from flask import render_template,flash,redirect
from .forms import LoginForm
@app.route('/')
@app.route('/index')
def index():
	user = {'nickname': 'Magic'}
	posts =[{'author': {'nickname': u'6LW15q+F54+C'}, 
            'body': 'MeWkqeawlCggXl9eICnkuI3plJnlmJsh' },
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
@app.route('/login',methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash('Login requested for OpenID="%s", remember_me=%s' %
              (form.openid.data, str(form.remember_me.data)))
		return redirect('/index')
	return render_template('login.html',
							title='Sign in',
							form=form)
