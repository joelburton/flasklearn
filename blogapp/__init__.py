"""Main file for blog app Flask server."""

from flask import Flask, redirect, url_for
from flask.ext.login import current_user
from flask.ext.principal import identity_loaded, UserNeed, RoleNeed
from sqlalchemy import event

from blogapp.controllers.main import main_blueprint
from blogapp.controllers.rest.auth import AuthApi
from blogapp.controllers.rest.post import PostApi
from .controllers.blog import blog_blueprint
from .controllers.play import play_blueprint
from .models import db, Reminder
from .extensions import bcrypt, oid, login_manager, principals, debug_toolbar, mongo, rest_api, \
    celery
from .tasks import on_reminder_save


def create_app(object_name):
    """Create Flask application.

    :param object_name: Flask configuration object.
    """

    app = Flask(__name__)
    app.config.from_object(object_name)

    db.init_app(app)
    bcrypt.init_app(app)
    oid.init_app(app)
    login_manager.init_app(app)
    principals.init_app(app)
    debug_toolbar.init_app(app)
    mongo.init_app(app)
    celery.init_app(app)

    event.listen(Reminder, 'after_insert', on_reminder_save)

    rest_api.add_resource(PostApi, '/api/post', '/api/post/<int:post_id>', endpoint='api')
    rest_api.add_resource(AuthApi, '/api/auth', endpoint='auth_api')
    rest_api.init_app(app)

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        # Set the identity user object
        identity.user = current_user

        # Add the UserNeed to the identity
        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))

        # Add each role to the identity
        if hasattr(current_user, 'roles'):
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.name))

    @app.route('/')
    def main_home():
        return redirect(url_for('blog.home'))

    app.register_blueprint(blog_blueprint)
    app.register_blueprint(play_blueprint)
    app.register_blueprint(main_blueprint)

    return app
