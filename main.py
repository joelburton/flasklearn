import datetime

from flask.views import View
from flask_wtf import Form
from flask import Flask, render_template, request, redirect, session, g, abort, Blueprint, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired
from wtforms.validators import Length
from config import DevConfig

app = Flask(__name__)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)


class User(db.Model):
    """User."""

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))

    posts = db.relationship('Post', backref='user', lazy='dynamic')

    def __repr__(self):
        return "<User {}>".format(self.username)


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


class Comment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    text = db.Column(db.Text())
    date = db.Column(db.DateTime())
    post_id = db.Column(db.Integer(), db.ForeignKey('post.id'))

    def __repr__(self):
        return "<Comment {}>".format(self.text[:15])


class Tag(db.Model):
    """Tags for blog posts."""

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))

    def __repr__(self):
        return "<Tag {}>".format(self.title)


def sidebar_data():
    """Return information needed for sidebars: most recent posts and most popular tags."""

    recent = Post.query.order_by(Post.publish_date.desc()).limit(5).all()

    top_tags = (db.session.query(Tag, db.func.count(tags.c.post_id).label('total'))
                .join(tags)
                .group_by(Tag)
                .order_by('total DESC')
                .limit(5)
                .all()
                )

    return recent, top_tags


class CommentForm(Form):
    """Form for submitting comments."""

    name = StringField(
        'Name',
        validators=[DataRequired(), Length(max=255)]
    )
    text = TextAreaField(u'Comment', validators=[DataRequired()])


blog_blueprint = Blueprint(
    'blog',
    __name__,
    template_folder='templates/blog',
    url_prefix='/blog',
)


@app.route('/')
def main_home():
    return redirect(url_for('blog.home'))


@blog_blueprint.route('/')
@blog_blueprint.route('/<int:page>')
def home(page=1):
    """Homepage. Lists posts."""

    posts = Post.query.order_by(Post.publish_date.desc()).paginate(page, 10)
    recent, top_tags = sidebar_data()

    return render_template(
        'home.html',
        posts=posts,
        recent=recent,
        top_tags=top_tags,
    )


@blog_blueprint.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    """Post detail page."""

    form = CommentForm()

    if form.validate_on_submit():
        # If valid form is submitted, add comment and redirect back to page
        new_comment = Comment()
        new_comment.name = form.name.data
        new_comment.text = form.text.data
        new_comment.post_id = post_id
        new_comment.date = datetime.datetime.now()

        db.session.add(new_comment)
        db.session.commit()
        return redirect(request.url)

    else:
        # No form submitted or form is invalid, show post (with errors if appropriate)
        post = Post.query.get_or_404(post_id)
        tags = post.tags
        comments = post.comments.order_by(Comment.date.desc()).all()
        recent, top_tags = sidebar_data()

        return render_template(
            'post.html',
            post=post,
            tags=tags,
            comments=comments,
            recent=recent,
            top_tags=top_tags,
            form=form,
        )


@blog_blueprint.route('/tag/<string:tag_name>')
def tag(tag_name):
    """Tag detail page."""

    tag = Tag.query.filter_by(title=tag_name).first_or_404()
    posts = tag.posts.order_by(Post.publish_date.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template(
        'tag.html',
        tag=tag,
        posts=posts,
        recent=recent,
        top_tags=top_tags
    )


@blog_blueprint.route('/user/<string:username>')
def user(username):
    """User detail page."""

    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.publish_date.desc()).all()
    recent, top_tags = sidebar_data()
    return render_template(
        'user.html',
        user=user,
        posts=posts,
        recent=recent,
        top_tags=top_tags
    )


@app.before_request
def before_request():
    """Add user to g if logged in."""

    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])
    else:
        g.user = None


@app.route('/restricted')
def admin():
    if g.user is None:
        abort(403)
    return render_template('admin.html')


@app.errorhandler(403)
def forbidden(error):
    return render_template("forbidden.html"), 403


class GenericView(View):
    """Generic template view."""

    def __init__(self, template):
        self.template = template
        super(GenericView, self).__init__()

    def dispatch_request(self):
        return render_template(self.template)


app.add_url_rule('/hey', view_func=GenericView.as_view('hey', template='hey.html'))

app.register_blueprint(blog_blueprint)

if __name__ == '__main__':
    app.run()
