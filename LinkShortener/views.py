# Copyright 2016 Richard Campen
# All rights reserved
# This software is released under the Modified BSD license
# See LICENSE.txt for the full license documentation

from flask import redirect, render_template, abort, request, url_for
from flask_login import login_user, logout_user, current_user
from flask_login import login_required

from LinkShortener import app
from LinkShortener.forms import LoginForm
from LinkShortener.models import User, Link

# TODO implement flash messages

@app.login_manager.user_loader
def load_user(user_id):
    user = User.query.filter_by(id=user_id).limit(1).first()
    return user

# TODO implement better logging of activity


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    """Route for displaying index page."""

    if current_user.is_authenticated:
        links_data = Link.retrieve_links(owner=current_user)
        return render_template('index.html', data=links_data)

    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Route for displaying login page and redirects to index or next page if supplied in request."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).limit(1).first()
        if user is not None:
            if user.verify_password(form.password.data):
                login_user(user)
                _next = request.args.get('next')
                return redirect(_next or '/')
        # TODO handle incorrect password better, perhaps during form validation.

    return render_template('login.html', title='Log In', form=form)


@app.route('/logout')
@login_required
def logout():
    """Route for logging out user."""
    logout_user()
    return redirect(url_for('index'))


@app.route('/<link_token>', methods=['GET'])
@app.route('/link/<link_token>', methods=['GET'])
def view_link(link_token):
    """Default route for viewing a link."""

    link_data = Link.retrieve_link(link_token)
    if link_data is None:
        abort(404)
    else:
        if link_data['private']:
            return redirect('/link/private/' + link_token)
        else:
            return redirect(link_data['link_url'], code=307)


@app.route('/link/private/<link_token>', methods=['GET'])
@login_required
def view_private_link(link_token):
    """Route for viewing a private link.

    If a request is made for a private link, the request is redirected to this route that requires
    that the client by logged in in order to view the link.
    """

    # TODO refactor to remove redundancy between this route and the view_link route.

    link_data = Link.retrieve_link(link_token=link_token)
    if link_data is None:
        abort(404)
    else:
        # Prevent caching of redirect with 307 status code
        return redirect(link_data['link_url'], code=307)


@app.route('/link/add', methods=['POST'])
@login_required
def add_link():
    """Add supplied link to the database."""

    private = False

    try:
        request_data = request.form.to_dict()
        submitted_link = request_data['link']
        if 'private' in request_data.keys():
            private = True
        link_data = Link.add_link(submitted_link=submitted_link, user=current_user, private=private)
    except Exception as e:
        print(e)

    return redirect(url_for('index'))


@app.route('/link/delete', methods=['POST'])
@login_required
def delete_link():
    """Delete supplied link from the database."""

    try:
        link_token = request.form['link_token']
        link_data = Link.delete_link(link_token=link_token)
    except Exception as e:
        print(e)

    return redirect(url_for('index'))

