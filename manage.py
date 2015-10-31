import os

from flask.ext.script import Manager, Server
from flask.ext.migrate import Migrate, MigrateCommand

from blogapp import create_app
from blogapp.models import db, User, Post, Comment, Tag, Role

# default to dev config
env = os.environ.get('WEBAPP_ENV', 'dev')
app = create_app('blogapp.config.%sConfig' % env.capitalize())

migrate = Migrate(app, db)

manager = Manager(app)

manager.add_command("server", Server())
manager.add_command("db", MigrateCommand)


@manager.shell
def make_shell_context():
    return dict(app=app, db=db, User=User, Post=Post, Tag=Tag, Comment=Comment, Role=Role)


if __name__ == '__main__':
    manager.run()
