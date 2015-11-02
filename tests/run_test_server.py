from blogapp import create_app
from blogapp.models import db, User, Role

app = create_app('blogapp.config.TestConfig')

db.app = app
db.create_all()

default = Role(name="default")
poster = Role(name="poster")
db.session.add(default)
db.session.add(poster)
db.session.commit()

test_user = User(username="test")
test_user.set_password("test")
test_user.roles.append(poster)
db.session.add(test_user)
db.session.commit()

app.run(port=5001, use_reloader=False)
