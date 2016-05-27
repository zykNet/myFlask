# -*- coding: utf-8 -*-
from app import db
from flask.ext.login import	 UserMixin
from hashlib import md5
class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	nickname = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	posts = db.relationship('Post', backref='author', lazy='dynamic')
	about_me = db.Column(db.String(140))
	last_seen = db.Column(db.DateTime)
	@property
	def is_authenticated(self):
		return True

	@property
	def is_active(self):
		return True

	@property
	def is_anonymous(self):
		return False
	def avatar(self, size):
		return 'http://www.gravatar.com/avatar/%s?d=retro&s=%d' % (md5(self.email.encode('utf-8')).hexdigest(), size)
		
	def get_id(self):
		return unicode(self.id)	 # python 2

	def __repr__(self):
		return '<User %r>'% (self.nickname)

class Post(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Post %r>' % (self.body)