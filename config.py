# -*- coding: utf-8 -*-
# form crse??
WTF_CSRF_ENABLED =True
SECRET_KEY = 'you-will-never-guess'
# pagination
POSTS_PER_PAGE = 3
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
#email
MAIL_SERVER = 'mail.qq.com'
MAIL_PORT = 456
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
# MAIL_USERNAME = 'zyknet'
# MAIL_PASSWORD = 123456

# administrator list
ADMINS = ['602836219@qq.com']
# search.db
WHOOSH_BASE = os.path.join(basedir, 'search.db')
MAX_SEARCH_RESULTS =50

LANGUAGES = {
    'en': 'English',
    'es': 'Español',
	'zh': 'Chinese'
}
#1 .\venv\Scripts\pybabel extract -F babel.cfg -o messages.pot app
#2 .\venv\scripts\pybabel init -i messages.pot -d app\translations -l zh

# microsoft translation service
MS_TRANSLATOR_CLIENT_ID = '' # enter your MS translator app id here
MS_TRANSLATOR_CLIENT_SECRET = '' # enter your MS translator app secret here
Client_ID = '2d0b61c72539e88e49b7'
Client_Secret = 'ebad322a3ac06ed1c3887e74542f7c9eb33c4dc3'
#test
TEST_NUM=30