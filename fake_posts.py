import random
import datetime

from main import User, Tag, Post, db

user = User.query.get(1)

tag_one = Tag(title='Python')
tag_two = Tag(title='Flask')
tag_three = Tag(title='SQLAlchemy')
tag_four = Tag(title='Jinja')
tag_list = [tag_one, tag_two, tag_three, tag_four]

s = "Example text"

for i in xrange(100):
    new_post = Post(title="Post " + str(i))
    new_post.user = user
    new_post.publish_date = datetime.datetime.now()
    new_post.text = s
    new_post.tags = random.sample(tag_list, random.randint(1, 3))
    db.session.add(new_post)

db.session.commit()