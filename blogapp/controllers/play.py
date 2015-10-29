from flask import render_template, session, Blueprint, abort, g
from flask.views import View

from blogapp.models import User

play_blueprint = Blueprint(
    'play',
    __name__,
)


@play_blueprint.before_request
def before_request():
    """Add user to g if logged in."""

    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])
    else:
        g.user = None


@play_blueprint.route('/restricted')
def admin():
    if g.user is None:
        abort(403)
    return render_template('admin.html')


@play_blueprint.errorhandler(403)
def forbidden(error):
    return render_template("forbidden.html"), 403


class GenericView(View):
    """Generic template view."""

    def __init__(self, template):
        self.template = template
        super(GenericView, self).__init__()

    def dispatch_request(self):
        return render_template(self.template)


play_blueprint.add_url_rule('/hey', view_func=GenericView.as_view('hey', template='hey.html'))
