"""Models for blog application."""


from flask.ext.sqlalchemy import SQLAlchemy

from .extensions import bcrypt


db = SQLAlchemy()


class User(db.Model):
    """User."""

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))

    posts = db.relationship('Post', backref='user', lazy='dynamic')

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        """Hash password and set."""

        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        """Return True if hashes correctly."""

        return bcrypt.check_password_hash(self.password, password)

tags = db.Table("post_tags",
                db.Column("post_id", db.Integer, db.ForeignKey("post.id")),
                db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"))
                )


class Post(db.Model):
    """Blog post."""

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))
    text = db.Column(db.Text())
    publish_date = db.Column(db.DateTime())
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

    comments = db.relationship("Comment", backref="post", lazy="dynamic")
    tags = db.relationship("Tag", secondary=tags, backref=db.backref("posts", lazy="dynamic"))

    def __repr__(self):
        return "<Post {}>".format(self.title)


class Tag(db.Model):
    """Tags for blog posts."""

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))

    def __repr__(self):
        return "<Tag {}>".format(self.title)


class Comment(db.Model):
    """Comments for blog posts."""

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    text = db.Column(db.Text())
    date = db.Column(db.DateTime())
    post_id = db.Column(db.Integer(), db.ForeignKey('post.id'))

    def __repr__(self):
        return "<Comment {}>".format(self.text[:15])
