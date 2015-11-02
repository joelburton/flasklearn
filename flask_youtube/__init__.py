from flask import render_template, Blueprint, Markup


class Video(object):
    """Individual video element.

    :param video_id: Youtube video ID.
    :param cls: CSS class that gets added onto element
    """

    def __init__(self, video_id, cls="youtube"):
        self.video_id = video_id
        self.cls = cls

    def render(self, *args, **kwargs):
        return render_template(*args, **kwargs)

    @property
    def html(self):
        return Markup(
            self.render('youtube/video.html', video=self)
        )


def youtube(*args, **kwargs):
    """Jinja function to render a video."""

    video = Video(*args, **kwargs)
    return video.html


class Youtube(object):
    """YouTube extension object.

    This is the extension itself; it needs to be registered with init_app.
    """

    def __init__(self, app=None, **kwargs):
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.register_blueprint(app)

        # Make youtube() function available in jinja
        app.add_template_global(youtube)

    def register_blueprint(self, app):
        module = Blueprint(
            "youtube",
            __name__,
            template_folder="templates"
        )
        app.register_blueprint(module)
        return module
