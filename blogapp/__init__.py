"""Main file for blog app Flask server."""

from flask import Flask, redirect, url_for

from .controllers.blog import blog_blueprint
from .controllers.play import play_blueprint
from .models import db


def create_app(object_name):
    """Create Flask application.

    :param object_name: Flask configuration object.
    """

    app = Flask(__name__)
    app.config.from_object(object_name)

    db.init_app(app)

    @app.route('/')
    def main_home():
        return redirect(url_for('blog.home'))

    app.register_blueprint(blog_blueprint)
    app.register_blueprint(play_blueprint)

    return app
