import os

import datetime
import random

from flask.ext.script import Manager, Server
from flask.ext.migrate import Migrate, MigrateCommand

from blogapp import create_app
from blogapp.models import db, User, Post, Comment, Tag, Role, Tweet, TweetComment, Reminder

# default to dev config
env = os.environ.get('WEBAPP_ENV', 'dev')
app = create_app('blogapp.config.%sConfig' % env.capitalize())

migrate = Migrate(app, db)

manager = Manager(app)

manager.add_command("server", Server())
manager.add_command("db", MigrateCommand)


@manager.shell
def make_shell_context():
    return dict(app=app,
                db=db,
                User=User,
                Post=Post,
                Tag=Tag,
                Comment=Comment,
                Role=Role,
                Tweet=Tweet,
                TweetComment=TweetComment,
                Reminder=Reminder,
                now=datetime.datetime.now
                )


def setup_posts():
    """Add posts."""

    user = User.query.get(1)

    tag_one = Tag(title='Python')
    tag_two = Tag(title='Flask')
    tag_three = Tag(title='SQLAlchemy')
    tag_four = Tag(title='Jinja')
    tag_list = [tag_one, tag_two, tag_three, tag_four]

    for i in xrange(1, 101):
        new_post = Post(title="Post " + str(i))
        new_post.user = user
        new_post.publish_date = datetime.datetime.now()
        new_post.text = "Example test for post #%s" % i
        new_post.tags = random.sample(tag_list, random.randint(1, 3))
        db.session.add(new_post)

    db.session.commit()


def setup_users():
    """Add users and roles."""

    poster = Role(name="poster")
    admin = Role(name="admin")
    default = Role(name="default")

    db.session.add_all([poster, admin, default])

    for username, roles in [("joel", [poster, admin]), ("george", [poster]), ("jane", [default])]:
        u = User(username=username, roles=roles)
        u.set_password("testtest")
        db.session.add(u)

    db.session.commit()


@manager.command
def fakedata():
    setup_users()
    setup_posts()


if __name__ == '__main__':
    manager.run()
