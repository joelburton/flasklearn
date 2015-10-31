"""Special field types for restful API."""

from HTMLParser import HTMLParser
from flask.ext.restful import fields


class HTMLStripper(HTMLParser):
    """Strip HTML."""

    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)

    @classmethod
    def strip_tags(cls, html):
        s = cls()
        s.feed(html)
        return s.get_data()


class HTMLField(fields.Raw):
    """HTML field."""

    def format(self, value):
        return HTMLStripper.strip_tags(str(value))
