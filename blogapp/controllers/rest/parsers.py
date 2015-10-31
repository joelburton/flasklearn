from flask.ext.restful import reqparse

post_get_parser = reqparse.RequestParser()
post_get_parser.add_argument(
    'page',
    type=int,
    location=['json', 'args', 'headers'],
    required=False,
    default=1,
    help="Batch number to show. Must be an integer.",
)
post_get_parser.add_argument(
    'user',
    type=str,
    location=['json', 'args', 'headers'],
    required=False,
    help="Username to search for.",
)
