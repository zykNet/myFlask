# -*- coding: utf-8 -*-
from app import app,db,lm,oid
from flask import render_template,flash,redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from .forms import LoginForm, EditForm, PostForm, SearchForm
from .models import User, Post
from .emails import follower_notification
from app import babel
from config import LANGUAGES
from flask.ext.babel import gettext
from guess_language import guessLanguage
from flask import jsonify
from .translate import microsoft_translate
from random import randint

from datetime import datetime
from config import POSTS_PER_PAGE, MAX_SEARCH_RESULTS,TEST_NUM

def test1_init():
	nums = {}
	for i in xrange(TEST_NUM):
		ran = randint(10000,99999)
		nums[i] = ran
	session['test1_1'] = nums#存储随机数据
	session['test1_2'] = TEST_NUM#存储全局变量
@app.route('/test1')
@app.route('/test1/<int:num>')
def test1(num = 0):
	if num == 0:#初始化
		test1_init()
	session['test1_2'] = session['test1_2']-1
	
	if session['test1_2'] == 0:#终止
		return render_template('index.html')
	ok = session['test1_1'] 
	try:
		if num == ok[session['test1_2']]:
			return render_template('test1.html',
									next = ok[session['test1_2']-1],
									flag = True)
		else:
			session['test1_2'] = TEST_NUM
			return render_template('test1.html',
									next = ok[session['test1_2']-1],
									flag = False)
	except:
		if num == ok[str(session['test1_2'])]:
			return render_template('test1.html',
									next = ok[str(session['test1_2']-1)],
									flag = True)
		else:
			session['test1_2'] = TEST_NUM
			print 'here'
			return render_template('test1.html',
									next = ok[str(session['test1_2']-1)],
									flag = False)

@app.route('/design')
def design():
	return render_template('base.html')

@app.route('/translate', methods=['POST'])
@login_required
def translate():
	return jsonify({'text':'ok,translate test.'})
	return jsonify({ 
		'text': microsoft_translate(
			request.form['text'], 
			request.form['sourceLang'], 
			request.form['destLang']) })
			
@app.route('/follow/<nickname>')
@login_required
def follow(nickname):
	user = User.query.filter_by(nickname=nickname).first()
	if user is None: 
		flash('User %s not found.'% nickname)
	u = g.user.follow(user)
	if u is None:
		flash('User %s is None:view21.'% nickname)
		return redirect(url_for('user', nickname=nickname))
	db.session.add(u)
	db.session.commit()
	flash('User %s successful followed.'% nickname)
	follower_notification(user, g.user)
	return redirect(url_for('user', nickname=nickname))
	
@app.route('/unfollow/<nickname>')
def unfollow(nickname):
	user = User.query.filter_by(nickname=nickname).first()
	if user is None: 
		flash('User %s not found.'% nickname)
	u = g.user.unfollow(user)
	if u is None:
		flash('Cannot unfollow ' + nickname + '.')
		return redirect(url_for('user', nickname=nickname))
	db.session.add(u)
	db.session.commit()
	flash('You have stopped following ' + nickname + '.')
	return redirect(url_for('user', nickname=nickname))
	
@app.route('/edit',methods=['GET', 'POST'])
@login_required
def edit():
	form = EditForm(g.user.nickname)
	if form.validate_on_submit():
		g.user.nickname = form.nickname.data
		g.user.about_me = form.about_me.data
		db.session.add(g.user)
		db.session.commit()
		flash('Your changes have been saved.')
		return redirect(url_for('edit'))
	else:
		form.nickname.data = g.user.nickname
		form.about_me.data = g.user.about_me
		flash('Your changes Fall.')
	return render_template('edit.html', form=form)
	
@app.route('/',methods=['GET','POST'])
@app.route('/index',methods=['GET','POST'])
@app.route('/index/<int:page>', methods=['GET', 'POST'])
@login_required
def index(page=1):
	user = g.user
	form = PostForm()
	if form.validate_on_submit():
		language = guessLanguage(form.post.data)
		if language == 'UNKNOWN' or len(language) > 5:
			language = ''
		post=Post(body=form.post.data, timestamp=datetime.utcnow(), author=g.user, language=language)
		db.session.add(post)
		db.session.commit()
		flash('You post successful.')
		return redirect(url_for('index'))
	posts = g.user.followed_posts().paginate(page, POSTS_PER_PAGE, False)
	return render_template('index.html',
							title='Home',
							user=user,
							form=form,
							posts=posts)
							
@app.route('/login',methods=['GET','POST'])
@oid.loginhandler
def login():
	if g.user is not None and g.user.is_authenticated:
		flash(gettext('log out please'))
		# (u'你已经登录，先退出！')
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		#app.logger.error(form.remember_me.data)
		session['remember_me'] = form.remember_me.data
		return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
	return render_template('login.html',
							title='Sign in',
							form=form,
							providers=app.config['OPENID_PROVIDERS'])

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/user/<nickname>')
@app.route('/user/<nickname>/<int:page>')
@login_required
def user(nickname,page=1):
	user = User.query.filter_by(nickname=nickname).first()
	if user == None:
		flash('User %s not found.' % nickname)
		return redirect(url_for('index'))
	user = User.query.filter_by(nickname=nickname).first()
	posts = Post.query.filter(Post.user_id == user.id).order_by(Post.timestamp.desc()).paginate(page, POSTS_PER_PAGE, False)
	return render_template('user.html',
						   user=user,
						   posts=posts
						   ,flash=flash)
@app.route('/search', methods=['GET','POST'])
@login_required
def search():
	if not g.search_form.validate_on_submit():
		return redirect(url_for('index'))
	return redirect(url_for('search_results', query= g.search_form.search.data))
	
@app.route('/search_results/<query>', methods=['GET','POST'])
@login_required
def search_results(query):
	results = Post.query.whoosh_search(query, MAX_SEARCH_RESULTS).all()
	return render_template('search_results.html',
						   query=query,
						   results=results)

@app.errorhandler(404)
def not_found_error(error):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
	db.session.rollback()
	return render_template('500.html'), 500		
	
@oid.after_login
def after_login(resp):
	if resp.email is None or resp.email == "":
		flash('Invalid login. Please try again.')
		return redirect(url_for('login'))
	user = User.query.filter_by(email=resp.email).first()
	if user is None:
		nickname = resp.nickname
		if nickname is None or nickname == "":
			nickname = resp.email.split('@')[0]
		nickname = User.make_unique_nickname(nickname)
		user = User(nickname=nickname, email=resp.email)
		db.session.add(user)
		db.session.add(user.follow(user))
		db.session.commit()
	remember_me = False
	if 'remember_me' in session:
		remember_me = session['remember_me']
		session.pop('remember_me', None)#666
	login_user(user, remember = remember_me)
	return redirect(request.args.get('next') or url_for('index'))

@lm.user_loader
def load_user(id):
	return User.query.get(int(id))
	
@app.before_request
def before_request():
	g.user = current_user#defin by flask_login
	g.search_form = SearchForm() 
	if g.user.is_authenticated:
		g.user.last_seen = datetime.utcnow()
		db.session.add(g.user)
		db.session.commit()
@babel.localeselector
def get_locale():
	return request.accept_languages.best_match(LANGUAGES.keys())