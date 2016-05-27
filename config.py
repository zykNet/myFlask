# -*- coding: utf-8 -*-
# form crse??
WTF_CSRF_ENABLED =True
SECRET_KEY = 'you-will-never-guess'

#openId
OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
	{'name': 'Open id [china]', 'url': 'http://<username>.openid.org.cn/'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]
# database
import os
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True