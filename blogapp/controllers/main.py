"""Main routes."""

from flask import Blueprint, url_for, redirect, flash, render_template

from blogapp.forms import LoginForm, RegisterForm
from blogapp.models import User, db

main_blueprint = Blueprint(
    'main',
    __name__,
    template_folder="../templates/main",
)


@main_blueprint.route('/')
def index():
    """Homepage for main."""

    return redirect(url_for('blog.home'))


@main_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """Handle login; show form or process results."""

    form = LoginForm()

    if form.validate_on_submit():
        flash("You have been logged in.", category="success")
        return redirect(url_for('blog.home'))

    return render_template('login.html', form=form)


@main_blueprint.route('/logout', methods=['GET', 'POST'])
def logout():
    """Handle logout."""

    flash("You have been logged out.", category="success")
    return redirect(url_for('.home'))


@main_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    """Handle registration; show form or process results."""

    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User()
        new_user.username = form.username.data
        new_user.set_password(form.username.data)

        db.session.add(new_user)
        db.session.commit()

        flash(
            "Your user has been created, please login.",
            category="success"
        )

        return redirect(url_for('.login'))

    return render_template('register.html', form=form)
