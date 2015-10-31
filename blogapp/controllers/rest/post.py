import datetime
from flask import abort
from flask.ext.restful import Resource, fields, marshal_with

from blogapp.controllers.rest.parsers import post_get_parser, post_post_parser
from blogapp.models import Post, User, Tag, db
from .fields import HTMLField

nested_tag_fields = {
    'id': fields.Integer(),
    'title': fields.String()
}

post_fields = {
    'title': fields.String(),
    'text': HTMLField(),
    'publish_date': fields.DateTime(dt_format='iso8601'),
    'tags': fields.List(fields.Nested(nested_tag_fields)),
    'author': fields.String(attribute=lambda post: post.user.username if post.user else ''),
}


class PostApi(Resource):
    """Posts API."""

    @marshal_with(post_fields)
    def get(self, post_id=None):
        if post_id is not None:
            post = Post.query.get(post_id)
            if not post:
                abort(404)
            return post
        else:
            args = post_get_parser.parse_args()
            page = args['page']

            if args['user']:
                user = User.query.filter_by(username=args['user']).first()
                if not user:
                    abort(404)
                posts = user.posts.order_by(Post.publish_date.desc()).paginate(page, 3)
            else:
                posts = Post.query.order_by(Post.publish_date.desc()).paginate(page, 3)
            return posts.items

    def post(self, post_id=None):
        if post_id:
            abort(400)
        else:
            args = post_post_parser.parse_args(strict=True)
            user = User.verify_auth_token(args['token'])
            if not user:
                abort(401)
            new_post = Post(title=args['title'],
                            publish_date=datetime.datetime.now(),
                            text=args['text'],
                            user=user)

            if args['tags']:
                for item in args['tags']:
                    tag = Tag.query.filter_by(title=item).first()

                    # Add the tag if it exists.
                    # If not, make a new tag
                    if tag:
                        new_post.tags.append(tag)
                    else:
                        new_tag = Tag(title=item)
                        new_post.tags.append(new_tag)

            db.session.add(new_post)
            db.session.commit()
            return new_post.id, 201