from flask import flash, url_for, redirect, session
from flask.ext.assets import Environment, Bundle
from flask.ext.bcrypt import Bcrypt
from flask.ext.celery import Celery
from flask.ext.login import LoginManager
from flask.ext.mongoengine import MongoEngine
from flask.ext.oauth import OAuth
from flask.ext.openid import OpenID
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.restful import Api
from flask.ext.cache import Cache
from flask.ext.admin import Admin
from flask.ext.mail import Mail

bcrypt = Bcrypt()
oid = OpenID()
oauth = OAuth()
login_manager = LoginManager()
debug_toolbar = DebugToolbarExtension()
mongo = MongoEngine()
rest_api = Api()
celery = Celery()
cache = Cache()
assets_env = Environment()
admin = Admin()
mail = Mail()

main_css = Bundle(
    'css/site.css',
    filters='cssmin',
    output='css/common.css'
)

main_js = Bundle(
    'js/site.js',
    filters='jsmin',
    output='js/common.js'
)


@oid.after_login
def create_or_login(resp):
    from models import db, User
    username = resp.fullname or resp.nickname or resp.email
    if not username:
        flash('Invalid login. Please try again.', 'danger')
        return redirect(url_for('main.login'))

    user = User.query.filter_by(username=username).first()
    if user is None:
        user = User(username=username)
        db.session.add(user)
        db.session.commit()

    # Log the user in here
    return redirect(url_for('blog.home'))


facebook = oauth.remote_app(
    'facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key='446037675585555',
    consumer_secret='2dff74777b42d680c268f4f6d2e10e44',
    request_token_params={'scope': 'email'}
)


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('facebook_oauth_token')


twitter = oauth.remote_app(
    'twitter',
    base_url='https://api.twitter.com/1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key='Bhjr4f6WlUox1BGG8szvhj8lJ',
    consumer_secret='ZFlp0cBB9zPf3pDQvuS2E4MP2fxUnbnABTw9ofRUAzLJl3wmSk'
)


@twitter.tokengetter
def get_twitter_oauth_token():
    return session.get('twitter_oauth_token')


login_manager.login_view = "main.login"
login_manager.session_protection = "strong"
login_manager.login_message = "Please login to access this page"
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(userid):
    """Load user with this ID. Required by login manager."""

    from models import User
    return User.query.get(userid)


from flask.ext.principal import Principal, Permission, RoleNeed

principals = Principal()
admin_permission = Permission(RoleNeed('admin'))
poster_permission = Permission(RoleNeed('poster'))
default_permission = Permission(RoleNeed('default'))
