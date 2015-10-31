from flask import abort
from flask.ext.restful import Resource, fields, marshal_with

from blogapp.controllers.rest.parsers import post_get_parser
from blogapp.models import Post, User
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
    'author': fields.String(attribute=lambda post: post.user.username),
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
