from flask import Flask, redirect, url_for

from blogapp.controllers.blog import blog_blueprint
from blogapp.controllers.play import play_blueprint
from blogapp.models import db
from config import DevConfig

app = Flask(__name__)
app.config.from_object(DevConfig)

db.init_app(app)


@app.route('/')
def main_home():
    return redirect(url_for('blog.home'))


app.register_blueprint(blog_blueprint)
app.register_blueprint(play_blueprint)


if __name__ == '__main__':
    app.run()
