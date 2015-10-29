"""Views specific to blog application."""

import datetime
from flask import Blueprint, request, redirect, url_for
from flask import render_template

from blogapp.forms import CommentForm, PostForm
from blogapp.models import Post, Tag, tags, Comment, User
from blogapp.models import db


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


blog_blueprint = Blueprint(
    'blog',
    __name__,
    template_folder='../templates/blog',
    url_prefix='/blog',
)


@blog_blueprint.route('/', defaults={'page': 1})
@blog_blueprint.route('/<int:page>')
def home(page):
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


@blog_blueprint.route('/new', methods=['GET', 'POST'])
def new_post():
    """Make new blog post."""

    form = PostForm()

    if form.validate_on_submit():
        new_post = Post(
            title=form.title.data,
            text=form.text.data,
            publish_date=datetime.datetime.now(),
        )

        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('.home'))

    return render_template('new.html', form=form)


@blog_blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    """Edit existing blog post."""

    post = Post.query.get_or_404(id)
    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.text = form.text.data
        post.publish_date = datetime.datetime.now()

        db.session.commit()

        return redirect(url_for('.post', post_id=post.id))

    form.text.data = post.text

    return render_template('edit.html', form=form, post=post)
